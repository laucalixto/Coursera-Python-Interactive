# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [1 ,1]


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0, 0]
    if(direction == RIGHT):
        ball_vel[0] = 1 
        ball_vel[1] = -1
    if(direction == LEFT):
        ball_vel[0] = -1 
        ball_vel[1] = -1

# helper function
def distance(p, q):
    return math.sqrt( (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
        
        
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [WIDTH - PAD_WIDTH,(HEIGHT /2) - HALF_PAD_HEIGHT]
    paddle2_pos = [PAD_WIDTH,(HEIGHT /2) - HALF_PAD_HEIGHT]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    score1 = 0
    score2 = 0
    
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #collision detection paddles
    if ball_pos[0] + BALL_RADIUS >= ((WIDTH - 1) - PAD_WIDTH):
        if ball_pos[1] in range(paddle1_pos[1], paddle1_pos[1] + (PAD_HEIGHT + 1)):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += ball_vel[0]
            ball_vel[1] += ball_vel[1]
        else:
            spawn_ball(RIGHT)
            score2+=1
            ball_vel += ball_vel 
        
    if ball_pos[0] - BALL_RADIUS  <= PAD_WIDTH:
        if ball_pos[1] in range(paddle2_pos[1], paddle2_pos[1] + (PAD_HEIGHT + 1)):
            ball_vel[0] = ball_vel[0] * -1
            ball_vel[0] += ball_vel[0] 
            ball_vel[1] += ball_vel[1] 
        else:
            spawn_ball(LEFT)
            score1+=1
            ball_vel += ball_vel 
    
    #collision detection screen top/down
    if((ball_pos[1] >= HEIGHT - BALL_RADIUS) or (ball_pos[1] <= BALL_RADIUS)):
       ball_vel[1] = -ball_vel[1]
        
        
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1,"White", "White")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > 0 or paddle1_pos[1] < HEIGHT - 1:
        paddle1_pos[1] += paddle1_vel[1]
    if paddle1_pos[1] < 0 or paddle1_pos[1] + PAD_HEIGHT > HEIGHT - 1:
        paddle1_vel[1] = 0
    
    if paddle2_pos[1] > 0 or paddle2_pos[1] < HEIGHT - 1:
        paddle2_pos[1] += paddle2_vel[1]
    if paddle2_pos[1] < 0 or paddle2_pos[1] + PAD_HEIGHT > HEIGHT - 1:
        paddle2_vel[1] = 0
                
    # draw paddles
    canvas.draw_line(paddle1_pos, [WIDTH - PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos, [PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH - WIDTH/4,HEIGHT/4], 60, "White")
    canvas.draw_text(str(score2), [WIDTH/4, HEIGHT/4], 60, "White")

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle1_vel[1] = -2
    elif key == simplegui.KEY_MAP["down"]:
        paddle1_vel[1] = 2
    
    if key == simplegui.KEY_MAP["w"]:
        paddle2_vel[1] = -2
    elif key == simplegui.KEY_MAP["s"]:
        paddle2_vel[1] = 2
    
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle1_vel[1] = 0
    
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle2_vel[1] = 0
    
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
