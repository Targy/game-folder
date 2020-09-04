import pygame
import argparse
import pygame_gui

from random import seed
from random import randint
from datetime import datetime

seed(datetime.now())





pygame.init()


#define variables
win =  pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paddle Game")
manager = pygame_gui.UIManager((800,600), "button.json")
singlePlayerBut = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 100), (200, 50)),
                                             text="single player",
                                             manager=manager, object_id="#button")
DoublePlayerBut = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 250), (200, 50)),
                                             text="Double player",
                                             manager=manager, object_id="#button")

ComputerPlayerBut = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 400), (200, 50)),
                                             text="Computer battle",
                                             manager=manager, object_id="#button")





first = True
start = False
clock = pygame.time.Clock() 
screenWidth = 800
screenHeight = 600
run = True
catch = True
computer_a = False
computer_b = False
score_a = 0
score_b = 0

blue = (0, 0, 255)
red = (255, 0, 0)

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 17
    
    
    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))

class ball(object):
    def __init__(self, x, y, radius, color, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = dx
        self.dy = dy
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


#function to redraw during everyupdate
def Redraw_win():
    global first
    if start:
        win.fill((231, 235, 224))
        paddle_a.draw(win, blue)
        paddle_b.draw(win, red)
        ball1.draw(win)
        font = pygame.font.Font("freesansbold.ttf", 32) 

        score_l = font.render("Score", True, (0, 0, 0))
        score_al = font.render(str(score_a), True, (0, 0, 0))
        score_bl = font.render(str(score_b), True, (0, 0, 0))


        win.blit(score_l, (screenWidth/2 - 45, 10))
        win.blit(score_al, (screenWidth/2 - 94, 10))
        win.blit(score_bl, (screenWidth/2 + 76, 10))
        if first:
            pygame.display.update()
            pygame.time.wait(2000)
            first = False
    else:
        win.fill((231, 235, 224))
        manager.draw_ui(win)

    pygame.display.update()




#set objects and random first ball

paddle_a = player(30, 225, 30, 150)
paddle_b = player(740, 225, 30, 150)
ball1 = ball(420, 290, 10, (0, 0, 0), 20, 20)

if randint(0, 1) == 0:
    ball1.dx *= -1
if randint(0, 1) == 0:
    ball1.dy *= -1




#main loop
while run:
    time_delta = clock.tick(60)/1000
    pygame.time.delay(100)
    

    #no error when click exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == singlePlayerBut:
                    start = True
                    computer_a = True
                    computer_b = False
                    paddle_a.vel = 15
                if event.ui_element == DoublePlayerBut:
                    start = True
                    computer_a = False
                    computer_b = False
                if event.ui_element == ComputerPlayerBut:
                    start = True
                    computer_a = True
                    computer_b = True
                    paddle_a.vel = 15
                    paddle_b.vel = 15
                


        manager.process_events(event)

    manager.update(time_delta)

    
    #bond keyboard with player and computer mode
    keys = pygame.key.get_pressed()
    if start:
        if computer_a:
            if ball1.dx < 0 :
                if ball1.y + ball1.radius > paddle_a.y + (paddle_a.height / 2) and paddle_a.y < screenHeight - paddle_a.height - paddle_a.vel and ball1.dy > 0:
                    paddle_a.y += paddle_a.vel
                elif ball1.y + ball1.radius < paddle_a.y + (paddle_a.height / 2) and paddle_a.y > paddle_a.vel and ball1.dy < 0:
                    paddle_a.y -= paddle_a.vel
        else:
            if keys[pygame.K_w] and paddle_a.y > paddle_a.vel:
                paddle_a.y -= paddle_a.vel
            if keys[pygame.K_s] and paddle_a.y < screenHeight - paddle_a.height - paddle_a.vel:
                paddle_a.y += paddle_a.vel
        
        if computer_b:
            if ball1.dx > 0:
                if ball1.y + ball1.radius > paddle_b.y + (paddle_b.height / 2) and paddle_b.y < screenHeight - paddle_b.height - paddle_b.vel and ball1.dy > 0:
                    paddle_b.y += paddle_b.vel
                elif ball1.y + ball1.radius < paddle_b.y + (paddle_b.height / 2) and paddle_b.y > paddle_b.vel and ball1.dy < 0:
                    paddle_b.y -= paddle_b.vel
        else:
            if keys[pygame.K_UP] and paddle_b.y > paddle_b.vel:
                paddle_b.y -= paddle_b.vel
            if keys[pygame.K_DOWN] and paddle_b.y < screenHeight - paddle_b.height - paddle_b.vel:
                paddle_b.y += paddle_b.vel
        

        #move ball and interraction with paddle, screen and score system
        ball1.x += ball1.dx
        ball1.y += ball1.dy
        if ball1.y > screenHeight - ball1.radius:
            ball1.y = screenHeight - ball1.radius
            ball1.dy *= -1
        if ball1.y < ball1.radius:
            ball1.y = ball1.radius
            ball1.dy *= -1
        if ball1.x > screenWidth - ball1.radius:
            ball1.x = 400
            ball1.y = 300
            if randint(0, 1) == 0:
                ball1.dx *= -1
            if randint(0, 1) == 0:
                ball1.dy *= -1
            pygame.time.wait(1000)
            catch = True
            score_a += 1
        elif ball1.x < ball1.radius:
            if randint(0, 1) == 0:
                ball1.dx *= -1
            if randint(0, 1) == 0:
                ball1.dy *= -1
            ball1.x = 400
            ball1.y = 300
            pygame.time.wait(1000)
            catch = True
            score_b += 1
        
        if ball1.x + (2*ball1.radius) >= paddle_b.x:
            if ball1.y  + ball1.radius <= paddle_b.y or ball1.y + ball1.radius >= paddle_b.y + paddle_b.height:
                catch = False
            elif catch:
                ball1.dx *= -1
        elif ball1.x <= paddle_a.x + paddle_a.width + 20:
            if ball1.y + ball1.radius <= paddle_a.y or ball1.y + ball1.radius >= paddle_a.y + paddle_a.height:
                catch = False
            elif catch:
                ball1.dx *= -1

    Redraw_win()
    #end game if anyone win 5 score 
    if score_a >= 5 or score_b >= 5:
        if score_a >= 5:
            text = "Blue Player win"
        else:
            text = "Red Player win"

        font = pygame.font.Font("freesansbold.ttf", 32) 

        end_l = font.render(text, True, (255, 255, 255))
        
        textRect = end_l.get_rect()  
  
        textRect.center = (screenWidth / 2, screenHeight / 2)

        win.blit(end_l, textRect) 
        
        pygame.display.update()
    
        pygame.time.wait(2000)



        run = False
    




    pygame.display.update()

    


    
pygame.quit()