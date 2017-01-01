from get_probs import get_probs
import operator
import random

probs = get_probs()
prob_class = 'dp'



# dp nodp separate word count list
# dpCount = 0
# nodpCount = 0

# words = {0:{}, 1:{}}
# for p in probs:
#     if p.category == 'dp':
#         for w in p.description.split(' '):
#             if w not in words[1]:
#                 words[1][w] = 1
#             else :
#                 words[1][w] += 1
#     else:
#         for w in p.description.split(' '):
#             if w not in words[0]:
#                 words[0][w] = 1
#             else :
#                 words[0][w] += 1



# sorted_w = sorted(words[1].items(), key=operator.itemgetter(1))
# for w in sorted_w:
#     print w

# sorted_w = sorted(words[0].items(), key=operator.itemgetter(1))
# for w in sorted_w:
#     print w


#word count by, no of words in dp prob and in no dp prob
words = {}
random.shuffle(probs)

test_size = 0.2
train_set = probs[:-int(test_size*len(probs))]
test_set = probs[-int(test_size*len(probs)):]

for p in train_set:
    desclist = p.description.split()
    uniqWordList = sorted(set(desclist), key=desclist.index)
    p.description = ' '.join(uniqWordList)

    if p.category == prob_class:
        for w in p.description.split(' '):
            if w not in words:
                words[w] = {0:0, 1:0}
                words[w][1] = 1
            else :
                words[w][1] += 1
    else:
        for w in p.description.split(' '):
            if w not in words:
                words[w] = {0: 0, 1: 0}
                words[w][0] = 1
            else :
                words[w][0] += 1

percent = {}
for w in words:
    if (words[w][0] + words[w][1]) > 100: #word should have atleast 100 occurances
        percent[w] = 100.0 * words[w][1] / (words[w][0] + words[w][1])

sorted_perc = sorted(percent.items(), key=operator.itemgetter(1))
sorted_perc.reverse() #desc order

# print sorted_perc[:10]
# print sorted_perc[-10:]

total_data = []

count = 0
for p in train_set:
    total_data.append([])
    features = []

    for presentWord in sorted_perc[:10]:
        presentWord = presentWord[0] #it contains tuple of word and percentage, hence [0] element for word

        if presentWord in p.description.split():
            features.append(1)
        else:
            features.append(0)

    for notPresentWord in sorted_perc[-10:]:
        notPresentWord = notPresentWord[0]

        if notPresentWord in p.description.split():
            features.append(1)
        else:
            features.append(0)

    features.append(p.submission_size)
    features.append(p.time_limit[:1])

    if p.category == prob_class:
        features.append(1)
    else : features.append(0)

    total_data[count] = features
    count += 1

for p in test_set:
    total_data.append([])
    features = []
    for presentWord in sorted_perc[:10]:
        presentWord = presentWord[0]

        if presentWord in p.description.split():
            features.append(1)
        else:
            features.append(0)

    for notPresentWord in sorted_perc[-10:]:
        notPresentWord = notPresentWord[0]

        if notPresentWord in p.description.split():
            features.append(1)
        else:
            features.append(0)

    features.append(p.submission_size)
    features.append(p.time_limit[:1])

    if p.category == prob_class:
        features.append(1)
    else : features.append(0)

    total_data[count] = features
    count += 1


with open('dp_dataset.csv', 'w') as f:
    f.write(','.join([x[0] for x in sorted_perc[:10]]))
    f.write(','.join([x[0] for x in sorted_perc[-10:]]))
    f.write(',sub_size,time_limit')
    f.write(',class')

    f.write('\n')

    for t in total_data:
        f.write(','.join([str(x) for x in t]))
        f.write('\n')

