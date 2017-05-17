import sys, os
import csv

sys.path.append('../Utilities/')
sys.path.append('../../Data Transformation/integrated/')
from prob_class import Integrated_Problem, Codechef_Problem, Codeforces_Problem
from get_session import get_session, get_session_by_configuration
from constants import PlatformType
from transform_description import transform, new_transform

probCodeToDifficulty = None
probCodeToCategory = None


def get_all_probs(useIntegrated=True, platform=PlatformType.Default):
    # s = get_session()
    s = get_session_by_configuration(useIntegrated)
    if (useIntegrated):
        probs = s.query(Integrated_Problem).filter()
    elif platform == PlatformType.Codechef:
        probs = s.query(Codechef_Problem).filter()
    else:
        probs = s.query(Codeforces_Problem).filter()
    problist = [p for p in probs]

    problist = [p for p in probs if 'connect' in p.description]
    i = 0
    processed_till_now = 0
    print(str(len(problist)))
    try:
        for prob in problist:
            o = prob.modified_description
            prob.modified_description = transform(prob.description)
            # prob.modified_description = new_transform(prob.description)
            # print(o + '\n' + prob.modified_description)
            # if i > 1000:
            #     break
            if i%100 == 0:
                print(str(i))
            print(str(i))
            i += 1
            # print(str(prob.prob_code) + ' ' + str(prob.modified_description))
            processed_till_now += 1
            if processed_till_now > 100:
                processed_till_now = 0
                s.commit()
        print len(problist)
    except Exception as e:
        print(str(e))
        print(str(prob.prob_code) + ' ' + str(prob.modified_description))

    s.commit()
    return problist


def get_all_probs_without_category_NA(useIntegrated=True, platform=PlatformType.Default, probs_all_or_categorywise=1):
    # s = get_session()
    s = get_session_by_configuration(useIntegrated)
    # probs = s.query(Problem).filter()
    if (useIntegrated):
        probs = s.query(Integrated_Problem).filter()
    elif platform == PlatformType.Codechef:
        probs = s.query(Codechef_Problem).filter()
    else:
        probs = s.query(Codeforces_Problem).filter()


    if probs_all_or_categorywise == 1:
        problist = [p for p in probs if p.category and 'N/A' not in p.category]
    else:
        problist = [p for p in probs if p.category != 'N/A']




    return problist


def get_probCodeToObjectMap(useIntegrated=True, platform=PlatformType.Default):
    probs = get_all_probs_without_category_NA(useIntegrated = useIntegrated, platform = platform)
    probCodeToObjects = {}
    for prb in probs:
        probCodeToObjects[prb.prob_code] = prb

    return probCodeToObjects

def get_difficulty(prob_code):
    difficulty = 'NA'
    global probCodeToDifficulty

    if probCodeToDifficulty == None:
        probCodeToDifficulty = {}
        with open('codechef_prob_diff.csv', 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                probCodeToDifficulty[line[0]] = line[1]

    if prob_code in probCodeToDifficulty:
        difficulty = probCodeToDifficulty[prob_code]

    return difficulty


# Currently implemented for Codechef, because its difficulty for some probs are empty,
#  later on can be replicated for other platforms
def get_probCodeToDiff_Map(platform=PlatformType.Codechef):
    if platform == PlatformType.Codechef:
        probCodeToDifficulty = {}
        with open('codechef_prob_diff.csv', 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                probCodeToDifficulty[line[0]] = line[1]
        return probCodeToDifficulty

    return None


def get_category(prob_code):
    category = 'NA'
    global probCodeToCategory

    if probCodeToCategory == None:
        probCodeToCategory = {}
        with open('codechef_prob_cat.csv', 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                probCodeToCategory[line[0]] = line[1]

    if prob_code in probCodeToCategory:
        category = probCodeToCategory[prob_code]
        category = category.split()

    return category


if __name__ == '__main__':
    get_all_probs()
