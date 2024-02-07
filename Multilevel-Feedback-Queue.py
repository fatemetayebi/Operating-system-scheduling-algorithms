# fatemetayebi

# Multilevel Feedback Queue (Queue1: RR , Queue2: RR, Queue3: FCFS)

# first line of input: number of processes
# second line of input : needed time to execute of each process
# third line of input : arrival time of processes
# fourth line of input : first queue quantum length
# fifth line of input : second queue quantum length

import numpy as np
import matplotlib.pyplot as plt
import random

# Get inputs
n = int(input(""))
BurstT = input("")
ArrivalT = input("")
q1 = int(input(""))
q2 = int(input(""))

# Transform entries to int array
arrival_time = ArrivalT.split(", ")
arrival_time = np.array(arrival_time, dtype='i')

# Transform entries to int array
burst_time = BurstT.split(", ")
burst_time = np.array(burst_time, dtype='i')

# Count executed time
zero = np.zeros(n)
ExtT = np.array(zero, dtype='i')  # an array for executed time for each processes


def ET(arr, a):  # function of ET add to executed time of processes
    arr[a] += 1
    return arr


# What process are in ready queue now?
i = 0


def RQ(i, AT, BT, ExtT):
    rq = np.where(AT <= i, True, False)  # set true for a index if it is smaller than or equal to arrival time
    for i in range(n):
        if BT[i] <= ExtT[i]:  # if executed time is equal to burt time remove the process because it was over
            rq[i] = False
    return rq


# Creat a list of lists
process = [[]]


# Record executed time i = time , n = array index (process id) 
def Record(i, n):
    while n > len(process) - 1:  # if the input index is larger than length of list
        process.append([])  # then add i as a list
    else:
        process[n].append(i)  # if list has the index n so add i in the list with index n
    return process


# Shift elements
def shift(Q, index):
    Q = Q.tolist()
    if (Q[index + 1] != -2) and (Q[index] == -2):
        if (index >= n) & (index < 2 * n):
            Q = Q[0:n] + Q[n + 1:(2 * n)] + [Q[n]] + Q[2 * n:3 * n]
        elif (index >= 2 * n) & (index < 3 * n):
            Q = Q[0:2 * n] + Q[(2 * n) + 1:(3 * n)] + [Q[2 * n]]
    Q = np.array(Q)
    return Q


# An array for queues
Q = np.full(3 * n, -2, dtype='i')


def initQ(inRq, Q, ExtT):
    i = np.where(Q == -2)[0]  # empty blocks are in array i
    for j in inRq:
        if (j not in Q) and (
                ExtT[j] == 0):  # if there is element in ready queue, but it is not in Q, and it has not executed yet
            Q[i[0]] = j  # set the first empty block as process recently arrived
    return Q


# Chose one process to execute
def chose(Q):
    i = np.where(Q != -2)[0]
    j = i[0]
    return Q[j], j  # return the first element in Q (which is not -2 )and its index


# Executing
def executing(q, index, process, ExtT, time, Q, BT):
    while q > 0 and (BT[index] != ExtT[index]):  # do executing while quantum become 0
        ExtT = ET(ExtT, index)  # add to executed time
        process = Record(time, index)  # add the current second to index of process
        time += 1
        q -= 1
    i = np.where(Q == -2)[0]
    j = int(np.where(Q == index)[0])
    n = len(Q) / 3
    if BT[index] == ExtT[index]:  # if process is over remove it from Q array
        Q[j] = -2
    elif (j >= 0) & (j < n):  # if process is not over, and it is in the first 1/3 of array transfer it to second 1/3
        Q[j] = -2
        m = (np.where(i < 2 * n) and np.where(i >= n))[0]
        Q[i[m[0]]] = index
        Q = shift(Q, j)
    elif (j >= n) & (j < 2 * n):  # if process is not over, and it is in the second 1/3 of array transfer it to third 1/3
        Q[j] = -2
        m = (np.where(i < 3 * n) and np.where(i >= 2 * n))[0]
        Q[i[m[0]]] = index
        Q = shift(Q, j)
    return process, ExtT, Q, time


# While
time = 0
while not ((ExtT == burst_time).all()):
    Rq = RQ(time, arrival_time, burst_time, ExtT)  # ready queue
    inRq = np.where(Rq == True)[0]  # return the index of processes which are arrived
    Q = initQ(inRq, Q, ExtT)  # if a process is arrived add it to array Q
    pr, index = chose(Q)  # choose a process to execute
    if (index >= 0) & (index < n):  # if index is in first 1/3 of Array, quantum is equal to q1
        q = q1
    elif (index >= n) & (index < 2 * n):  # if index is in second 1/3 of Array, quantum is equal to q2
        q = q2
    elif (index >= 2 * n) & (
            index < 3 * n):  # if index is in third 1/3 of Array, quantum is equal to the remaining time of process
        q = burst_time[pr] - ExtT[pr]
    process, ExtT, Q, time = executing(q, pr, process,  # execute chosen process
                                       ExtT, time, Q, burst_time)

    # print(time)
    # print(process)
    # print(ExtT)
    # print(Q)
    # print(inRq)
    # print('\n')

# Count exit time
ExitT = []  # exit time
for i in range(n):
    ExitT.append(max(process[i]) + 1)  # exit time = the last element of process[index]
ExitT = np.array(ExitT)
# print(ExitT)

# Count turnaround time
TAT = np.subtract(ExitT, arrival_time)  # turnaround time = exit time - arrival time
print(TAT)

# Count average of turnaround time
sumTAT = sum(TAT)
print('\nAverage of turnaround time : ', sumTAT / n, '\n')

# Calculate average of waiting time
wating = np.subtract(TAT, burst_time)
sumWT = sum(wating)
print('\nAverage of waiting time : ', sumWT / n, '\n')

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

                plt.savefig("Multilevel-Feedback-Queue.png")


Gantt(n, process)

# inputs
5
3, 6, 4, 5, 2
0, 2, 4, 6, 8
1
2
