import turtle

s = turtle.Screen()
s.title('xxxxxx')
s.bgcolor('black')
s.setup(width= 800, height=600)
s.tracer(0)

paddle_a, paddle_b = turtle.Turtle(), turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape('square')
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
paddle_a.color('white')

paddle_b.speed(0)
paddle_b.shape('square')
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)
paddle_b.color('white')

#move function

def paddle_a_up():
    paddle_a.sety(paddle_a.ycor() + 10)


def paddle_a_down():
    paddle_a.sety(paddle_a.ycor() - 10)


def paddle_b_up():
    paddle_b.sety(paddle_b.ycor() + 10)


def paddle_b_down():
    paddle_b.sety(paddle_b.ycor() - 10)


s.listen()
s.onkeypress(paddle_a_up, "w")
s.onkeypress(paddle_a_down, "s")
s.onkeypress(paddle_b_up, "Up")
s.onkeypress(paddle_b_down, "Down")

#Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('square')
ball.penup()
ball.goto(0, 0)
ball.color('white')
# X Speed
ball.dx = 0.1
ball.dy = 0.1

pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 280)
pen.write("Player A: 0 Player B: 0", align=center)


while True:
    s.update()


    #move    
    
    
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
    
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.goto(0,0)
        time.sleep(1)


    
        