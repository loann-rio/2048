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
        self.size_image = self.width//11
        
        # init screen:
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # load images:
        self.back_img = pygame.image.load(r'retour.jpg')
        self.restart_img = pygame.image.load(r'recommencer.jpg')

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
                    (self.width//27, self.width//27))
        
        # renter score
        self.screen.blit(self.font_number.render('score:', True, (150, 50, 50)),
                    (self.width//1.5, self.width//27))
        self.screen.blit(self.font_number.render(str(score), True, (50, 50, 150)),
                    (self.width//1.5, self.width//12.3))
        
        # render best score:
        self.screen.blit(self.font_number.render('best score:', True, (150, 50, 50)),
                    (self.width//1.5, self.width//7.1))
        self.screen.blit(self.font_number.render(str(bestScore), True, (50, 50, 150)),
                    (self.width//1.5, self.width//5.4))

        # render buttons:
        pygame.draw.rect(self.screen, (125, 125, 125), [self.width//9, self.width//4, self.size_image+2, self.size_image+2])
        pygame.draw.rect(self.screen, (125, 125, 125), [self.width//3.4, self.width//4, self.size_image+2, self.size_image+2])
        
        self.screen.blit(self.back_img, (self.width//9 +1, self.width//4 +1))
        self.screen.blit(self.restart_img, (self.width//3.4 +1, self.width//4 +1))

        # draw table lines:
        for i in range(5):
            pygame.draw.line(self.screen, (127, 127, 127), 
                             (self.X_offset + i*self.size_main_rect//4, self.Y_offset), 
                             (self.X_offset + i*self.size_main_rect//4, self.Y_offset+self.size_main_rect), 3)
             
            pygame.draw.line(self.screen, (127, 127, 127), 
                             (self.X_offset, self.Y_offset + i*self.size_main_rect//4), 
                             (self.X_offset + self.size_main_rect, self.Y_offset+i*self.size_main_rect//4), 3)
            
        pygame.display.flip()


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

    def manage_event(self, event):
        match event:
            case pygame.QUIT:
                return False
            case pygame.KEYUP:
                self.movement(event)
            case pygame.MOUSEBUTTONUP:
                self.mouse()
            case pygame.VIDEORESIZE:
                self.resize_window()
        return True

    def movement(self):
        pass

    def mouse(self):
        pass

    def resize_window(self):
        pass

    




game = Game()
window = Window()

done = False
while not done:
    event = pygame.event.wait()

    game.manage_event(event)

    window.draw(game.board, game.score, game.bestScore)





                    
                        
                    

