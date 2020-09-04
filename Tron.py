import sys
sys.path.append("C:/Users/41774/Desktop/game folder/util")
import pygame
from block import block
import mesh

pygame.init()

screenWidth = 900
screenHeight = 900
win =  pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tron Game")
clock = pygame.time.Clock() 

run = True

Right = 1
Down = 2
Left = 3
Up = 4
blue = (0, 0, 255)
red = (255, 0, 0)
timeCount = 0
hit1 = False
hit2 = False
computer = True
snake2_newblock = block(810, 450)


foo = False

all_blocks = [[foo for i in range(900 // 15)] for j in range(900 // 15)]
block_num = 10



def judge(direct1, direct2, x, y):
    num1 = 0
    num2 = 0
    if direct2 == Right:
        for i in range(900 // 15):
            for j in range(900 // 15):
                if i < (x // 15):
                    if all_blocks[i][j]:
                        num1 += 1
                if i > (x // 15):
                     if all_blocks[i][j]:
                        num2 += 1

    else:
        for i in range(900 // 15):
            for j in range(900 // 15):
                if j < (y // 15):
                    if all_blocks[i][j]:
                        num1 += 1
                if j > (y // 15):
                     if all_blocks[i][j]:
                        num2 += 1
    if num1 > num2:
        return direct2
    else:
        return direct1


class snake(object):
    def __init__(self, x, y, vel, direction):
        self.x = x
        self.y = y
        self.vel = vel
        self.blocks = []
        self.direction = direction


    def move(self, snake_other, num):
        global snake2_newblock
        if not self.blocks:
            new_block = block(self.x, self.y)


        else:
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
        
        for i in self.blocks:
            
            if new_block.x == i.x and new_block.y == i.y:
                return True
        for i in snake_other.blocks:
            
            if new_block.x == i.x and new_block.y == i.y:
                return True
        
        all_blocks[new_block.x // 15][new_block.y // 15] = True
        if num == 2:
            snake2_newblock = new_block
        self.blocks.append(new_block)

        return False
        
    def draw(self, win, color):
        for i in self.blocks:
            i.draw(win, color)

snake1 = snake(90, 450, 15, Right)
snake2 = snake(810, 450, 15, Left)


def redraw():
    win.fill((255, 255, 255))

    snake1.draw(win, red)
    snake2.draw(win, blue)
    mesh.draw_mesh(win, 0, 0, 900, 900, 15, 15)
    pygame.display.update()



while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    keys = pygame.key.get_pressed()
    if snake1.direction != Down and keys[pygame.K_w]:
        snake1.direction = Up
    elif snake1.direction != Up and keys[pygame.K_s]:
        snake1.direction = Down
    elif snake1.direction != Left and keys[pygame.K_d]:
        snake1.direction = Right
    elif snake1.direction != Right and keys[pygame.K_a]:
        snake1.direction = Left

    left_block = False
    right_block = False
    down_block = False
    up_block = False


    if computer:
        for i in range (1, block_num):
            if snake2_newblock.x - i * 15 <= 0:
                left_block = True
            else:
                if all_blocks[(snake2_newblock.x - i * 15) // 15][snake2_newblock.y // 15]:
                    left_block = True
            if snake2_newblock.x + i * 15 >= 900:
                right_block = True
            else:
                if all_blocks[(snake2_newblock.x + i * 15) // 15][snake2_newblock.y // 15]:
                    right_block = True
            if snake2_newblock.y - i * 15 <= 0:
                up_block = True
            else:
                if all_blocks[snake2_newblock.x // 15][(snake2_newblock.y - i * 15) // 15]:
                    up_block = True
            if snake2_newblock.y + i * 15 >= 900:
                down_block = True
            else:
                if all_blocks[snake2_newblock.x // 15][(snake2_newblock.y + i * 15) // 15]:
                    down_block = True
        
        if snake2.direction == Left:
            if left_block:
                if not up_block and not down_block:
                    snake2.direction = judge(Up, Down, snake2_newblock.x, snake2_newblock.y)
                elif up_block and not down_block:
                    snake2.direction = Down
                elif down_block and not up_block:
                    snake2.direction = Up
                else:
                    block_num -= 1
        if snake2.direction == Up:
            if up_block:
                if not left_block and not right_block:
                    snake2.direction = judge(Left, Right, snake2_newblock.x, snake2_newblock.y)
                elif left_block and not right_block:
                    snake2.direction = Right
                elif right_block and not left_block:
                    snake2.direction = Left
                else:
                    block_num -= 1
        if snake2.direction == Right:
            if right_block:
                if not up_block and not down_block:
                    snake2.direction = judge(Up, Down, snake2_newblock.x, snake2_newblock.y)
                elif up_block and not down_block:
                    snake2.direction = Down
                elif down_block and not up_block:
                    snake2.direction = Up
                else:
                    block_num -= 1
        if snake2.direction == Down:
            if down_block:
                if not left_block and not right_block:
                    snake2.direction = judge(Left, Right, snake2_newblock.x, snake2_newblock.y)
                elif left_block and not right_block:
                    snake2.direction = Right
                elif right_block and not left_block:
                    snake2.direction = Left
                else:
                    block_num -= 1


                





    else:
        if snake2.direction != Down and keys[pygame.K_UP]:
            snake2.direction = Up
        elif snake2.direction != Up and keys[pygame.K_DOWN]:
            snake2.direction = Down
        elif snake2.direction != Left and keys[pygame.K_RIGHT]:
            snake2.direction = Right
        elif snake2.direction != Right and keys[pygame.K_LEFT]:
            snake2.direction = Left
    



    if timeCount == 100:
        hit1 = snake1.move(snake2, 1)
        hit2 = snake2.move(snake1, 2)
        timeCount = 0




    redraw()
    timeCount += 1

    if hit1 or hit2:
        
        if hit1 and hit2:
            text = "tie"
        elif hit1:
            text = "red player lose"
        elif hit2:
            text = "blue player lose"


        font = pygame.font.Font("freesansbold.ttf", 32) 

        end_l = font.render(text, True, (255, 0, 0))
        
        textRect = end_l.get_rect()  

        textRect.center = (screenWidth / 2, screenHeight / 2)

        win.blit(end_l, textRect) 
        
        pygame.display.update()
    
        pygame.time.wait(5000)

        run = False



