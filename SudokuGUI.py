"""
The Sudoku GUI is a graphical user interface for Sudoku. 
It will automatically solving the Sudoku for you when you click Solve It!

@author:
Jackson Cagle
Brain Mapping Laboratory
J. Crayton Pruitt Family Department of Biomedical Engineering, 
University of Florida
"""

import os
import sys; sys.path.append('.\\SDL2\\PySDL2')
if sys.maxsize > 2**32:
    os.environ['PYSDL2_DLL_PATH'] = '.\\SDL2'
else:
    os.environ['PYSDL2_DLL_PATH'] = '.\\SDL2\\x86'
import ctypes
import sdl2
import numpy as np
import sdl2.sdlttf
import sdl2.ext
from collections import defaultdict
from sets import Set
import time

from SudokuMath import SudokuSolver

RESOURCES = sdl2.ext.Resources(".", "resources")

GREY = sdl2.ext.Color(200, 200, 200)
WHITE = sdl2.ext.Color(225, 225, 225)
BLACK = sdl2.SDL_Color(0, 0, 0)
CYAN = sdl2.SDL_Color(0, 70, 90)
GREEN = sdl2.ext.Color(0, 255, 0)
RED = sdl2.SDL_Color(255, 0, 0)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 1000

class Sudoku:
    def __init__(self):
        self.input = defaultdict(lambda: None)
        self.block = defaultdict(lambda: None)
        self.digit = defaultdict(lambda: None)
        self.grid = defaultdict(lambda: None)
        self.matrix = np.zeros((9,9),dtype=np.int8)
        self.selected = False
        self.chosen = 0
        
    def updateBlocks(self, sprite, x, y):
        self.block[x*10+y] = sprite
        self.block[x*10+y].position = x*100+5, y*100+5
        self.input[x*10+y] = dict({"Position":(x,y),"State":False})
        
    def updateDigits(self, sprite, chosen, state, digit):
        self.digit[chosen] = sprite
        self.digit[chosen].position = np.add(self.block[chosen].position,(25,10))
        self.input[chosen]["State"] = state
        if state:
            self.matrix[self.input[chosen]["Position"]] = digit
        
    def updateGrid(self, sprite, x, y):
        self.grid[x*1000+y] = sprite
        self.grid[x*1000+y].position = x, y
    
    def reset(self):
        self.input = defaultdict(lambda: None)
        self.block = defaultdict(lambda: None)
        self.digit = defaultdict(lambda: None)
        self.grid = defaultdict(lambda: None)
        self.matrix = np.zeros((9,9),dtype=np.int8)
        self.selected = False
        self.chosen = 0
    
class SudokuGUI():
    
    def __init__(self):
        # Initialize Window
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Sudoku Solver", size=(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.window.show()
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        self.spriterenderer = self.factory.create_sprite_render_system(self.window)
        
        # Initialize TTF Printer
        sdl2.sdlttf.TTF_Init()
        self.font = sdl2.sdlttf.TTF_OpenFont(RESOURCES.get_path("GillSans-SemiBold.ttf"),60)
        self.digit = 0
        
        # Grid and Matrix Setup
        self.Sudoku = Sudoku()
        self.buildBackground()
        
        # Input Event Manipulation
        self.KeyAction = defaultdict(lambda: self.NoAction)
        self.KeyAction[sdl2.SDL_SCANCODE_Q] = self.Quit
        self.KeyAction[sdl2.SDL_SCANCODE_R] = self.DigitReset
        for scancode in range(89,98):
            self.KeyAction[scancode] = self.KeyEnter
            
        self.running = True
        self.reset = False
    
    def buildBackground(self):
        sprite =self.factory.from_color(WHITE, size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        sprite.position = 0,0
        self.spriterenderer.render(sprite)
        for x in (0,897):
            sprite =self.factory.from_color(CYAN, size=(3, 900))
            sprite.position = x,0
            self.spriterenderer.render(sprite)
        for x in (297,597):
            sprite =self.factory.from_color(CYAN, size=(6, 900))
            sprite.position = x,0
            self.spriterenderer.render(sprite)
        for y in (0,897):
            sprite =self.factory.from_color(CYAN, size=(900, 3))
            sprite.position = 0,y
            self.spriterenderer.render(sprite)
        for y in (297,597):
            sprite =self.factory.from_color(CYAN, size=(900, 6))
            sprite.position = 0,y
            self.spriterenderer.render(sprite)
        
        for x in range(9):
            for y in range(9):
                self.Sudoku.updateBlocks(self.factory.from_color(GREY, size=(90, 90)), x, y)
                surface = sdl2.sdlttf.TTF_RenderText_Solid(self.font, " ", BLACK)
                self.Sudoku.updateDigits(self.factory.from_surface(surface.contents, True), x*10+y, False, 0)
                self.spriterenderer.render(self.Sudoku.block[x*10+y])
                self.spriterenderer.render(self.Sudoku.digit[x*10+y])
        
        # Solver Button Setup
        self.Sudoku.updateGrid(self.factory.from_color(sdl2.ext.Color(0, 255, 255), size=(200, 50)), 350, 925)
        self.spriterenderer.render(self.Sudoku.grid[350925])
        Font = sdl2.sdlttf.TTF_OpenFont(RESOURCES.get_path("GillSans-SemiBold.ttf"),40)
        surface = sdl2.sdlttf.TTF_RenderText_Solid(Font, "Solve It!", BLACK)
        self.Sudoku.Character = self.factory.from_surface(surface.contents, True)
        self.Sudoku.Character.position = (380,925)
        self.spriterenderer.render(self.Sudoku.Character)
        
        # Reset Button        
        self.Sudoku.updateGrid(self.factory.from_color(sdl2.ext.Color(50, 155, 255), size=(200, 50)), 650, 925)
        self.spriterenderer.render(self.Sudoku.grid[650925])
        surface = sdl2.sdlttf.TTF_RenderText_Solid(Font, "Reset", BLACK)
        self.Sudoku.Character = self.factory.from_surface(surface.contents, True)
        self.Sudoku.Character.position = (700,925)
        self.spriterenderer.render(self.Sudoku.Character)
        sdl2.sdlttf.TTF_CloseFont(Font)
        
    def RenderBlocks(self):
        self.spriterenderer.render(self.Sudoku.block[self.Sudoku.chosen])
        self.spriterenderer.render(self.Sudoku.digit[self.Sudoku.chosen])
        
    def Quit(self):
        self.running = False
        
    def DigitReset(self):
        self.reset = True
        
    def KeyEnter(self):
        if self.Sudoku.selected and (self.reset or not self.Sudoku.input[self.Sudoku.chosen]["State"]):
            surface = sdl2.sdlttf.TTF_RenderText_Solid(self.font,str(self.digit),BLACK)
            self.Sudoku.updateDigits(self.factory.from_surface(surface.contents, True),self.Sudoku.chosen, True, self.digit)
            self.RenderBlocks()
            self.reset = False
    
    def MouseAction(self,event):
        if self.Sudoku.selected:
            sdl2.ext.fill(self.Sudoku.block[self.Sudoku.chosen].surface, GREY)
            self.Sudoku.selected = False
            self.RenderBlocks()
        if np.floor(event.x/100) < 9 and np.floor(event.y/100) < 9:
            sdl2.ext.fill(self.Sudoku.block[np.floor(event.x/100)*10+np.floor(event.y/100)].surface, GREEN)
            self.Sudoku.selected = True
            self.Sudoku.chosen = np.floor(event.x/100)*10+np.floor(event.y/100)
            self.RenderBlocks()
        if event.x > 350 and event.x < 550 and event.y > 925 and event.y < 975:
            self.SolveIt()
        elif event.x > 650 and event.x < 850 and event.y > 925 and event.y < 975:
            self.ResetProgram()
    
    def SolveIt(self):
        start = time.time()*1000
        solver = SudokuSolver(self.Sudoku.matrix)
        cycles = 0
        while solver.toSolve > 0:
            ForceFound,Solution = solver.BruteForceSearch()
            for i in range(ForceFound):
                self.Sudoku.chosen = Solution[i]["pos"]
                surface = sdl2.sdlttf.TTF_RenderText_Solid(self.font,str(Solution[i]["digit"]),RED)
                self.Sudoku.updateDigits(self.factory.from_surface(surface.contents, True),self.Sudoku.chosen, True, self.digit)
                self.RenderBlocks()
                
            EliminationFound,Solution = solver.EliminationSearch()
            for i in range(EliminationFound):
                self.Sudoku.chosen = Solution[i]["pos"]
                surface = sdl2.sdlttf.TTF_RenderText_Solid(self.font,str(Solution[i]["digit"]),RED)
                self.Sudoku.updateDigits(self.factory.from_surface(surface.contents, True),self.Sudoku.chosen, True, self.digit)
                self.RenderBlocks()
                
            solver.toSolve -= (ForceFound+EliminationFound)
            cycles += 1
            if ForceFound == 0 and EliminationFound == 0 and solver.toSolve > 0:
                print "Unable to Complete Puzzle"        
                break
            
        if solver.toSolve == 0:
            print "Found All"
        
        end = time.time()*1000
        print "Time Consumed: " + str(end-start) + " milliseconds"
        print "Calculation Cycles: " + str(cycles) + " times"
            
    def ResetProgram(self):
        self.Sudoku.reset()
        self.buildBackground()
        
    def NoAction(self):
        pass

def main():
    Prog = SudokuGUI()
    
    event = sdl2.SDL_Event()
    while Prog.running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_Quit:
                print "Something"
                Prog.Quit()
                break
            if event.type == sdl2.SDL_KEYDOWN:
                Prog.digit = event.key.keysym.scancode - 88
                Prog.KeyAction[event.key.keysym.scancode]()
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                Prog.MouseAction(event.button)
                
    return 0

if __name__ == "__main__":
    sys.exit(main())
