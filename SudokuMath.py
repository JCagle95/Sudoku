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

""" Hard  
matrix[0] = [8,9,0,3,0,6,2,0,0]
matrix[1] = [0,0,0,2,0,0,0,0,5]
matrix[2] = [2,0,0,9,1,0,0,0,0]
matrix[3] = [0,4,0,0,0,0,5,0,0]
matrix[4] = [0,0,3,0,5,0,8,0,0]
matrix[5] = [0,0,6,0,0,0,0,1,0]
matrix[6] = [0,0,0,0,8,7,0,0,6]
matrix[7] = [3,0,0,0,0,1,0,0,0]
matrix[8] = [0,0,7,6,0,3,0,5,8]
"""

""" Hard (Somewhat Harder)  """
matrix[0] = [0,5,0,0,0,0,2,0,9]
matrix[1] = [9,0,0,0,1,8,5,6,0]
matrix[2] = [0,0,0,0,0,3,0,4,0]
matrix[3] = [0,0,0,0,0,0,0,5,3]
matrix[4] = [0,8,0,0,0,0,0,7,0]
matrix[5] = [5,9,0,0,0,0,0,0,0]
matrix[6] = [0,2,0,6,0,0,0,0,0]
matrix[7] = [0,4,3,7,5,0,0,0,6]
matrix[8] = [6,0,5,0,0,0,0,2,0]

class SudokuSolver:
    def __init__(self, matrix, possible=defaultdict(lambda: None), 
                exist_x=defaultdict(lambda: None), 
                exist_y=defaultdict(lambda: None),
                exist_group=defaultdict(lambda: None),
                target_digit=defaultdict(lambda: None)):
                    
        self.matrix = matrix
        self.possible = possible
        self.exist_x = exist_x
        self.exist_y = exist_y
        self.exist_group = exist_group
        self.target_digit = target_digit
        self.toSolve = 0
        
        for x in range(9):
            self.exist_x[x] = Set(self.matrix[x,self.matrix[x,:]!=0])
            self.toSolve += sum(self.matrix[x,:]==0)
            
        for y in range(9):
            self.exist_y[y] = Set(self.matrix[self.matrix[:,y]!=0,y])
            
        for group in range(9):
            x = int(np.floor(group/3))
            y = group - x*3
            data = np.reshape(self.matrix[x*3:x*3+3,y*3:y*3+3],(1,9))
            self.exist_group[group] = Set(data[data!=0])
    
    def BruteForceSearch(self):
        # Reset the Start Condition
        Solution = defaultdict(lambda: None)
        found = 0
        Run = True
        
        # Only Run once unless we found some solutions
        while Run:
            Run = False
            
            # Grid Search
            for x in range(9):
                for y in range(9):
                    
                    # Index Calculation to reduce multiplication
                    pos = x*10+y
                    group = np.floor(x/3)*3+np.floor(y/3)
                    
                    # If Matrix[x,y] is 0, this is a block to be solved
                    if self.matrix[x,y] == 0:
                        
                        # Find all possible solutions in this block
                        self.possible[pos] = dict({"pool":Set(range(1,10)),"index":(x,y)})
                        self.possible[pos]["pool"].difference_update(self.exist_y[y])
                        self.possible[pos]["pool"].difference_update(self.exist_x[x])
                        self.possible[pos]["pool"].difference_update(self.exist_group[group])
                        
                        # If there is only 1 possible solution, this is the answer
                        if len(self.possible[pos]["pool"]) == 1:
                            
                            # Obtain The Solution (Digit)
                            digit = list(self.possible[pos]["pool"])[0]
                            self.matrix[self.possible[pos]["index"]] = digit
                            Solution[found] = dict({"pos":pos,"digit":digit})
                            
                            # Update the Search Variables
                            self.exist_group[group].add(digit)
                            self.exist_y[y].add(digit)
                            self.exist_x[x].add(digit)
                            
                            # Run again because search variable changes
                            Run = True
                            found+=1
                            
        return found, Solution
    
    def EliminationSearch(self):
        # Reset Start Condition
        Solution = defaultdict(lambda: None)
        found = 0
        
        # Search Each Group
        for group in range(9):
            
            # Determine what are possible digits within the 3x3 matrix
            self.target_digit[group] = Set(range(1,10))
            self.target_digit[group].difference_update(self.exist_group[group])
            
            # Loop through all possible digits within the 3x3 matrix
            for digit in self.target_digit[group]:
                
                # Calculate the Index
                x_t = int(np.floor(group/3))
                y_t = group - x_t*3
                
                # How many blocks meet the criteria
                TotalSlots = 0
                for x in range(x_t*3,x_t*3+3):
                    for y in range(y_t*3,y_t*3+3):
                        if self.possible[x*10+y] is not None:
                            if digit in self.possible[x*10+y]["pool"]:
                                TotalSlots+=1
                                pos = x*10+y
                                X = x
                                Y = y
                
                # If only one blocks meet the criteria, this is the solution
                if TotalSlots == 1:
                    
                    # Update Solution
                    self.matrix[self.possible[pos]["index"]] = digit
                    Solution[found] = dict({"pos":pos,"digit":digit})
                    
                    # Update the Search Variables
                    self.possible[pos]["pool"].clear()
                    self.possible[pos]["pool"].add(digit)
                    self.exist_group[group].add(digit)
                    self.exist_y[Y].add(digit)
                    self.exist_x[X].add(digit)
                    
                    # Elimination is Costly, only run when nothing is found by BruteFource
                    found += 1
        return found, Solution

if __name__ == "__main__":
    start = time.time()*1000
    
    solver = SudokuSolver(matrix)
    cycles = 0
    while solver.toSolve > 0:
        ForceFound,Solution = solver.BruteForceSearch()
        EliminationFound,Solution = solver.EliminationSearch()
        solver.toSolve -= (ForceFound+EliminationFound)
        matrix = solver.matrix
        cycles += 1
        
        #TODO:
        if ForceFound == 0 and EliminationFound == 0 and solver.toSolve > 0:
            """
            targetLength = len(solver.exist_group[0])
            targetGroup = 0
            for group in range(1,9):
                if len(solver.exist_group[group]) > targetLength:
                    targetGroup = group
                    targetLength = len(solver.exist_group[group])
            
            x_t = int(np.floor(targetGroup/3))
            y_t = targetGroup - x_t*3
            for x in range(x_t*3,x_t*3+3):
                for y in range(y_t*3,y_t*3+3):
                    if solver.possible[x*10+y] is not None:
                        if len(solver.possible[x*10+y]["pool"]) > 1:
                            GuessIndex = solver.possible[x*10+y]["index"]
                            GuessDigit = list(solver.target_digit[targetGroup])[0]
                    
            # Now is time to guess!
            temp = matrix
            temp[GuessIndex] = GuessDigit
            backupSolver = SudokuSolver(temp)
            backupSolver.matrix[GuessIndex] = GuessDigit
            ForceFound,Solution = backupSolver.BruteForceSearch()
            EliminationFound,Solution = backupSolver.EliminationSearch()
            """
            print "Unable to Complete Puzzle"        
            break
        
    if solver.toSolve == 0:
        print "Found All"
    
    end = time.time()*1000
    print "Time Consumed: " + str(end-start) + " milliseconds"
    print "Calculation Cycles: " + str(cycles) + " times"
