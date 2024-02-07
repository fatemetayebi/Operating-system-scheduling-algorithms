# fatemetayebi

# Round Robin

# first line of input: number of processes
# second line of input : needed time to execute of each process
# third line of input : arrival time of processes
# fourth line of input : quantum length

import numpy as np
import matplotlib.pyplot as plt
import random

# Get inputs
n = int(input(""))
BurstT = input("")
ArrivalT = input("")
q = int(input(""))

# Transform entries to int array
AT = ArrivalT.split(", ")
AT = np.array(AT, dtype='i')

# Transform entries to int array
BT = BurstT.split(", ")
BT = np.array(BT, dtype='i')

# Count executed time
zero = np.zeros(n)
ExtT = np.array(zero, dtype='i')  # an array for executed time for each processes


def ET(arr, a):  # function of ET add to executed time of processes
    arr[a] += 1
    return arr


# Count remaining time for each process
ReT = BT.copy()  # an array of remaining time of each processes


def RT(ReT, n):  # function to subtracting remaining time
    ReT[n] -= 1
    return ReT


# What process are in ready queue now?
i = 0


def RQ(i, AT, BT, ExtT):
    rq = np.where(AT <= i, True, False)
    for i in range(n):
        if BT[i] <= ExtT[i]:  # if executed time is equal to burt time remove the process because it was over
            rq[i] = False
    return rq


# Update inQT (index of QT process)
def UinQT(inRq, inQT, qt, q, ReT, ExtT, BT):
    for j in inRq:
        if j not in inQT:
            inQT = np.append(inQT, j)
            qt = np.append(qt, q)

    for h in inQT:
        if h not in inRq:
            d = int(np.where(inQT == h)[0])
            inQT = np.delete(inQT, d)
            qt = np.delete(qt, d)

    if qt[0] <= 0:
        if ExtT[inQT[0]] == BT[inQT[0]] and ReT[inQT[0]] <= 0:
            np.delete(inQT, 0)
            np.delete(qt, 0)
        else:
            temp = inQT[0]
            for i in range(len(inQT) - 1):
                inQT[i] = inQT[i + 1]
            inQT[-1] = temp
            qt[0] = q
    else:
        qt[0] -= 1

    return qt, inQT


# Creat a list of lists
process = [[]]


# Record executed time i = time , n = array index (process id) 
def Record(i, n):
    while n > len(process) - 1:  # if the input index is larger than length of list
        process.append([])  # then add i as a list
    else:
        process[n].append(i)  # if list has the index n so add i in the list with index n
    return process


# Check if after a unit of time
a = 0
inQT = np.array((), dtype='i')
qt = np.array((), dtype='i')
while not ((ExtT == BT).all()):
    Rq = RQ(i, AT, BT, ExtT)  # ready queue
    inRq = np.where(Rq == True)[0]  # return the index of processes which are arrived
    qt, inQT = UinQT(inRq, inQT, qt, q, ReT, ExtT, BT)
    a = inQT[0]

    ExtT = ET(ExtT, a)  # add to executed time
    ReT = RT(ReT, a)  # subtract from remain time
    process = Record(i, a)

    # print('in Rq:', inRq)                      
    # print('i = ', i)
    # print('Rq =', Rq)
    # print('ReT =', ReT)
    # print('inQT:', inQT)
    # print('qt:', qt)
    # print('executed time:', ExtT)
    # print('process:',process, '\n')

    i += 1

print(process)

# Count exit time
ExitT = []  # exit time
for i in range(n):
    ExitT.append(max(process[i]) + 1)  # exit time = the last element of process[index]
ExitT = np.array(ExitT)
# print(ExitT)

# Count turnaround time
TAT = np.subtract(ExitT, AT)  # turnaround time = exit time - arrival time
print(TAT)

# Count average of turnaround time
sumTAT = sum(TAT)
print('\nAverage of turnaround time : ', sumTAT / n, '\n')

# Calculate average of waiting time
wating = np.subtract(TAT, BT)
sumWT = sum(wating)
print('\nAverage of wating time : ', sumWT / n, '\n')

# Gantt chart
fig, gnt = plt.subplots()


def Gantt(n, process):
    gnt.set_ylim(0, (10 * n) + 20)
    # Setting X-axis limits 
    max = []
    for i in process:
        max.append(np.max(i))

    max = np.max(max) + 1
    gnt.set_xlim(0, max)
    # print(max)

    # Setting labels for x-axis and y-axis 
    gnt.set_xlabel('seconds')
    gnt.set_ylabel('Processor')

    # Setting ticks on y-axis
    ytick = [15]
    sumy = 15
    for i in range(n - 1):
        sumy += 10
        ytick.append(sumy)
    gnt.set_yticks(ytick)

    # Labelling tickes of y-axis 
    ytickL = []
    for i in range(1, n + 1):
        ytickL.append(i)
    ytickLa = map(str, ytickL)
    gnt.set_yticklabels(ytickLa)

    # Setting graph attribute 
    gnt.grid(True)

    # Declaring a bar in schedule 
    # [(fasele az chap , andze tul bar)], (fasele az paiin, andaze arze bar)
    color = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
             'tab:olive', 'tab:cyan', '#1f77b4',
             '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    wi = []

    # print(wi)

    li = ()

    # print(i)
    for i in process:
        c = int(random.randint(0, 19))
        for j in i:
            wi = []
            wi.append((j, 1))

            for a in range(1, n + 1):
                d = process.index(i) + 1
                if d == a:
                    li = (a * 10, 10)
                    gnt.broken_barh(wi, li, facecolors=(color[c]))
                    # print(li)
                    # print(wi)

                plt.savefig("Round-Robin.png")


Gantt(n, process)

#######inputs
3
24, 3, 3
0, 0, 0
4
