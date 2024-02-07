# fatemetayebi

# Highest Response Ratio Next

# first line of input: number of processes
# second line of input : needed time to execute of each process
# third line of input : arrival time of processes

import numpy as np
import matplotlib.pyplot as plt
import random

# Get inputs
n = int(input(""))
BurstT = input("")
ArrivalT = input("")

# Transform entries to int array
AT = ArrivalT.split(", ")
AT = np.array(AT, dtype='i')

# Transform entries to int array
BT = BurstT.split(", ")
BT = np.array(BT, dtype='i')

# What process are in ready queue now?
i = 0


def RQ(i, AT, a, BT, ExtT):
    rq = np.where(AT <= i, True,
                  False)  # if arrival time of a process is smaller than current time so add it to ready queue
    for i in range(n):
        if BT[i] <= ExtT[i]:  # if executed time is equal to burt time remove the process because it was over
            rq[i] = False
    if BT[a] > ExtT[
        a]:  # the algorithm is non-preemptive so if the current process is not over add it to queue(continue it)
        rq[a] = True
    else:
        rq[a] = False  # otherwise if it is over remove it from ready queue
    return rq


# Count executed time
zero = np.zeros(n)
ExtT = np.array(zero, dtype='i')  # an array for executed time for each processes


def ET(arr, inArr):  # function of ET add to executed time of processes
    arr[inArr] += 1
    return arr


# Count waiting time
WTi = np.array(zero, dtype='i')


def WT(inRq, WTi):
    for i in inRq:
        WTi[i] += 1
    return WTi


# Count response ratio for each processes in RQ
RR = np.array(zero, dtype='f')


def HRR(RR, inRq, WTi):
    for i in inRq:
        RR[i] = WTi[i] / BT[i]
    return RR


# Creat a list of lists
process = [[]]


# Record executed time i = time , n = array index (process id) 
def Record(i, n):
    while n > len(process) - 1:  # if the input index is larger than length of list
        process.append([])  # then add i as a list
    else:
        process[n].append(i)  # if list has the index n so add i in the list with index n
    return process


# Find the highest response ratio
def HighestRR(RR, ExtT, BT):
    for i in range(n):
        if ExtT[i] >= BT[i]:  # if a process is over check another one
            continue
        else:
            max = np.max(RR)  # find the highest response ratio
            search = np.where(RR == max)[0]
    return int(search[0])  # return the index of process with the highest response ratio


# Check if after a unit of time
a = 0
j = 0
while not ((ExtT == BT).all()):
    Rq = RQ(i, AT, a, BT, ExtT)  # ready queue
    inRq = np.where(Rq == True)[0]  # return the index of processes which are arrived
    RR = HRR(RR, inRq, WTi)  # response ratio array
    if len(inRq) == 1:  # if we have just one process it doesn't need to calculate the highest response ratio
        a = inRq[0]  # return the only process index
    elif ExtT[a] == BT[a]:  # if the current process is over-
        a = HighestRR(RR, ExtT, BT)  # choes another one
        # otherwise it doesn't need to change the process
    ExtT = ET(ExtT, a)  # add to executed time
    WTi = WT(inRq, WTi)  # if there is a process in ready queue add to its waiting time
    process = Record(i, a)

    # print('\n','response ratio:', RR)
    # print('in Rq:', inRq)                      
    # print('i = ', i)
    # print('Rq =', Rq)
    # print('WTi =', WTi)
    # print('highest RR:', a)
    # print('executed time:', ExtT)
    # print('process:',process, '\n')
    i += 1
    j += BT[a]

# Calculate average of turnaround time
sumTT = sum(WTi)
print('\nAverage of turnaround time : ', sumTT / n, '\n')

# Calculate average of waiting time
wating = np.subtract(WTi, BT)
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

                plt.savefig("Highest-Response-Ratio-Next.png")


Gantt(n, process)

5
3, 6, 4, 5, 2
0, 2, 4, 6, 8
