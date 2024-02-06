# fatemetayebi

# Shortest-remaining-time-first (Shortest remaining time next)

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


def RQ(i, AT):
    rq = np.where(AT <= i, True, False)  # if arrival time it smaller than i then set that element true
    return rq  # an array of true and false to know what processes are in ready queue now


# Count executed time
zero = np.zeros(n)
ExtT = np.array(zero, dtype='i')  # an array for executed time for each processes


def ET(arr, inArr):  # function of ET add to executed time of processes
    arr[inArr] += 1
    return arr


# Count remaining time for each process
ReT = BT.copy()  # an array of remaining time of each processes


def RT(ReT, n):  # function to subtracting remaining time
    ReT[n] -= 1
    return ReT


# Creat a list of lists
process = [[]]


# Record executed time i = time , n = array index (process id) 
def Record(i, n):
    while n > len(process) - 1:  # if the input index is larger than length of list
        process.append([])  # then add i as a list
    else:
        process[n].append(i)  # if list has the index n so add i in the list with index n
    return process


# Find the shortest remaining time
def min(ReT, inRq):
    sort = np.sort(ReT)  # sort ReT array
    newRT = np.where(sort > 0, sort,
                     10000000)  # if there is finished process so change the remaining time to 1... to recognize minimum correctly
    newRT = np.sort(newRT)
    i = 0
    while newRT.any != 10000000:
        min = newRT[i]  # we sorted the remaining time so the first element is the smallest
        search = np.where(ReT == min)[0]  # get the index of the shortest remaining time in the ReT array
        se = int(search[0])
        if se in inRq:  # if the index is in array of arrived processes (inRq)
            return se  # so return it
        else:  # otherwise check the next smallest element
            i += 1


# Check if after a unit of time
while (ReT.any(0)):
    Rq = RQ(i, AT)
    inRq = np.where(Rq == True)[0]  # return the index of processes which are arrived
    a = min(ReT, inRq)  # return the index of a process with the shortest remaining time
    ExtT = ET(ExtT, a)  # add to executed time
    ReT = RT(ReT, a)  # subtract from remain time
    process = Record(i, a)
    # print(ReT)
    # print(inRq)                      
    # print(i)
    # print(a)
    # print(process)
    i += 1
print('\n', process, '\n')

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
sumTAT = 0
for i in TAT:
    sumTAT += i
print('\nAverage of turnaround time : ', sumTAT / n, '\n')

# Count waiting time
WT = np.subtract(TAT, BT)  # waiting time = turnaround time - burst time
print(WT)

# Count average waiting time
sumWT = 0
for i in WT:
    sumWT += i
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
                if (d == a):
                    li = (a * 10, 10)
                    gnt.broken_barh(wi, li, facecolors=(color[c]))
                    # print(li)
                    # print(wi)

                plt.savefig("gantt1.png")


Gantt(n, process)

####inputs 
5
3, 6, 4, 5, 2
0, 2, 4, 6, 8


