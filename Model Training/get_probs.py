import sys, os
import csv

sys.path.append('Utilities/')

from prob_class import Integrated_Problem, Codechef_Problem, Codeforces_Problem
from get_session import get_session, get_session_by_configuration
from constants import PlatformType

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
    print len(problist)
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
