from gensim import models
import pickle
import csv

from sorting import sort_by_date_difficulty, sort_by_date

"""
user - Username
prev_sub - No of recent submissions to consider for recommendation
diff - Difficulty level of problems to use for recommendation i.e ( "5" recently solved "easy" problems )
no_recomm - No of problems to recommend
"""


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


def get_word2vec_recommendation(user, prev_sub, diff, no_recomm):
    model = models.Word2Vec.load("Codechef_word2vec")
    with open('userNameToObjectsDict.pickle', 'r+b') as f:
        userNameToObjectsDict = pickle.load(f)
    output_csv = open('recommend.csv', 'w')
    writer = csv.writer(output_csv)
    submissionsDict = userNameToObjectsDict[user].problemMappings

    sorted_submissions = sort_by_date_difficulty(submissionsDict, diff)

    submission_sentence = []

    [submission_sentence.append(row[0]) for row in sorted_submissions[-prev_sub:]]
    print submission_sentence  # Print problems given as input to recommender

    # Word2Vec function call to give recommendations
    recommendation = model.most_similar(positive=submission_sentence, topn=no_recomm)

    # For each row x in the list recommendation
    # x[0] - Problem codes
    # x[1] - Score
    #
    # To get difficulty for problem code use get_difficulty(prob_code) from get_probs.py

    print recommendation

    writer.writerow([user] + recommendation)

    return recommendation


get_word2vec_recommendation('i_am_what_i_am', 5, 'easy', 5)
