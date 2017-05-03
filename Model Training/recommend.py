from gensim import models
import pickle
import operator
import sys
import copy

from sqlalchemy.sql.functions import user

from sorting import sort_by_date_difficulty, sort_by_date
from generate_users_dataset import generateLazyLoad, generateLazyLoadAll, get_probCodeToObjects
from get_probs import get_difficulty, get_category, get_all_probs_without_category_NA
from user_level_limits import get_categorywise_difficulty_limits, get_difficulty_limits_without_category

from recommend_popular import get_popular

sys.path.append('Utilities/')

from constants import PlatformType, categories, stddifficultyLevels, codechefDifficultyLevels
tp = tn = fp = fn = 0

def build_recommendation_list_for_users(usersClusterMap, probs):
    probDict = {}
    for prob in probs:
        probDict[prob.prob_code] = prob

    for label in usersClusterMap:
        userList = usersClusterMap[label]
        for user in userList:
            user.calculate_user_level()
            print(user.uname + ' ' + str(len(user.failed_probs)) + ' ' + str(len(user.solved_probs)))
            if len(user.failed_probs) == 0 and len(user.solved_probs) > 0:
                print(user.uname + ' Level: ' + str(user.user_level))

        userList.sort(key=lambda x: x.user_level, reverse=True)
        # print(userList)

    for label in usersClusterMap:
        userList = usersClusterMap[label]

        probsSolvedUntilCurrentLevelUser = []
        generalUsersStartIndex = int(len(userList) * 0.1) + 1
        for i in range(len(userList)):
            tempDict = {}
            if i >= generalUsersStartIndex:
                for probCode in probsSolvedUntilCurrentLevelUser:
                    if probCode not in userList[i].solved_probs:
                        tempDict[probCode] = probDict[probCode].get_problem_level()

                        tempDict = dict(sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True))
                        # print(str(tempDict))
            for probCode in tempDict:
                userList[i].recommendation_list.append(probCode)
            # print(str(userList[i].recommendation_list))

            for probCode in userList[i].solved_probs:
                probsSolvedUntilCurrentLevelUser.append(probCode)

        usersClusterMap[label] = userList
        return usersClusterMap


def get_word2vec_recommendation(uniqueFileConvention, submissionsDict, prev_sub, diff, no_recomm):
    model = models.Word2Vec.load(uniqueFileConvention)

    sorted_submissions = sort_by_date_difficulty(submissionsDict, diff)
    recommendation = None

    if len(sorted_submissions) >= prev_sub:
        submission_sentence = []
        [submission_sentence.append(row[0]) for row in sorted_submissions[-prev_sub:]]

        # Word2Vec function call to give recommendations
        recommendation = model.most_similar(positive=submission_sentence, topn=no_recomm)

        # For each row x in the list recommendation
        # x[0] - Problem codes
        # x[1] - Score
        #
        # To get difficulty for problem code use get_difficulty(prob_code) from get_probs.py
    else:
        submission_sentence = []
        sorted_submissions = sort_by_date_difficulty(submissionsDict)
        [submission_sentence.append(row[0]) for row in sorted_submissions[-prev_sub:]]
        recommendation = model.most_similar(positive=submission_sentence, topn=no_recomm)

    return recommendation


def get_user_level_without_category(uniqueFileConvention, level_wise_submissions):
    optimum_level = 'easy'

    difficulty_limits = get_difficulty_limits_without_category(uniqueFileConvention, PlatformType.Codechef, 730)

    if level_wise_submissions['medium'] >= difficulty_limits['medium']:
        optimum_level = 'hard'

    elif level_wise_submissions['easy'] >= difficulty_limits['easy']:
        optimum_level = 'medium'

    return optimum_level


def get_user_level_by_category(uniqueFileConvention, categoryDifficultyMap):
    optimum_category_level = {'easy': [], 'medium': [], 'hard': []}

    categorywise_difficulty_limits = get_categorywise_difficulty_limits(uniqueFileConvention, PlatformType.Codechef,
                                                                        730)
    for category in categoryDifficultyMap:

        if categoryDifficultyMap[category]['medium'] >= categorywise_difficulty_limits[category]['medium']:
            optimum_category_level['hard'].append(category)
        elif categoryDifficultyMap[category]['easy'] >= categorywise_difficulty_limits[category]['easy']:
            optimum_category_level['medium'].append(category)
        else:
            optimum_category_level['easy'].append(category)

    # print "Optimum level for each category"
    # print optimum_category_level

    return optimum_category_level

def print_recommendation(recommendation):
    for row in recommendation:
        val = ''
        val += str(row) + " "
        for cat in get_category(row[0]):
            val +=  cat + " "
        val += get_difficulty(row[0])
        print val

def recommender(uniqueFileConvention, userObjects, username):

    global tp, tn, fp, fn

    submissionsDict = userObjects.problemMappings
    optimum_category_level = get_user_level_by_category(uniqueFileConvention, userObjects.categoryDifficultyMap)

    evalsubmissions = []
    for x in sort_by_date(submissionsDict)[-10:]:
        evalsubmissions.append(x[0])
    
    for prob_code in evalsubmissions:
        del submissionsDict[prob_code]

    # print "Category wise difficulty limits"
    # print categorywise_difficulty_limits
    # print "User submissions sorted by category and difficulty"
    # print categoryDifficultyMap

    final_recommendation = []

    if len(submissionsDict) < 5:

        uniqueFileConvention1 = 'users_codechef_all_probs'
        userObjectsAll = generateLazyLoadAll(uniqueFileConvention1, platform=PlatformType.Codechef, username=username)
        submissionsDict = userObjectsAll.problemMappings
        if len(submissionsDict) < 5:
            print "Less than 5 submissions for this user"
            for category in categories:
                final_recommendation.append(get_popular('easy', category, final_recommendation, {}))

        else:
            level = get_user_level_without_category(uniqueFileConvention, userObjectsAll[user].level_wise_submissions)
            recommendation = get_word2vec_recommendation(uniqueFileConvention1, submissionsDict, 5, level, 5)

            for problem in recommendation:
                final_recommendation.append(problem[0])

    else:

        all_recommendation = []
        iterations = 0
        obtained_categories = 0
        recomm_no_probs_per_category = 3
        prev_sub = 0
        no_recomm = 100
        score_threshold = 0.75
        optimum_category_level_copy = copy.deepcopy(optimum_category_level)
        categorywise_recomm = {}
        for category in categories:
            categorywise_recomm[category] = []
        while obtained_categories != 6 and iterations != 10:
            iterations += 1
            prev_sub += 5
            for level in optimum_category_level:
                if len(optimum_category_level[level]) != 0:
                    recommendation = get_word2vec_recommendation(uniqueFileConvention, submissionsDict, prev_sub, level, no_recomm)
                    if recommendation is not None:
                        for problem in recommendation:
                            if problem[1] >= score_threshold:
                                if get_difficulty(problem[0]) == level:
                                    rec_prob_cat = get_category(problem[0])
                                    for cat in rec_prob_cat:
                                        if cat in optimum_category_level[level]:
                                            if problem[0] not in all_recommendation:
                                                categorywise_recomm[cat].append(problem)
                                                all_recommendation.append(problem[0])
                                                if len(categorywise_recomm[cat]) == recomm_no_probs_per_category:
                                                    optimum_category_level[level].remove(cat)
                                                    obtained_categories += 1

                            else:
                                break
                    else:
                        # Low submission count for a particular level
                        obtained_categories += len(optimum_category_level[level])
                        optimum_category_level[level][:] = []

                        break

        for level in stddifficultyLevels:
            for category in optimum_category_level_copy[level]:
                if categorywise_recomm[category]:
                    final_recommendation.append(categorywise_recomm[category][0][0])
                else:
                    prob_code = get_popular(level, category, all_recommendation, userObjects.solved_probs)
                    final_recommendation.append(prob_code)

        for prob_code in final_recommendation:
            if prob_code in evalsubmissions:
                tp += 1
            else:
                fp += 1

        for prob_code in evalsubmissions:
            if prob_code not in final_recommendation:
                fn += 1

    print final_recommendation
    # print evalsubmissions

    recomm_prob_obj = []

    probObjects, probObjectsAll = get_probCodeToObjects()

    for prob_code in final_recommendation:
        try:
            recomm_prob_obj.append(probObjects[prob_code])
        except:
            recomm_prob_obj.append(probObjectsAll[prob_code])

    print("=====================================================================================")

    return recomm_prob_obj


def get_recommendations(username):

    uniqueFileConvention = 'users_codechef'
    platform = PlatformType.Codechef

    userObjects = generateLazyLoad(uniqueFileConvention, platform, username)

    recommended_probs = recommender(uniqueFileConvention, userObjects, username)

    return recommended_probs, userObjects.categoryDifficultyMap, sort_by_date(userObjects.problemMappings)


if __name__ == '__main__':

    get_recommendations("i_am_what_i_am")
    # uniqueFileConvention = 'users_codechef'
    # global tp, tn, fp, fn
    #
    # tp = tp * 1.0
    # precision = tp/(tp + fp)
    # recall = tp/(tp + fn)
    # f1_score = 2 * precision * recall / (precision + recall)
    #
    # print str(tp) + " " + str(fn)
    # print str(fp) + " " + str(tn)
    # print "Precision - " + str(precision)
    # print "Recall - " + str(recall)
    # print "F1score - " + str(f1_score)