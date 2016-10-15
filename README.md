# Sudoku
This is a graphical user interface for Sudoku Puzzle solver. 
This program is designed in Python, using Python Wrapper for Simple DirectMedia Layer 2 (PySDL2, https://pysdl2.readthedocs.io/en/rel_0_9_4/) as rendering system.

## Files:
###SudokuGUI.py
The graphical user interface based on SDL2. Use pointer to click on the blocks to highlight block for edit.

Keyboard Control

1. Type Q to Quit Program.
2. Click on a Block, and type in the digit using Small Number Keypad.
3. Highlight a block already with digit, Click R and retype the digit.
4. Click "SolveIt!" to solve the puzzle give. 
5. Click "Reset" to refresh the Sudoku and solve the next one.

###SudokuMath.py
The mathematical and logical flow of how a Sudoku can be solved. The testing Sudoku matrix are obtained from **Web Sudoku** (http://www.websudoku.com/).

The key approach for solving Sudoku is based on Brute Force Searching and Elimination Searching. 
Combination of these two methods can solve every puzzle (that have been tested by me) from Easy to Hard.

+ Easy and Medium can be solved with only Brute Force and Elimination Searching within 15 milliseconds.
+ Some Hard Puzzles can be solved with iteration of Brute Force and Elimination Searching within 15 milliseconds.
+ Majority of Hard and Evil Puzzles are puzzles must be search with intuitive guessing and iterations of try-and-error (Currently not implemented). 


## Installation as Windows Executable:
To Install:

`>> python setup.py py2exe`

To Run without Installation:

`>> python SudokuGUI.py`


# Resources Used:
Simple DirectMedia Layer 2: https://www.libsdl.org/download-2.0.php

Simple DirectMedia Layer 2 - LibImage: https://www.libsdl.org/projects/SDL_image/

Simple DirectMedia Layer 2 - LibTTF: https://www.libsdl.org/projects/SDL_ttf/

Fonts: GillSans-SemiBold.ttf: https://github.com/maxpushkarev/resume

