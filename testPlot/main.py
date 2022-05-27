import matplotlib.pyplot as plt
import pandas
import json

dict = {
    0: {'person': {'id': '1', 'Name': 'George', 'Family': 'Wood', 'Position': '1'
        }, 'listSplit': [
            501,
            720,
            818,
            1136,
            1593,
            123
        ]
    },
    1: {'person': {'id': '2', 'Name': 'Pippo', 'Family': 'Baudo', 'Position': '2'
        }, 'listSplit': [
            551,
            730,
            848,
            1136,
            1593,
            234
        ]
    }
}

lenx = len(dict[0]['listSplit'])
x = [*range(1 , lenx+1, 1)]

for p in dict:
    if dict[p]['person']['Position'] == str(1):
        splitFirst = dict[p]['listSplit']

if len(splitFirst)==0:
    print('hai fuckappato')

id = 'event'
cl = 'class'
plt.title('Race: '+id+'\nClass: '+cl)
plt.ylabel('Time difference')
plt.xlabel('Control')
for person in dict:

    split = dict[person]['listSplit']
    y = []
    zip_object = zip(split, splitFirst)
    for list1_i, list2_i in zip_object:
        y.append(list1_i-list2_i)

    plt.plot(x, y, linestyle="", marker="o")
    plt.plot(x, y, color=plt.gca().lines[-1].get_color())
    plt.ylim(max(y)+10, 0)

plt.show()
