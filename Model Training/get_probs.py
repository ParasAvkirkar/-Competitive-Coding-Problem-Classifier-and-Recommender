import sys, os

sys.path.append('Utilities/')

from prob_class import Integrated_Problem, Codechef_Problem, Codeforces_Problem
from get_session import get_session, get_session_by_configuration
from constants import PlatformType


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


def get_all_probs_without_category_NA(useIntegrated=True, platform=PlatformType.Default):
    # s = get_session()
    s = get_session_by_configuration(useIntegrated)
    # probs = s.query(Problem).filter()
    if (useIntegrated):
        probs = s.query(Integrated_Problem).filter()
    elif platform == PlatformType.Codechef:
        probs = s.query(Codechef_Problem).filter()
    else:
        probs = s.query(Codeforces_Problem).filter()

    problist = [p for p in probs if p.category and 'N/A' not in p.category]
    print len(problist)

    return problist


def get_difficulty(prob_code):
    difficulty = 'NA'
    global probCodeToDifficulty

    if prob_code_difficulty_map_dict == None:
        probCodeToDifficulty = {}
        with open('codechef_prob_diff.csv', 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                probCodeToDifficulty[line[0]] = line[1]

    if prob_code in probCodeToDifficulty:
        difficulty = probCodeToDifficulty[prob_code]
    
    return difficulty


if __name__ == '__main__':
    get_all_probs()
