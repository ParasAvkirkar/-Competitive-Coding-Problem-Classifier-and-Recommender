from gensim import models
import pickle
import operator
import sys
import copy

from sorting import sort_by_date_difficulty, sort_by_date
from generate_users_dataset import generateLazyLoad, generateLazyLoadAll
from get_probs import get_difficulty, get_category, get_all_probs_without_category_NA
from user_train_operations import get_categorywise_difficulty_limits, get_categorywise_tipping_points
from recommend_popular import get_popular
sys.path.append('Utilities/')

from constants import PlatformType, categories, stddifficultyLevels

noob_count = 0
low_sub_count = 0
total_count = 0
regular_count = 0

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
        # Insufficient input
        # Recommend popular problems
        # for each category in current diff level
        # present in optimum_category_level
        print str(diff) + " Insufficient input for this diff level. Recommend popular problems"

    return recommendation


"""
user - Username
prev_sub - No of recent submissions to consider for recommendation
diff - Difficulty level of problems to use for recommendation i.e ( "5" recently solved "easy" problems )
no_recomm - No of problems to recommend
"""


def get_user_level_by_category(categoryDifficultyMap, categorywise_difficulty_limits):
    optimum_category_level = {'easy': [], 'medium': [], 'hard': []}
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

def recommender(uniqueFileConvention, platform, user):

    global noob_count
    global low_sub_count
    global total_count
    global regular_count
    __user = ''
    total_count += 1

    userNameToObjects = generateLazyLoad(uniqueFileConvention, platform)

    categorywise_difficulty_limits = get_categorywise_difficulty_limits(uniqueFileConvention, PlatformType.Codechef,
                                                                        730)
    categoryDifficultyMap = userNameToObjects[user].categoryDifficultyMap
    optimum_category_level = get_user_level_by_category(categoryDifficultyMap, categorywise_difficulty_limits)

    submissionsDict = userNameToObjects[user].problemMappings

    # print "Category wise difficulty limits"
    # print categorywise_difficulty_limits
    # print "User submissions sorted by category and difficulty"
    # print categoryDifficultyMap

    all_recommendation = []
    print user

    if len(submissionsDict) < 5:
        # Cold Start
        # Recommend popular problems
        # Write code to see if he actually has < 5 submissions or is it due to
        # lack of problem categories if the latter case use other dictionary which
        # is w/o categorizing probs so at least something will be recommended
        print "Noob"

        uniqueFileConvention1 = 'users_codechef_all_probs'
        userNameToObjectsAll = generateLazyLoadAll(uniqueFileConvention1, platform=PlatformType.Codechef)
        submissionsDict = userNameToObjectsAll[user].problemMappings
        if len(submissionsDict) < 5:
            print "Real Noob"
            noob_count += 1
            # Recommend popular problems
        else:
            recommendation = get_word2vec_recommendation(uniqueFileConvention1, submissionsDict, 5, 'easy', 5)
            print recommendation

    else:
        # try:
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
                        # print_recommendation(recommendation)
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
                                                    # if len(optimum_category_level[level]) == 0:
                                                    #     del optimum_category_level[level]
                                                    #     break
                            else:
                                break
                    else:
                        # Low submission count for a particular level
                        print "Iteration " + str(iterations)
                        obtained_categories += len(optimum_category_level[level])
                        optimum_category_level[level][:] = []
                        # print categorywise_recomm

                        if user != __user:
                            __user = user
                            low_sub_count += 1

                        print("======================================")
                        break

        # except Exception as e:
        #     print e
        #     print level
        #     print optimum_category_level_copy
        #     print categoryDifficultyMap

        print categorywise_recomm
        print optimum_category_level_copy
        # ct = 0
        # for category in categorywise_recomm:
        #     ct += len(categorywise_recomm[category])
        # if ct == 12:
        #     regular_count += 1
        final_recommendation = []
        for level in stddifficultyLevels:
            for category in optimum_category_level_copy[level]:
                if categorywise_recomm[category]:
                    final_recommendation.append(categorywise_recomm[category][0][0])
                else:
                    prob_code = get_popular(level, category, all_recommendation, userNameToObjects[user].solved_probs)
                    final_recommendation.append(prob_code)

        print "Total iterations" + str(iterations)
        print final_recommendation
    print("=====================================================================================")



# uniqueFileConvention = 'users_codechef_all_probs'
# userNameToObjectsAll = generateLazyLoadAll(uniqueFileConvention, PlatformType.Codechef)
uniqueFileConvention = 'users_codechef'
userNameToObjects = generateLazyLoad(uniqueFileConvention, PlatformType.Codechef)
print "Total no of users in DB " + str(len(userNameToObjects))

#recommender(uniqueFileConvention, PlatformType.Codechef, 'pranet')

for username in userNameToObjects:
    recommender(uniqueFileConvention, PlatformType.Codechef, username)

print "Noob users - " +str(noob_count) + " Low_sub_count - " + str(low_sub_count) + " Regular - "+str(regular_count) \
      + " Total - " + str(total_count)
