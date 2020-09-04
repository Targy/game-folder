import sys
sys.path.append("C:/Users/41774/Desktop/game folder/util")


import pygame
from random import seed
from random import randint
from datetime import datetime
from block import block 
seed(datetime.now())


pygame.init()

screenWidth = 900
screenHeight = 600
win =  pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake game")
clock = pygame.time.Clock() 

run = True

#set direction as int and other variables
Right = 1
Down = 2
Left = 3
Up = 4
food = False
timeCount = 0
hit = False
start = False
lose = False

class snake(object):
    def __init__(self):
        self.x = screenWidth / 2
        self.y = screenHeight / 2
        self.length = 5
        self.direction = Right
        block1 = block(screenWidth/2 - 30, screenHeight / 2 )
        block2 = block(screenWidth/2 - 15, screenHeight / 2 )
        block3 = block(screenWidth/2 , screenHeight / 2 )
        block4 = block(screenWidth/2 + 15, screenHeight / 2 )
        block5 = block(screenWidth/2 + 30, screenHeight / 2 )
        
        self.blocks = [block1, block2, block3, block4, block5]
    
    def move(self):
        pop = True
        
        if self.direction == Right:
            new_block = block(self.blocks[-1].x + 15, self.blocks[-1].y)
            if new_block.x >= screenWidth:
                return True
        elif self.direction == Left:
            new_block = block(self.blocks[-1].x - 15, self.blocks[-1].y)
            if new_block.x < 0:
                return True
        elif self.direction == Up:
            new_block = block(self.blocks[-1].x , self.blocks[-1].y - 15)
            if new_block.y < 0:
                return True
        elif self.direction == Down:
            new_block = block(self.blocks[-1].x, self.blocks[-1].y + 15)
            if new_block.y >= screenHeight:
                return True
        
        if new_block.x == foodBlock.x and new_block.y == foodBlock.y:
            global food
            food = False
            pop = False


        for i in self.blocks:
            
            if new_block.x == i.x and new_block.y == i.y:
                return True
        
        if pop:
            self.blocks.pop(0)
        self.blocks.append(new_block)



        return False
        
        
    def draw(self, win):
        for i in self.blocks:
            i.draw(win, (255, 255, 255))
        


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


#initial the objects
snake1 = snake()
foodBlock = block(randint(0, (screenWidth - 15) // 15) * 15, randint(0, (screenHeight - 15) // 15) * 15)
startButton = button((0, 255, 0), 325, 250, 250, 100,  'Start')



def redraw(snake1):
    if start == True:
        win.fill((0, 0, 0))
        foodBlock.draw(win)
        snake1.draw(win)  
    else:
        startButton.draw(win, (0, 0, 0))
    pygame.display.update()
        

def gameLoop():
    global timeCount, food, hit
        #bond keys
    keys = pygame.key.get_pressed()
    if snake1.direction != Down and keys[pygame.K_w]:
        snake1.direction = Up
    elif snake1.direction != Up and keys[pygame.K_s]:
        snake1.direction = Down
    elif snake1.direction != Left and keys[pygame.K_d]:
        snake1.direction = Right
    elif snake1.direction != Right and keys[pygame.K_a]:
        snake1.direction = Left
    

    


    #move slower but can catch every input
    if timeCount == 100:
        hit = snake1.move()
        timeCount = 0
    
    #generate random food but not inside snake body
    if not food:
        go = True
        while go:
            foodBlock.set_pos(randint(0, (screenWidth - 15) // 15) * 15, randint(0, (screenHeight - 15) // 15) * 15)
            bad = False
            for i in snake1.blocks:
                if foodBlock.x == i.x and foodBlock.y == i.y:
                    bad = True
            if not bad:
                go = False
        
        food = True
    
    
    
    
    
    redraw(snake1)

    timeCount += 1

    #exit the game with message
    if hit:
        
        text = "You lose"


        font = pygame.font.Font("freesansbold.ttf", 32) 

        end_l = font.render(text, True, (255, 0, 0))
        
        textRect = end_l.get_rect()  

        textRect.center = (screenWidth / 2, screenHeight / 2)

        win.blit(end_l, textRect) 
        
        pygame.display.update()
    
        pygame.time.wait(5000)



        run = False



while run:
    redraw(snake1)
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if startButton.isOver(pos):
                start = True

        if event.type == pygame.MOUSEMOTION:
            if startButton.isOver(pos):
                startButton.color = (255, 0, 0)
            else:
                startButton.color = (0, 255, 0)
    if start:
        gameLoop()
pygame.quit()