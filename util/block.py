import pygame



class block(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
    
    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.width))

    def set_pos(self, x, y):
        self.x = x
        self.y = y
