import pygame
import numpy as np
import random
import pickle
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.display.set_caption('2048')


class Window:
    def __init__(self) -> None:
        # init height/width of screen:
        self.height = 800
        self.width = 550

        # offset and stuff
        self.size_main_rect = 500
        self.X_offset = 25
        self.Y_offset = 275
        self.size_image = self.Y_offset//5
        
        # init screen:
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # load images:
        self.back_img = pygame.image.load(r'retour.jpg')
        self.back_img = pygame.transform.scale(self.back_img, (self.size_image, self.size_image))
        
        self.restart_img = pygame.image.load(r'recommencer.jpg')
        self.restart_img = pygame.transform.scale(self.restart_img, (self.size_image, self.size_image))

        # init fonts:
        self.font_number = pygame.font.Font(None, int(self.width/13))
        self.font_title = pygame.font.Font(None, int(self.width/4))

        # tiles colors:
        self.colors = [(254, 254, 226), (231, 168, 84), (230, 126, 48), (237, 127, 16), (253, 70, 38), (198, 8, 0),
              (247, 255, 60), (223, 218, 0), (253, 238, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
              (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

    def draw(self, board:np.array, score:int, bestScore:int):
        self.screen.fill([193, 191, 177])

        for y in range(4):
            for x in range(4):
                if board[x, y] != 0:
                    
                    pygame.draw.rect(
                        self.screen, 
                        self.colors[int(np.log2(board[x, y]))-1], 
                            [self.X_offset + x*self.size_main_rect//4, 
                             self.Y_offset + y*self.size_main_rect//4, 
                             self.size_main_rect//4, 
                             self.size_main_rect//4]
                        )
                    
                    # choose color of numbers
                    c = (230, 230, 230)
                    if board[x, y] in (2, 128, 256, 512):
                        c = (0, 0, 0)

                    numberSurface = self.font_number.render(str(board[x, y]), True, c)
                    width = numberSurface.get_width()
                    height = numberSurface.get_height()

                    self.screen.blit(
                        numberSurface,
                        (int(self.X_offset + x*self.size_main_rect//4 + self.size_main_rect//8 - width//2),
                         int(self.Y_offset + y*self.size_main_rect//4 + self.size_main_rect//8 - height//2))
                    )

        # render title
        self.screen.blit(self.font_title.render(str(2048), True, (50, 50, 50)),
                    (min(self.width, self.height)//27, min(self.width, self.height)//27))
        
        # renter score
        self.screen.blit(self.font_number.render('score:', True, (150, 50, 50)),
                    (min(self.width, self.height)//1.5, min(self.width, self.height)//27))
        self.screen.blit(self.font_number.render(str(score), True, (50, 50, 150)),
                    (min(self.width, self.height)//1.5, min(self.width, self.height)//12.3))
        
        # render best score:
        self.screen.blit(self.font_number.render('best score:', True, (150, 50, 50)),
                    (min(self.width, self.height)//1.5, min(self.width, self.height)//7.1))
        self.screen.blit(self.font_number.render(str(bestScore), True, (50, 50, 150)),
                    (min(self.width, self.height)//1.5, min(self.width, self.height)//5.4))

        # render buttons:
        pygame.draw.rect(self.screen, (125, 125, 125), [min(self.width, self.height)//9, min(self.width, self.height)//4, self.size_image+2, self.size_image+2])
        pygame.draw.rect(self.screen, (125, 125, 125), [min(self.width, self.height)//3.4, min(self.width, self.height)//4, self.size_image+2, self.size_image+2])
        
        self.screen.blit(self.back_img, (min(self.width, self.height)//9 +1, min(self.width, self.height)//4 +1))
        self.screen.blit(self.restart_img, (min(self.width, self.height)//3.4 +1, min(self.width, self.height)//4 +1))

        # draw table lines:
        for i in range(5):
            pygame.draw.line(self.screen, (127, 127, 127), 
                             (self.X_offset + i*self.size_main_rect//4, self.Y_offset), 
                             (self.X_offset + i*self.size_main_rect//4, self.Y_offset+self.size_main_rect), 3)
             
            pygame.draw.line(self.screen, (127, 127, 127), 
                             (self.X_offset, self.Y_offset + i*self.size_main_rect//4), 
                             (self.X_offset + self.size_main_rect, self.Y_offset+i*self.size_main_rect//4), 3)
            
        pygame.display.flip()

    def resize_window(self):
        print("hello")
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()

        # offset and stuff
        self.size_main_rect = 500
        self.X_offset = (self.width - self.size_main_rect)//2
        self.Y_offset = 275
        self.size_image = self.Y_offset//5

        # resize image
        self.back_img = pygame.transform.scale(self.back_img, (self.size_image, self.size_image))
        self.restart_img = pygame.transform.scale(self.restart_img, (self.size_image, self.size_image))

        # resize fonts:
        self.font_number = pygame.font.Font(None, int(min(self.width, self.height)/13))
        self.font_title = pygame.font.Font(None, int(min(self.width, self.height)/4))


class Game:
    def __init__(self) -> None:
        # init board:
        self.board = np.zeros((4, 4), dtype=int)
        self.lastmove = np.zeros((4, 4), dtype=int)
        
        # init score:
        self.score:int = 0
        self.bestScore:int = 0

        # movement variable:
        self.direction:int = 0
        self.pressed:bool = False

        # first movement:
        self.board[random.randrange(0, 4), random.randrange(0, 4)] = 2

    def manage_event(self, event:pygame.event, window):

        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYUP:
                self.movement(event)
                window.draw(self.board, self.score, self.bestScore)
            case pygame.MOUSEBUTTONUP:
                self.mouse()
                window.draw(self.board, self.score, self.bestScore)
            case pygame.VIDEORESIZE:
                window.resize_window()
                window.draw(self.board, self.score, self.bestScore)
        
        return True

    def movement(self, event):

        # get direction from event
        direction = {82:1, 80:0, 81:3, 79:2}[event.scancode]
        print(direction)
        
        # save last move:
        for i in range(4):
            for j in range(4):
                self.lastmove[i, j] = self.board[i, j]

        # rotate the matrix in the right direction
        self.board = np.rot90(self.board, 5-direction)
        
        a = 0
        change = True
        while change:
            change = False
            for i in range(3):
                for j in range(4):
                    # if the tile can move to the right:
                    if self.board[j, i] == 0 and self.board[j, i + 1] != 0:

                        self.board[j, i] = self.board[j, i + 1]
                        self.board[j, i + 1] = 0
                        change = True
                        a = 1

                    # merge two tiles
                    if self.board[j, i + 1] == self.board[j, i] and self.board[j, i] > 0:
                        self.board[j, i] *= -2
                        self.board[j, i + 1] = 0

                        # update score
                        self.score -= self.board[j, i]

                        change = True
                        a = 1
        
        # rotate back the matrix
        self.board = np.rot90(self.board, direction-1)

        # if we hade any change add new tile:
        if a == 1:
            position = random.randrange(0, 4), random.randrange(0, 4)
            # while the choosen pos is occupied
            while self.board[position] != 0:
                position = random.randrange(0, 4), random.randrange(0, 4)

            # add a random number btw 2 and 4 at the choosen position
            self.board[position] = random.choices([2, 4], weights=(10, 3), k=1)[0]

        # put back merged number to positive value
        self.board = np.absolute(self.board)

        # update best score
        if self.score > self.bestScore:
            self.bestScore = self.score


    def mouse(self):
        pass

  
    




game = Game()
window = Window()
window.draw(game.board, game.score, game.bestScore)

done = False
while not done:
    event = pygame.event.wait()

    game.manage_event(event, window)

    





                    
                        
                    

