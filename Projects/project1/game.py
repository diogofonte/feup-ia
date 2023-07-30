#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import time
from copy import deepcopy
import random
import math
import numpy as np
import heapq # we'll be using a heap to store the states
import signal
import tracemalloc


def handler(signum, frame):
    raise TimeoutError("Timeout")

signal.signal(signal.SIGALRM, handler)


class Game:
    def __init__(self):


        self.state = State()
        self.availableLevels= ["lvl0", "lvl1","lvl2","lvl3","lvl4","lvl5","lvl6","lvl7","lvl8","lvl9","lvl10",]

        

        pygame.init()
        self.screen_width = 1180
        self.screen_height = 920
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = False
        self.menuState = True
        self.chooseLevelState = False
        self.chooseModeState = False
        self.chooseAlgoState = False
        self.endScreen = False
        self.i = None
        self.j = None
        self.selected_block_offset = None
        self.moving = False
        self.blockMoves = None
        self.showingHint = False
        self.hintOption = False
        self.visitedHint = []
        self.font = pygame.font.SysFont(None, 24)



        red = pygame.image.load("blocks/redB.png")
        DEFAULT_IMAGE_SIZE = (200, 200)
        red = pygame.transform.scale(red, DEFAULT_IMAGE_SIZE)

        blue = pygame.image.load("blocks/blueB.png")
        DEFAULT_IMAGE_SIZE = (100,200)
        blue = pygame.transform.scale(blue, DEFAULT_IMAGE_SIZE)

        yellow = pygame.image.load("blocks/yellowB.png")
        DEFAULT_IMAGE_SIZE = (100,100)
        yellow = pygame.transform.scale(yellow, DEFAULT_IMAGE_SIZE)


        self.photos = [red,blue,yellow]

        
        self.background = pygame.image.load("img/background.png")
        self.whiteBoard = pygame.image.load("img/whiteBoard.png")
        self.button_size = (250, 100)
        self.button_spacing = 20
        self.button_y = (self.screen_height // 2 - self.button_size[1] // 2) - 50
        self.selectedButton = 0
        self.buttons = [
            ("PLAY", self.screen_width // 2 - self.button_size[0] // 2, self.button_y),
            ("HELP", self.screen_width // 2 - self.button_size[0] // 2, self.button_y + self.button_size[1] + self.button_spacing),
            ("QUIT", self.screen_width // 2 - self.button_size[0] // 2, self.button_y + 2 * (self.button_size[1] + self.button_spacing))
        ]
        self.buttons2 = [
            ("PLAYER MODE", self.screen_width // 2 - self.button_size[0] // 2, self.button_y),
            ("PC MODE", self.screen_width // 2 - self.button_size[0] // 2, self.button_y + self.button_size[1] + self.button_spacing),
            ("BACK TO MENU", self.screen_width // 2 - self.button_size[0] // 2, self.button_y + 2 * (self.button_size[1] + self.button_spacing))
        ]
        self.buttons3 = [
            ("BFS", self.screen_width // 2 - self.button_size[0] // 2, self.button_y - 200),
            ("DFS", self.screen_width // 2 - self.button_size[0] // 2, self.button_y - 200 + self.button_size[1] + self.button_spacing),
            ("IFS", self.screen_width // 2 - self.button_size[0] // 2, self.button_y - 200 + 2 * (self.button_size[1] + self.button_spacing)),
            ("GREEDY", self.screen_width // 2 - self.button_size[0] // 2, self.button_y - 200 + 3 * (self.button_size[1] + self.button_spacing)),
            ("A STAR", self.screen_width // 2 - self.button_size[0] // 2, self.button_y - 200 + 4 * (self.button_size[1] + self.button_spacing)),
            ("BACK", self.screen_width // 2 - self.button_size[0] // 2, self.button_y - 200 + 5 * (self.button_size[1] + self.button_spacing))
        ]
        self.buttons4 = [
            ("LVL0", self.screen_width // 6 , self.button_y - 200),
            ("LVL1", self.screen_width // 6 , self.button_y - 200 + self.button_size[1] + self.button_spacing),
            ("LVL2", self.screen_width // 6 , self.button_y - 200 + 2 * (self.button_size[1] + self.button_spacing)),
            ("LVL3", self.screen_width // 6 , self.button_y - 200 + 3 * (self.button_size[1] + self.button_spacing)),
            ("LVL4", self.screen_width // 6 + (self.button_size[0] + self.button_spacing), self.button_y - 200),
            ("LVL5", self.screen_width // 6 + (self.button_size[0] + self.button_spacing) , self.button_y - 200 + (self.button_size[1] + self.button_spacing)),
            ("LVL6", self.screen_width // 6 + (self.button_size[0] + self.button_spacing) , self.button_y - 200 + 2 * (self.button_size[1] + self.button_spacing)),
            ("LVL7", self.screen_width // 6 + (self.button_size[0] + self.button_spacing) , self.button_y - 200 + 3 * (self.button_size[1] + self.button_spacing)),
            ("LVL8", self.screen_width // 6 + 2 * (self.button_size[0] + self.button_spacing), self.button_y - 200),
            ("LVL9", self.screen_width // 6 + 2 * (self.button_size[0] + self.button_spacing), self.button_y - 200 + (self.button_size[1] + self.button_spacing)),
            ("LVL10", self.screen_width // 6 + 2 * (self.button_size[0] + self.button_spacing), self.button_y - 200 + 2 * (self.button_size[1] + self.button_spacing)),
            ("RANDOM", self.screen_width // 6 + 2 * (self.button_size[0] + self.button_spacing), self.button_y - 200 + 3 * (self.button_size[1] + self.button_spacing)),
            ("8x8", self.screen_width // 6 + (self.button_size[0] + self.button_spacing), self.button_y - 200 + 4 * (self.button_size[1] + self.button_spacing)),
        ]
        self.menu()
 

    def run(self):
        moves = 0
        oldState =deepcopy(self.state)
        start_time = time.time()
        goal = A_star_search(self.state,h1,h2,allMoves)
        next = getNextState(goal[0])
        self.diff = getDiffArray(self.state.blocks,next.blocks)
        while self.running:
            if goal_piece_state(self.state):
                end_time = time.time()
                totalTime = end_time - start_time
                self.running = False
                self.endScreen = True
                self.showEndScreen(moves,totalTime)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.menuState = True
                    elif event.key == pygame.K_h:  
                        if (self.hintOption):
                            self.showingHint = True
                            self.showHint(self.diff)
                    elif event.key == pygame.K_p:
                        if (self.hintOption):
                            self.hintOption = False
                        else:
                            self.hintOption = True
                            if (self.diff == []):
                                goal = self.hint_aStar(self.state,h1,h2,allMoves)
                                if (goal != None):
                                    next = getNextState(goal[0])
                                    if (next != None):
                                        self.diff = getDiffArray(self.state.blocks,next.blocks) 
                                        self.visitedHint.append(deepcopy(self.state.blocks))
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_h:
                        self.showingHint = False
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a block was clicked
                    for i in range(len(self.state.blocks)):
                        for j in range(len(self.state.blocks[0])):
   
                            if self.state.blocks[i][j] == 1:
                                block_image = self.photos[1]
                                block_rect = block_image.get_rect()
                                block_rect.x = (j + 2.5) * 100
                                block_rect.y = (i + 0.2) * 100
                                if block_rect.collidepoint(event.pos):
                                    
                                    self.i,self.j = i,j
                                    self.selected_block_offset = (event.pos[0], event.pos[1])
                                    self.blockMoves = blockMoves(self.state,self.i,self.j)
                                    break

                            elif (self.state.blocks[i][j] == 2):
                              
                                
                                block_image = self.photos[2]
                                block_rect = block_image.get_rect()
                                block_rect.x = (j + 2.5) * 100
                                block_rect.y = (i + 0.2) * 100
                                if block_rect.collidepoint(event.pos):
                         
                                    self.i,self.j = i,j
                                    self.selected_block_offset = (event.pos[0], event.pos[1])
                                    self.blockMoves = blockMoves(self.state,self.i,self.j)
                                    break

                            elif (self.state.blocks[i][j] == 3 and i+1 < len(self.state.blocks) and j+1 < len(self.state.blocks[i])):
                                if (self.state.blocks[i+1][j+1]==3):
                                    block_image = self.photos[0]
                                    block_rect = block_image.get_rect()
                                    block_rect.x = ((j + 2.5) * 100) 
                                    block_rect.y = (i + 0.2) * 100
    
                                    if block_rect.collidepoint(event.pos):
             
                                        self.i,self.j = self.getRootPos(i,j)
                                        self.selected_block_offset = (event.pos[0] , event.pos[1] )
                                        self.blockMoves = blockMoves(self.state,self.i,self.j)
                                        break
                                    
                                    
                                    
                   
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.i,self.j,self.selected_block_offset,self.moving,self.blockMoves = None, None, None, False, None

                elif event.type == pygame.MOUSEMOTION:
                    # Move the selected block
                    if self.i is not None and not self.moving:
                        self.moving = True
                        x, y = event.pos[0] - self.selected_block_offset[0], event.pos[1] - self.selected_block_offset[1]
                        move = calcOffset(x,y)

                        if (self.moveBlock(self.i,self.j,move)):
                            moves +=1
                            if (self.hintOption):
                                goal = self.hint_aStar(self.state,h1,h2,allMoves)
                                if (goal != None):
                                    next = getNextState(goal[0])
                                    if (next != None):
                                        self.diff = getDiffArray(self.state.blocks,next.blocks) 
                                        self.visitedHint.append(deepcopy(self.state.blocks))
                            else:
                                self.diff = []
                                    
                            self.moving = False
                            
                            
                            
                            
                            

            if not (self.showingHint):
                self.showBoard(moves)
        """self.state = State()"""
        self.state =oldState
        

    
    def menu(self):
        while self.menuState:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menuState = False
                    elif event.key == pygame.K_UP:
                        self.selectedButton = (self.selectedButton - 1) % len(self.buttons)
                    elif event.key == pygame.K_DOWN:
                        self.selectedButton = (self.selectedButton + 1) % len(self.buttons)
                    elif event.key == pygame.K_RETURN:
                        self.handle_button_click(self.buttons[self.selectedButton])

            block_rect = self.background.get_rect()
            block_rect.x = 0
            block_rect.y = 0
            self.screen.blit(self.background,block_rect)
            counter = 0
            for button in self.buttons:
                if (self.selectedButton == counter):
                    self.draw_button(*button,True)
                else:
                    self.draw_button(*button)
                counter +=1
            pygame.display.update()
        
            self.clock.tick(self.fps)

    def chooseLevel(self):
        while self.chooseLevelState:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.chooseLevelState = False
                    elif event.key == pygame.K_UP:
                        self.selectedButton = (self.selectedButton - 1) % len(self.buttons4)
                    elif event.key == pygame.K_DOWN:
                        self.selectedButton = (self.selectedButton + 1) % len(self.buttons4)
                    elif event.key == pygame.K_LEFT:
                        self.selectedButton = (self.selectedButton -4) % len(self.buttons4)
                    elif event.key == pygame.K_RIGHT:
                        self.selectedButton = (self.selectedButton +4) % len(self.buttons4)
                    elif event.key == pygame.K_RETURN:
                        self.handle_button_click(self.buttons4[self.selectedButton])

            block_rect = self.background.get_rect()
            block_rect.x = 0
            block_rect.y = 0
            self.screen.blit(self.background,block_rect)
            counter = 0
            for button in self.buttons4:
                if (self.selectedButton == counter):
                    self.draw_button(*button,True)
                else:
                    self.draw_button(*button)
                counter +=1
            pygame.display.update()
        
            self.clock.tick(self.fps)
    
    def chooseMode(self):
        while self.chooseModeState:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.chooseModeState = False
                    elif event.key == pygame.K_UP:
                        self.selectedButton = (self.selectedButton - 1) % len(self.buttons2)
                    elif event.key == pygame.K_DOWN:
                        self.selectedButton = (self.selectedButton + 1) % len(self.buttons2)
                    elif event.key == pygame.K_RETURN:
                        self.handle_button_click(self.buttons2[self.selectedButton])

            block_rect = self.background.get_rect()
            block_rect.x = 0
            block_rect.y = 0
            self.screen.blit(self.background,block_rect)
            counter = 0
            for button in self.buttons2:
                if (self.selectedButton == counter):
                    self.draw_button(*button,True)
                else:
                    self.draw_button(*button)
                counter +=1
            pygame.display.update()
        
            self.clock.tick(self.fps)

    def chooseAlgo(self):
        while self.chooseAlgoState:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.chooseAlgoState = False
                    elif event.key == pygame.K_UP:
                        self.selectedButton = (self.selectedButton - 1) % len(self.buttons3)
                    elif event.key == pygame.K_DOWN:
                        self.selectedButton = (self.selectedButton + 1) % len(self.buttons3)
                    elif event.key == pygame.K_RETURN:
                        self.handle_button_click(self.buttons3[self.selectedButton])

            block_rect = self.background.get_rect()
            block_rect.x = 0
            block_rect.y = 0
            self.screen.blit(self.background,block_rect)
            counter = 0
            for button in self.buttons3:
                if (self.selectedButton == counter):
                    self.draw_button(*button,True)
                else:
                    self.draw_button(*button)
                counter +=1
            pygame.display.update()
        
            self.clock.tick(self.fps)
            
    
    def showEndScreen(self,moves,time):
        while self.endScreen:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.endScreen = False
                        self.menuState = True
            
            
            
            block_rect = self.background.get_rect()
            block_rect.x = 0
            block_rect.y = 0
            self.screen.blit(self.background,block_rect)
            
            block_rect = self.whiteBoard.get_rect()
            block_rect.x = 160
            block_rect.y = 200
            
            
            self.screen.blit(self.whiteBoard
                             ,block_rect)
            
            self.font = pygame.font.SysFont(None, 96)
            text_surface = self.font.render(f"Press ESC to leave", True, (0, 0, 0))
            self.screen.blit(text_surface, (300, 600))
            
            
            
            text_surface = self.font.render(f"Total Moves: {moves}", True, (0, 0, 0))
            self.screen.blit(text_surface, (350, 300))
            
            time = math.ceil(time)
            
            text_surface = self.font.render(f"Total Time: {time} seconds", True, (0, 0, 0))
            self.screen.blit(text_surface, (280, 400))
            
            points = math.ceil((1/(time + moves)) * 1000)
            
            
            text_surface = self.font.render(f"Total Points: {points}", True, (0, 0, 0))
            self.screen.blit(text_surface, (320, 500))
            
            pygame.display.update()
        
            self.clock.tick(self.fps)
        
        self.font = pygame.font.SysFont(None, 24)
               

    def handle_button_click(self, button):
        if button[0] == "PLAY":
            self.menu = False
            """self.chooseModeState = True"""
            """self.chooseMode()"""
            self.chooseLevelState= True
            self.chooseLevel()
         
        elif button[0] == "HELP":
            print('not')
        elif button[0] == "QUIT":
            self.menuState = False

        elif button[0] == "LVL0":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl0.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "LVL1":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl1.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()

        elif button[0] == "LVL2":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl2.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "LVL3":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl3.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()

        elif button[0] == "LVL4":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl4.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "LVL5":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl5.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "LVL6":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl6.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "LVL7":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl7.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "LVL8":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl8.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()

        elif button[0] == "LVL9":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl9.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "LVL10":
            self.chooseLevelState = False
            self.state.blocks = np.loadtxt("levels/lvl10.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()

        
        elif button[0] == "RANDOM":
            self.chooseLevelState = False
            levelName = random.choice(self.availableLevels)
            self.state.blocks = np.loadtxt("levels/"+ levelName + ".txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "8x8":
            self.chooseLevelState = False
            levelName = random.choice(self.availableLevels)
            self.state.blocks = np.loadtxt("levels/lvl8x8.txt", dtype='i',delimiter=',')
            self.chooseModeState = True
            self.chooseMode()
        
        elif button[0] == "PC MODE":
            self.chooseModeState = False
            self.chooseAlgoState = True
            self.chooseAlgo()

        elif button[0] == "PLAYER MODE":
            self.running = True
            self.run()
        elif button[0] == "BACK TO MENU":
            self.menuState = True
            self.chooseModeState = False
            self.selectedButton = 2
        elif button[0] == "BACK":
            self.chooseModeState = True
            self.chooseAlgoState = False
            self.selectedButton = 2
        
        elif button[0] == "BFS":
            signal.alarm(20)
            oldState = self.state
            try:
                start_time = time.time()
                goal = breadth_first_search(self.state,goal_piece_state,allMoves)
                end_time = time.time()
                totalTime = end_time - start_time
                signal.alarm(0)
                totalMoves = calc_moves(goal[0]) - 1
                self.print_solution(goal[0])
                self.state = oldState
                with open("stats/bfs_stats.txt", "w") as f:
                    # Write values to file separated by semicolons
                    f.write(f"{totalTime};{totalMoves};{goal[1]}")
            except TimeoutError:
                print("Code took too long to execute")
            finally:
                signal.alarm(0)  # Cancel the timer

        elif button[0] == "DFS":
            signal.alarm(20)
            oldState = self.state
            try:
                start_time = time.time()
                goal = depth_first_search(self.state,goal_piece_state,allMoves)
                end_time = time.time()
                totalTime = end_time - start_time
                signal.alarm(0)
               
                totalMoves = calc_moves(goal[0]) - 1
                
                self.print_solution(goal[0])
                self.state = oldState
                with open("stats/dfs_stats.txt", "w") as f:
                    # Write values to file separated by semicolons
                    f.write(f"{totalTime};{totalMoves};{goal[1]}")
            except TimeoutError:
                print("Code took too long to execute")
            finally:
                signal.alarm(0)  # Cancel the timer
            
        elif button[0] == "IFS":
            signal.alarm(20)
            oldState = self.state
            try:
                start_time = time.time()
                goal = iterative_deepening_search(self.state,goal_piece_state,allMoves,20)
                end_time = time.time()
                totalTime = end_time - start_time
                signal.alarm(0)
                totalMoves = calc_moves(goal[0]) - 1
                self.print_solution(goal[0])
                self.state = oldState
                with open("stats/ifs_stats.txt", "w") as f:
                    # Write values to file separated by semicolons
                    f.write(f"{totalTime};{totalMoves};{goal[1]}")
            except TimeoutError:
                print("Code took too long to execute")
            finally:
                signal.alarm(0)  # Cancel the timer                
        
        elif button[0] == "GREEDY":
            oldState = self.state
            signal.alarm(20)
            try:
                start_time = time.time()
                goal = greedy_search(self.state,h1,allMoves)
                end_time = time.time()
                totalTime = end_time - start_time
                signal.alarm(0)
                totalMoves = calc_moves(goal[0]) - 1
                self.print_solution(goal[0])
                self.state = oldState
                with open("stats/greedy_stats.txt", "w") as f:
                    # Write values to file separated by semicolons
                    f.write(f"{totalTime};{totalMoves};{goal[1]}")
            except TimeoutError:
                print("Code took too long to execute")
            finally:
                signal.alarm(0)  # Cancel the timer
                
        elif button[0] == "A STAR":
            oldState= self.state
            signal.alarm(20)
            try:
                start_time = time.time()
                goal = A_star_search(self.state,h1,h2,allMoves)
                end_time = time.time()
                totalTime = end_time - start_time
                signal.alarm(0)
                totalMoves = calc_moves(goal[0]) - 1
                self.print_solution(goal[0])
                self.state = oldState
                with open("stats/a_star_stats.txt", "w") as f:
                    # Write values to file separated by semicolons
                    f.write(f"{totalTime};{totalMoves};{goal[1]}")
            except TimeoutError:
                print("Code took too long to execute")
            finally:
                signal.alarm(0)  # Cancel the timer


    def draw_button(self, text, x, y, selected=False):
        button_surface = pygame.Surface(self.button_size, pygame.SRCALPHA)
        transparency = 128  # 50% transparency
        pygame.draw.ellipse(button_surface, (0, 0, 0, transparency), button_surface.get_rect())

        text_surface = self.font.render(text, True, (255, 255, 255))
        text_x = self.button_size[0] // 2 - text_surface.get_width() // 2
        text_y = self.button_size[1] // 2 - text_surface.get_height() // 2

        button_surface.blit(text_surface, (text_x, text_y))

        if selected:
            pygame.draw.ellipse(button_surface, (255, 255, 255), button_surface.get_rect(), width=4)

        self.screen.blit(button_surface, (x, y))


    def showBoard(self,moves):
        self.screen.fill((255, 255, 255))
            
        text_surface = self.font.render(f"nº moves: {moves}", True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        text_surface = self.font.render(f"Press ESC to leave", True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 40))
        if (self.hintOption):
            text_surface = self.font.render(f"Press h for hint", True, (0, 0, 0))
            self.screen.blit(text_surface, (10, 70))
        else:
            text_surface = self.font.render(f"Press p to activate hints (lag)", True, (0, 0, 0))
            self.screen.blit(text_surface, (10, 70))
 
        for i in range(len(self.state.blocks)):
            for j in range(len(self.state.blocks[i])):
                if self.state.blocks[i][j] == 1 and i+1 < len(self.state.blocks):
                    if (self.state.blocks[i+1][j]==1):
                        if (i-1 < 0):
                            block_image = self.photos[1]
                            block_rect = block_image.get_rect()
                            block_rect.x = (j + 2.5) * 100
                            block_rect.y = (i + 0.2) * 100
                            self.screen.blit(block_image, block_rect)
                        elif (self.state.blocks[i-1][j] != 1):
                            block_image = self.photos[1]
                            block_rect = block_image.get_rect()
                            block_rect.x = (j + 2.5) * 100
                            block_rect.y = (i + 0.2) * 100
                            self.screen.blit(block_image, block_rect)
                        else:
                            if (i+2 < len(self.state.blocks)):
                                if (self.state.blocks[i-1][j] == 1 and self.state.blocks[i+2][j] != 1):
                                    block_image = self.photos[1]
                                    block_rect = block_image.get_rect()
                                    block_rect.x = (j + 2.5) * 100
                                    block_rect.y = (i + 0.2) * 100
                                    self.screen.blit(block_image, block_rect)
                            elif(self.state.blocks[i-1][j] == 1):
                                if (i+2 == len(self.state.blocks) and self.state.blocks[i+1][j] == 1):
                                    block_image = self.photos[1]
                                    block_rect = block_image.get_rect()
                                    block_rect.x = (j + 2.5) * 100
                                    block_rect.y = (i + 0.2) * 100
                                    self.screen.blit(block_image, block_rect)
        
                elif (self.state.blocks[i][j] == 2):
                    block_image = self.photos[2]
                    block_rect = block_image.get_rect()
                    block_rect.x = (j + 2.5) * 100
                    block_rect.y = (i + 0.2) * 100
                    self.screen.blit(block_image, block_rect)
                    
                elif (self.state.blocks[i][j] == 3 and i+1 < len(self.state.blocks) and j+1 < len(self.state.blocks[i])):
                    if (self.state.blocks[i+1][j+1]==3):
                        block_image = self.photos[0]
                        block_rect = block_image.get_rect()
                        block_rect.x = (j+ 2.5) * 100
                        block_rect.y = (i + 0.2) * 100
                        self.screen.blit(block_image, block_rect)
         
        pygame.display.update()
        
        self.clock.tick(self.fps)
        
    
    def showHint(self,hint):
         for i in range(len(self.state.blocks)):
            for j in range(len(self.state.blocks[i])):
                if hint[i][j] == 1 and i+1 < len(self.state.blocks):
                    if (hint[i+1][j]==1):
                        if (i-1 < 0):
                            block_image = self.photos[1]
                            block_rect = block_image.get_rect()
                            block_rect.x = (j + 2.5) * 100
                            block_rect.y = (i + 0.2) * 100
                            self.screen.blit(block_image, block_rect)
                        elif (hint[i-1][j] != 1):
                           
                            block_image = self.photos[1]
                            block_rect = block_image.get_rect()
                            block_rect.x = (j + 2.5) * 100
                            block_rect.y = (i+ 0.2) * 100
                            self.screen.blit(block_image, block_rect)
                        else:
                            if (i+2 < len(self.state.blocks)):
                                if (hint[i-1][j] == 1 and hint[i+2][j] != 1):
                                    block_image = self.photos[1]
                                    block_rect = block_image.get_rect()
                                    block_rect.x = (j + 2.5) * 100
                                    block_rect.y = (i + 0.2) * 100
                                    self.screen.blit(block_image, block_rect)
        
                elif (hint[i][j] == 2):
                    block_image = self.photos[2]
                    block_rect = block_image.get_rect()
                    block_rect.x = (j + 2.5) * 100
                    block_rect.y = (i + 0.2) * 100
                    self.screen.blit(block_image, block_rect)
                    
                elif (hint[i][j] == 3 and i+1 < len(self.state.blocks) and j+1 < len(self.state.blocks[i])):
                    if (hint[i+1][j+1]==3):
                        block_image = self.photos[0]
                        block_rect = block_image.get_rect()
                        block_rect.x = (j + 2.5) * 100
                        block_rect.y = (i + 0.2) * 100
                        self.screen.blit(block_image, block_rect)
                        
                elif (hint[i][j] == 4):
                    square_size = (170, 170)
                    square_surface = pygame.Surface(square_size)
                    square_surface.fill((255, 255, 255))  # Set the color to white
                    square_pos = ((j + 2.5) * 100, (i + 0.2) * 100)
                    self.screen.blit(square_surface, square_pos)
        
         pygame.display.update()
         
         self.clock.tick(self.fps)


    def getRootPos(self,i,j):
        if (i - 1 >=0):
            if (self.state.blocks[i-1][j] == 3):
                if (j + 1 < len(self.state.blocks[i])):
                    if (self.state.blocks[i][j+1] == 3):
                        i-=1
                    else:
                        i-=1
                        j-=1
                else:
                    if (self.state.blocks[i][j-1] == 3):
                        i-=1
                        j-=1
        else:
            if (j + 1 < len(self.state.blocks[i])):
                if (self.state.blocks[i][j+1] != 3):
                    j-=1
            else:
                if (self.state.blocks[i][j-1] == 3):
                    j-=1

        return (i,j)
    

    def moveBlock(self,i,j,move):
        if (move in self.blockMoves):
            if self.state.blocks[i][j] == 1 and i + 1 < len(self.state.blocks): #blue
                if (self.state.blocks[i+1][j]==1):
                    if (i+2 < len(self.state.blocks)):
                        if (self.state.blocks[i+2][j] == 0 and move=='down'): #down
                            self.state.blocks[i][j] = 0
                            self.state.blocks[i+2][j] = 1
                            return True

                    if (i-1 >= 0):
                        if (self.state.blocks[i-1][j] == 0 and move == 'up'): #up
                            self.state.blocks[i+1][j] = 0
                            self.state.blocks[i-1][j] = 1
                            return True
      
                    if (j+1 < len(self.state.blocks[i])):
                        if (self.state.blocks[i][j+1] == 0 and self.state.blocks[i+1][j+1] == 0 and move =='right'): #right
                            self.state.blocks[i][j] = 0
                            self.state.blocks[i+1][j] = 0
                            self.state.blocks[i][j+1] = 1
                            self.state.blocks[i+1][j+1] = 1
                            return True

                    if (j-1 >= 0):
                        if (self.state.blocks[i][j-1] == 0 and self.state.blocks[i+1][j-1] == 0) and move =='left': #left
                            self.state.blocks[i][j] = 0
                            self.state.blocks[i+1][j] = 0
                            self.state.blocks[i][j-1] = 1
                            self.state.blocks[i+1][j-1] = 1
                            return True    
                            
            elif (self.state.blocks[i][j] == 2): #yellow
                if (i+1 < len(self.state.blocks)):
                    if (self.state.blocks[i+1][j] == 0 and move =='down'): #down

                        self.state.blocks[i][j] = 0
                        self.state.blocks[i+1][j] = 2
                        return True

                if (i-1 >= 0):
                    if (self.state.blocks[i-1][j] == 0 and move == 'up'): #up

                        self.state.blocks[i][j] = 0
                        self.state.blocks[i-1][j] = 2
                        return True

                if (j+1 < len(self.state.blocks[i])):
                    if (self.state.blocks[i][j+1] == 0 and move =='right'): #right
  
                        self.state.blocks[i][j] = 0
                        self.state.blocks[i][j+1] = 2
                        return True

                if (j-1 >= 0):
                    if (self.state.blocks[i][j-1] == 0 and move =='left'): #left

                        self.state.blocks[i][j] = 0
                        self.state.blocks[i][j-1] = 2
                        return True
                
            elif (self.state.blocks[i][j] == 3 and i+1 < len(self.state.blocks) and j+1 < len(self.state.blocks[i])): #red
                if (self.state.blocks[i+1][j+1]==3):
                    if (i+2 < len(self.state.blocks)):
                        if (self.state.blocks[i+2][j] == 0 and self.state.blocks[i+2][j+1] == 0 and move=='down'): #down

                            self.state.blocks[i][j] = 0
                            self.state.blocks[i][j+1] = 0
                            self.state.blocks[i+2][j] = 3
                            self.state.blocks[i+2][j+1] = 3
                            return True
    
                    if (i-1 >= 0):
                        if (self.state.blocks[i-1][j] == 0 and self.state.blocks[i-1][j+1] == 0 and move =='up'): #up

                            self.state.blocks[i+1][j] = 0
                            self.state.blocks[i+1][j+1] = 0
                            self.state.blocks[i-1][j] = 3
                            self.state.blocks[i-1][j+1] = 3
                            return True

                    if (j+2 < len(self.state.blocks[i])):
                        if (self.state.blocks[i][j+2] == 0 and self.state.blocks[i+1][j+2] == 0 and move =='right'): #right

                            self.state.blocks[i][j] = 0
                            self.state.blocks[i+1][j] = 0
                            self.state.blocks[i][j+2] = 3
                            self.state.blocks[i+1][j+2] = 3
                            return True
                      
                    if (j-1 >= 0):
                        if (self.state.blocks[i][j-1] == 0 and self.state.blocks[i+1][j-1] == 0 and move =='left'): #left
          
                            self.state.blocks[i][j+1] = 0
                            self.state.blocks[i+1][j+1] = 0
                            self.state.blocks[i][j-1] = 3
                            self.state.blocks[i+1][j-1] = 3
                            return True
        else:
            return False         

    
    def hint_aStar(self,problem, h1, h2, operators_func):
    
        root = TreeNode(problem)
        g_score = {tuple(root.state.blocks.flatten()): 0}
        f_score = {tuple(root.state.blocks.flatten()): h1(root.state) + h2(root.state)}
    
        setattr(TreeNode, "__lt__", lambda self, other: f_score[tuple(self.state.blocks.flatten())] < f_score[tuple(other.state.blocks.flatten())])
    
        states = [root]
        visited = []
        tracemalloc.start()
        while states:
            node = heapq.heappop(states)
            visited.append(node.state.blocks)
    
            if goal_piece_state(node.state):
                peak_memory = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
                return (node, peak_memory)
    
            for child_state in operators_func(node.state):
                if any(np.array_equal(child_state.blocks, visited_state) for visited_state in visited):
                    continue
                
                if any(np.array_equal(child_state.blocks, arr) for arr in self.visitedHint):
                    continue
    
                tentative_g_score = g_score[tuple(node.state.blocks.flatten())] + 1  # cost of moving to child is always 1
    
                if tuple(child_state.blocks.flatten()) not in g_score or tentative_g_score < g_score[tuple(child_state.blocks.flatten())]:
                    g_score[tuple(child_state.blocks.flatten())] = tentative_g_score
                    f_score[tuple(child_state.blocks.flatten())] = h1(child_state) + h2(child_state)
    
                    child = TreeNode(child_state, node)
                    node.add_child(child)
    
                    if not any(np.array_equal(child_state.blocks, visited_state) for visited_state in visited):
                        heapq.heappush(states, child)
                    
                    
    
        return None 
            
    
    def print_solution_aux(self,node,lst):
        if (node.parent != None):
            lst.append(node)
            print_solution_aux(node.parent,lst)
            return True
        else:
            lst.append(node)
            return True

    def print_solution(self,node):
        l= []
        print_solution_aux(node,l),
        l.reverse()

        moves = 0
        for n in l:
            self.state = n.state
            self.showBoard(moves)
            time.sleep(1)
            moves += 1
        return True
    

def calc_moves_aux(node,lst):
    if (node.parent != None):
        lst.append(node)
        calc_moves_aux(node.parent,lst)
        return True
    else:
        lst.append(node)
        return True

def calc_moves(node):
    l= []
    calc_moves_aux(node,l)
    return len(l)



def calcOffset(x,y):
    if (y > 0 and abs(y) > abs(x)):
        return 'down'
    elif (y < 0 and abs(y) > abs(x)):
        return 'up'
    elif (x > 0 and abs(x) > abs(y)):
        return 'right'
    elif (x < 0 and abs(x) > abs(y)):
        return 'left'          
          
class State:
    def __init__(self):

        
        self.blocks = np.loadtxt("levels/lvl0.txt", dtype='i',delimiter=',')
        
        
 
        """
        self.blocks = np.array([[1,1,1,1],
                                [1,1,1,1],
                                [0,1,3,3],
                                [0,1,3,3],
                                [2,2,2,2]])
                    
        
        """
        
        """
        self.blocks = np.array([[0,0,0,0],
                                [0,0,0,0],
                                [0,0,3,3],
                                [0,0,3,3],
                                [0,0,0,0]])
        """
    
    def changeLevel(self,levelName):
        self.state.blocks = np.loadtxt("levels/lvl1.txt", dtype='i',delimiter=',')
    

def printMoves(states):
    for state in states:
        print(state.blocks)
    
def goal_piece_state(state):
    
    row = state.blocks.shape[0]
    col = state.blocks.shape[1]
    row = row -1
    col = int(math.ceil(col/2)) -1
    
    return state.blocks[row-1][col] == 3 and state.blocks[row,col+1] == 3
    #print(row-1,col)
    #print(row,col+1)
    #return state.blocks[3][1] == 3 and state.blocks[4,2] == 3
    
    
def allMoves(state):
    
    new_states = []
    
    for i in range(len(state.blocks)):
        for j in range(len(state.blocks[i])):
            if state.blocks[i][j] == 1 and i + 1 < len(state.blocks): #blue
                if (state.blocks[i+1][j]==1):
                    if (i+2 < len(state.blocks)):
                        if (state.blocks[i+2][j] == 0): #down
                            temp = deepcopy(state.blocks)
                            temp[i][j] = 0
                            temp[i+2][j] = 1
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
                    if (i-1 >= 0):
                        if (state.blocks[i-1][j] == 0): #up
                            temp = deepcopy(state.blocks)
                            temp[i+1][j] = 0
                            temp[i-1][j] = 1
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
                    if (j+1 < len(state.blocks[i])):
                        if (state.blocks[i][j+1] == 0 and state.blocks[i+1][j+1] == 0): #right
                            temp = deepcopy(state.blocks)
                            temp[i][j] = 0
                            temp[i+1][j] = 0
                            temp[i][j+1] = 1
                            temp[i+1][j+1] = 1
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
                    if (j-1 >= 0):
                        if (state.blocks[i][j-1] == 0 and state.blocks[i+1][j-1] == 0): #left
                            temp = deepcopy(state.blocks)
                            temp[i][j] = 0
                            temp[i+1][j] = 0
                            temp[i][j-1] = 1
                            temp[i+1][j-1] = 1
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
                                         
            elif (state.blocks[i][j] == 2): #yellow
                if (i+1 < len(state.blocks)):
                    if (state.blocks[i+1][j] == 0): #down
                        temp = deepcopy(state.blocks)
                        temp[i][j] = 0
                        temp[i+1][j] = 2
                        tempS = State()
                        tempS.blocks = temp
                        new_states.append(tempS)
                if (i-1 >= 0):
                    if (state.blocks[i-1][j] == 0): #up
                        temp = deepcopy(state.blocks)
                        temp[i][j] = 0
                        temp[i-1][j] = 2
                        tempS = State()
                        tempS.blocks = temp
                        new_states.append(tempS)
                if (j+1 < len(state.blocks[i])):
                    if (state.blocks[i][j+1] == 0): #right
                        temp = deepcopy(state.blocks)
                        temp[i][j] = 0
                        temp[i][j+1] = 2
                        tempS = State()
                        tempS.blocks = temp
                        new_states.append(tempS)
                if (j-1 >= 0):
                    if (state.blocks[i][j-1] == 0): #left
                        temp = deepcopy(state.blocks)
                        temp[i][j] = 0
                        temp[i][j-1] = 2
                        tempS = State()
                        tempS.blocks = temp
                        new_states.append(tempS) 
                
            elif (state.blocks[i][j] == 3 and i+1 < len(state.blocks) and j+1 < len(state.blocks[i])): #red
                if (state.blocks[i+1][j+1]==3):
                    if (i+2 < len(state.blocks)):
                        if (state.blocks[i+2][j] == 0 and state.blocks[i+2][j+1] == 0): #down
                            temp = deepcopy(state.blocks)
                            temp[i][j] = 0
                            temp[i][j+1] = 0
                            temp[i+2][j] = 3
                            temp[i+2][j+1] = 3
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
                    if (i-1 >= 0):
                        if (state.blocks[i-1][j] == 0 and state.blocks[i-1][j+1] == 0): #up
                            temp = deepcopy(state.blocks)
                            temp[i+1][j] = 0
                            temp[i+1][j+1] = 0
                            temp[i-1][j] = 3
                            temp[i-1][j+1] = 3
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
                    if (j+2 < len(state.blocks[i])):
                        if (state.blocks[i][j+2] == 0 and state.blocks[i+1][j+2] == 0): #right
                            temp = deepcopy(state.blocks)
                            temp[i][j] = 0
                            temp[i+1][j] = 0
                            temp[i][j+2] = 3
                            temp[i+1][j+2] = 3
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
                    if (j-1 >= 0):
                        if (state.blocks[i][j-1] == 0 and state.blocks[i+1][j-1] == 0): #left
                            temp = deepcopy(state.blocks)
                            temp[i][j+1] = 0
                            temp[i+1][j+1] = 0
                            temp[i][j-1] = 3
                            temp[i+1][j-1] = 3
                            tempS = State()
                            tempS.blocks = temp
                            new_states.append(tempS)
           
    return new_states


def blockMoves(state,i,j):
    
    moves = []

    if state.blocks[i][j] == 1 and i + 1 < len(state.blocks): #blue
        if (state.blocks[i+1][j]==1):
            if (i+2 < len(state.blocks)):
                if (state.blocks[i+2][j] == 0): #down
                    moves.append("down")

            if (i-1 >= 0):
                if (state.blocks[i-1][j] == 0): #up
                    moves.append("up")

            if (j+1 < len(state.blocks[i])):
                if (state.blocks[i][j+1] == 0 and state.blocks[i+1][j+1] == 0): #right
                    moves.append("right")

            if (j-1 >= 0):
                if (state.blocks[i][j-1] == 0 and state.blocks[i+1][j-1] == 0): #left
                    moves.append("left")
                       
    elif (state.blocks[i][j] == 2): #yellow
        if (i+1 < len(state.blocks)):
            if (state.blocks[i+1][j] == 0): #down
                moves.append("down")

        if (i-1 >= 0):
            if (state.blocks[i-1][j] == 0): #up
                moves.append("up")

        if (j+1 < len(state.blocks[i])):
            if (state.blocks[i][j+1] == 0): #right
                moves.append("right")

        if (j-1 >= 0):
            if (state.blocks[i][j-1] == 0): #left
                moves.append("left") 
        
    elif (state.blocks[i][j] == 3 and i+1 < len(state.blocks) and j+1 < len(state.blocks[i])): #red
        if (state.blocks[i+1][j+1]==3):
            if (i+2 < len(state.blocks)):
                if (state.blocks[i+2][j] == 0 and state.blocks[i+2][j+1] == 0): #down
                    moves.append("down")

            if (i-1 >= 0):
                if (state.blocks[i-1][j] == 0 and state.blocks[i-1][j+1] == 0): #up
                    moves.append("up")

            if (j+2 < len(state.blocks[i])):
                if (state.blocks[i][j+2] == 0 and state.blocks[i+1][j+2] == 0): #right
                    moves.append("right")

            if (j-1 >= 0):
                if (state.blocks[i][j-1] == 0 and state.blocks[i+1][j-1] == 0): #left
                    moves.append("left")
    
    return moves


# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        
        
        
from collections import deque

def breadth_first_search(initial_state, goal_state_func, operators_func):
    
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    tracemalloc.start()
    visited =  []  # keep track of visited nodes
    while queue:
        node = queue.popleft()   # get first element in the queue
        visited.append(node.state.blocks)  # mark the node as visited
        if goal_state_func(node.state):   # check goal 
            peak_memory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            return (node, peak_memory)
        
        
        for state in operators_func(node.state):   # go through next states
            if not any(np.array_equal(state.blocks, arr) for arr in visited):
            # create tree node with the new state
                tempNode = TreeNode(state,node)
            
            # link child node to its parent in the tree
            
                node.add_child(tempNode)
            
            # your code here
            
            # enqueue the child node
            
                queue.append(tempNode)
            
    
    print('failed')
    return None



def depth_first_search(initial_state, goal_state_func, operators_func):
    
    root = TreeNode(initial_state)   # create the root node in the search tree
    stack = [root]  # initialize the queue to store the nodes
    visited =  []  # keep track of visited nodes
    tracemalloc.start()
    while stack:
        node = stack.pop()   # get the last element in the stack
        visited.append(node.state.blocks)  # mark the node as visited
        if goal_state_func(node.state):   # check goal state
            peak_memory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            return (node, peak_memory)
        for state in operators_func(node.state):   # go through next states
            if not any(np.array_equal(state.blocks, arr) for arr in visited):
                # create tree node with the new state
                tempNode = TreeNode(state, node)
                # link child node to its parent in the tree
                node.add_child(tempNode)
                # enqueue the child node
                stack.append(tempNode)
    return None


def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit):
    
    for depth in range(depth_limit + 1):
        root = TreeNode(initial_state)   # create the root node in the search tree
        stack = [(root, 0)]   # initialize the stack to store the nodes and their depths
        visited = []  # keep track of visited nodes
        tracemalloc.start()
        while stack:
            node, node_depth = stack.pop()   # get the last element in the stack
            visited.append(node.state.blocks)  # mark the node as visited
            if goal_state_func(node.state):   # check goal state
                peak_memory = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
                return (node, peak_memory)
            if node_depth < depth:  # explore nodes within the depth limit
                for state in operators_func(node.state):   # go through next states
                    if not any(np.array_equal(state.blocks, arr) for arr in visited):
                        # create tree node with the new state
                        tempNode = TreeNode(state, node)
                        # link child node to its parent in the tree
                        node.add_child(tempNode)
                        # enqueue the child node
                        stack.append((tempNode, node_depth + 1))
    return None






def greedy_search(problem, heuristic, operators_func):
    
    # heuristic (function) - the heuristic function that takes a board (matrix), and returns an integer
    setattr(TreeNode, "__lt__", lambda self, other: heuristic(self.state) < heuristic(other.state)) 
    root = TreeNode(problem)
    states = [root]
    visited = [] # to not visit the same state twice
    tracemalloc.start()
    while states:
        
        node = heapq.heappop(states)   # get first element in the queue
        visited.append(node.state.blocks)
        


        if goal_piece_state(node.state):   # check goal state
            peak_memory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            return (node, peak_memory)
            
        
      

        for child in operators_func(node.state): # go through next states
            if not any(np.array_equal(child.blocks, arr) for arr in visited):
                tempNode = TreeNode(child, node)
                node.add_child(tempNode)
        

                heapq.heappush(states,tempNode)
            
        
    return None


def A_star_search(problem, h1, h2, operators_func):
    
    root = TreeNode(problem)
    g_score = {tuple(root.state.blocks.flatten()): 0}
    f_score = {tuple(root.state.blocks.flatten()): h1(root.state) + h2(root.state)}

    setattr(TreeNode, "__lt__", lambda self, other: f_score[tuple(self.state.blocks.flatten())] < f_score[tuple(other.state.blocks.flatten())])

    states = [root]
    visited = []
    tracemalloc.start()
    while states:
        node = heapq.heappop(states)
        visited.append(node.state.blocks)

        if goal_piece_state(node.state):
            peak_memory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            return (node, peak_memory)

        for child_state in operators_func(node.state):
            if any(np.array_equal(child_state.blocks, visited_state) for visited_state in visited):
                continue

            tentative_g_score = g_score[tuple(node.state.blocks.flatten())] + 1  # cost of moving to child is always 1

            if tuple(child_state.blocks.flatten()) not in g_score or tentative_g_score < g_score[tuple(child_state.blocks.flatten())]:
                g_score[tuple(child_state.blocks.flatten())] = tentative_g_score
                f_score[tuple(child_state.blocks.flatten())] = h1(child_state) + h2(child_state)

                child = TreeNode(child_state, node)
                node.add_child(child)

                if not any(np.array_equal(child_state.blocks, visited_state) for visited_state in visited):
                    heapq.heappush(states, child)

    return None 





def h1(state): #number of pieces in front
    # heuristic function 1
    # returns the number of pieces between the red block and the goal position
    board = state.blocks
    side = len(board) # the size of the side of the board (only for square boards)

    #goalX = 1
    #goalY = 3

    goalY = state.blocks.shape[0]
    goalX = state.blocks.shape[1]
    goalY = goalY -1 -1
    goalX = int(math.ceil(goalX/2)) -1

    total = 0
    
    for row in range(side):
            for col in range(len(board[0])):
                if (board[row][col] == 3):
                    if (row + 1 < side and col + 1 < len(board[0])):
                        if (board[row+1][col+1] == 3): 
                            horizontalDistance = goalX - col
                            verticalDistance = goalY - row
                            
                            if (verticalDistance != 0):
                                for i in range(row,goalY):
                                    
                                    if (board[i+2][col] == 2):
                                        total +=1
                                    if (board[i+2][col+1] ==2):
                                        total +=1
                                    elif (board[i+2][col] == 1 and board[i+2][col] == 1):
                                        total +=1
                            
                            if (horizontalDistance < 0):
                               
                                for j in range(goalX,col):
                                    if (board[row][j] == 2):
                                        total +=1
                              
                                    if (board[row][j] == 1 and board[row+1][j] == 1):
                                        total +=1

                            elif (horizontalDistance > 0):
                                for j in range(col,goalX):
                                    if (board[row][j+2] == 2):
                                        total +=1
                                    if (board[row+1][j+2] == 2):
                                        total +=1
                                    if (board[row][j+2] == 1 and board[row+1][j+2] == 1):
                                        total +=1

    return total

def h2(state):
    # heuristic function 2
    # returns the sum of manhattan distances from incorrect placed pieces to their correct places
    board = state.blocks
    side = len(board) # the size of the side of the board (only for square boards)

    goalY = state.blocks.shape[0]
    goalX = state.blocks.shape[1]
    goalY = goalY -1 -1
    goalX = int(math.ceil(goalX/2)) -1

  
    
    for row in range(side):
            for col in range(len(board[0])):
                if (board[row][col] == 3):
                    if (row + 1 < side and col + 1 < len(board[0])):
                        if (board[row+1][col+1] == 3): 
                            #distance = abs(3-row) + abs(1-col) # to be changed for different sized boards
                            distance = abs(goalY-row) + abs(goalX-col)
                            break

    return distance

def print_solution_aux(node,lst):
    if (node.parent != None):
        lst.append(node)
        print_solution_aux(node.parent,lst)
        return True
    else:
        lst.append(node)
        return True

def print_solution(node):
    l= []
    print_solution_aux(node,l),
    l.reverse()
  
    for n in l:
        print(n.state.blocks)
    return True



def getNextStateAux(node,result):
    if (node.parent != None):
        if (node.parent.parent == None):
            result.append(node)
            getNextStateAux(node.parent,result)
            return True
        else:
            getNextStateAux(node.parent,result)
            return True
    else:
        return True

def getNextState(node):
    result = []
    getNextStateAux(node,result)
    if (result != []):
        return result[0].state
    else:
        return None
    


def getDiffArray(arr1, arr2):
    result = deepcopy(arr2)
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            if (arr1[i][j] != arr2[i][j]):
                if (arr2[i][j] != 0):
                    result[i][j] = arr2[i][j]
                elif (arr1[i][j] != 0):
                    result[i][j] = 4
    return result
            


game = Game()
pygame.quit()




