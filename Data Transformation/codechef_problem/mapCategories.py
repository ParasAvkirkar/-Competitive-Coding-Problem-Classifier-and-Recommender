import csv

probToTagsDictionary = {}
probToCategoryDictionary = {}
categories = {'greedy': ['greed']
    , 'graph': ['graph', 'dfs', 'bfs', 'biparti', 'hamilt', 'kruskal',
                'bellman', 'ford', 'floyd', 'warshal', 'mst', 'path',
                'flow', 'shortest-path', 'travel', 'salesman']
    , 'tree': ['tree']
    , 'combinatorics': ['combinat', 'pigeon']
    , 'math': ['math', 'fourier', 'modul', 'statistic', 'algebra', 'convex', 'polygon',
               'hull', 'number-theory', 'fastmodexp',
               'prime', 'factorization', 'sieve']
    , 'dp': ['dp', 'bitmask', 'dynamic', 'knapsack', 'memoiz', 'edit-distance']}

with open('codechef_problem.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        probToTagsDictionary[line[0]] = line[1]

with open('category.csv', 'w') as f:
    i = 1
    for prob_code in probToTagsDictionary:
        tagsString = probToTagsDictionary[prob_code]
        print('T ' + str(i) + ' ' + tagsString)
        catString = ''
        for cat in categories:
            catWords = categories[cat]
            for word in catWords:
                if word in tagsString:
                    catString = catString + (' ' if catString else '') + cat
                    print(word)
        catList = list(set(catString.split()))
        catString = ' '.join(word for word in catList)
        print('C ' + catString)
        f.write(prob_code + ',' + tagsString + ',' + catString + '\n')
        i += 1
