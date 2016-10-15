# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 19:08:45 2016

@author: Jackson
"""

import numpy as np
from sets import Set
from collections import defaultdict
import time
        
# Testing Dataset
matrix = np.zeros((9,9),dtype=np.int8)
possible = defaultdict(lambda: None)
exist_x = defaultdict(lambda: None)
exist_y = defaultdict(lambda: None)
exist_group = defaultdict(lambda: None)
target_digit = defaultdict(lambda: None)

""" Medium Level 
matrix[0] = [0,0,4,0,6,9,0,7,5]
matrix[1] = [7,0,0,0,5,0,0,0,2]
matrix[2] = [0,3,0,2,0,0,0,0,0]
matrix[3] = [4,0,0,0,1,0,0,0,0]
matrix[4] = [3,0,7,8,4,2,5,0,1]
matrix[5] = [0,0,0,0,3,0,0,0,4]
matrix[6] = [0,0,0,0,0,6,0,2,0]
matrix[7] = [6,0,0,0,8,0,0,0,3]
matrix[8] = [5,8,0,4,2,0,7,0,0]
"""

""" Hard """
matrix[0] = [8,9,0,3,0,6,2,0,0]
matrix[1] = [0,0,0,2,0,0,0,0,5]
matrix[2] = [2,0,0,9,1,0,0,0,0]
matrix[3] = [0,4,0,0,0,0,5,0,0]
matrix[4] = [0,0,3,0,5,0,8,0,0]
matrix[5] = [0,0,6,0,0,0,0,1,0]
matrix[6] = [0,0,0,0,8,7,0,0,6]
matrix[7] = [3,0,0,0,0,1,0,0,0]
matrix[8] = [0,0,7,6,0,3,0,5,8]

start = time.time()*1000

toSolve = 0

for x in range(9):
    exist_x[x] = Set(matrix[x,matrix[x,:]!=0])
    toSolve += sum(matrix[x,:]==0)
    
for y in range(9):
    exist_y[y] = Set(matrix[matrix[:,y]!=0,y])
    
for group in range(9):
    x = int(np.floor(group/3))
    y = group - x*3
    data = np.reshape(matrix[x*3:x*3+3,y*3:y*3+3],(1,9))
    exist_group[group] = Set(data[data!=0])

found = 0

while found < toSolve:
    Run = True
    while Run:
        Run = False
        for x in range(9):
            for y in range(9):
                pos = x*10+y
                group = np.floor(x/3)*3+np.floor(y/3)
                if matrix[x,y] == 0:
                    possible[pos] = dict({"pool":Set(range(1,10)),"index":(x,y)})
                    possible[pos]["pool"].difference_update(exist_y[y])
                    possible[pos]["pool"].difference_update(exist_x[x])
                    possible[pos]["pool"].difference_update(exist_group[group])
                    if len(possible[pos]["pool"]) == 1:
                        digit = list(possible[pos]["pool"])[0]
                        matrix[possible[pos]["index"]] = digit
                        exist_group[group].add(digit)
                        exist_y[y].add(digit)
                        exist_x[x].add(digit)
                        Run = True
                        found+=1

    for group in range(9):
        target_digit[group] = Set(range(1,10))
        target_digit[group].difference_update(exist_group[group])
        for digit in target_digit[group]:
            x_t = int(np.floor(group/3))
            y_t = group - x_t*3
            TotalSlots = 0
            for x in range(x_t*3,x_t*3+3):
                for y in range(y_t*3,y_t*3+3):
                    if possible[x*10+y] is not None:
                        if digit in possible[x*10+y]["pool"]:
                            TotalSlots+=1
                            pos = x*10+y
                            X = x
                            Y = y
                            
            if TotalSlots == 1:
                matrix[possible[pos]["index"]] = digit
                possible[pos]["pool"].clear()
                possible[pos]["pool"].add(digit)
                exist_group[group].add(digit)
                exist_y[Y].add(digit)
                exist_x[X].add(digit)
                found += 1


end = time.time()*1000
print "Time Consumed: " + str(end-start) + " milliseconds"
