def sort_by_date(submissionsDict):
    sorted_submissions = []

    date_wise_submissions = []

    for prob_code in submissionsDict:
        date_wise_submissions.append(
            [prob_code, submissionsDict[prob_code].date, submissionsDict[prob_code].difficulty])

    date_wise_submissions = sorted(date_wise_submissions, key=lambda k: k[1])

    sorted_submissions = sorted_submissions + date_wise_submissions

    return sorted_submissions


def sort_by_date_difficulty(submissionsDict, diff=None):
    if diff is None:
        difficulty = ['easy', 'medium', 'hard']
    else:
        difficulty = [diff]

    sorted_submissions = []

    for level in difficulty:

        level_wise_submissions = []

        for prob_code in submissionsDict:
            if submissionsDict[prob_code].difficulty == level:
                level_wise_submissions.append(
                    [prob_code, submissionsDict[prob_code].date, submissionsDict[prob_code].difficulty])

        level_wise_submissions = sorted(level_wise_submissions, key=lambda k: k[1])

        sorted_submissions = sorted_submissions + level_wise_submissions

    return sorted_submissions
