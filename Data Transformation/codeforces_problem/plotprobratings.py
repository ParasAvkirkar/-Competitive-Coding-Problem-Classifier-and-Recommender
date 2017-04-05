import csv
import matplotlib.pyplot as plt

with open('problem_ratings.csv', 'r') as f:
    reader = csv.reader(f)
    isfirst = True
    values = []
    for line in reader:
        if isfirst:
            isfirst = False
        else:
            rat = float(line[2])
            values.append(rat)
    values.sort(reverse = True)
    plt.plot(values, 'b-')

    plt.xlabel(' problems')
    plt.ylabel(' ratings')
    plt.show()
