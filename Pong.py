# Implementation of classic arcade game Pong

import simplegui
import random

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
VEL_INCREASE = 1.1
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [-5.0, 5.0]
    ball_vel_x = random.randrange(5,9)
    ball_vel_y = -1 * random.randrange(2,6)
    if direction == RIGHT:
        ball_vel = [ball_vel_x, ball_vel_y]    
    else:
        ball_vel = [-ball_vel_x, ball_vel_y]
            
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(LEFT)
    score1 = 0
    score2 = 0
     
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = ball_vel[1] * -1
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = ball_vel[1] * -1    

    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]    
    
    #determine if ball touches gutter   
        
#reflect if ball hits paddle1    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
        ball_vel[0] = -1 * ball_vel[0]
        ball_vel[0] = VEL_INCREASE * ball_vel[0]
        ball_vel[1] = VEL_INCREASE * ball_vel[1]

        
#reflect if ball hits paddle2    
    paddle2_top = paddle2_pos - HALF_PAD_HEIGHT
    paddle2_bottom = paddle2_pos + HALF_PAD_HEIGHT
    if ball_pos[0] + BALL_RADIUS >= WIDTH  - PAD_WIDTH and ball_pos[1] >= paddle2_top and ball_pos[1] <= paddle2_bottom:
        ball_vel[0] = -1 * ball_vel[0]
        ball_vel[0] = VEL_INCREASE * ball_vel[0]
        ball_vel[1] = VEL_INCREASE * ball_vel[1]

        
#respawn when paddle1 misses
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and not(ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT):
        
        score2 += 1
       
        spawn_ball(RIGHT)
        
#respawn when paddle2 misses
    if ball_pos[0] + BALL_RADIUS >= WIDTH  - PAD_WIDTH and not (ball_pos[1] >= paddle2_top and ball_pos[1] <= paddle2_bottom):
        score1 += 1
        spawn_ball(LEFT)        
    
    # draw ball

    canvas.draw_circle(ball_pos,BALL_RADIUS,1,"White","White")


    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT], 
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT] ],
                        1, 'Green','Green')
    canvas.draw_polygon([[WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 
                         [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT] ],
                        1, 'Green','Green')
    
    #prevent paddles from moving off the screen
    if paddle1_pos - HALF_PAD_HEIGHT <= 0 or paddle1_pos + HALF_PAD_HEIGHT >= HEIGHT:
        paddle1_vel = 0
    if paddle2_pos - HALF_PAD_HEIGHT <= 0 or paddle2_pos + HALF_PAD_HEIGHT >= HEIGHT:
        paddle2_vel = 0

    
    # draw scores
    canvas.draw_text(str(score1), (20, 35), 40, 'White')
    canvas.draw_text(str(score2), (560, 35), 40, 'White')

        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down'] and not (paddle2_pos + HALF_PAD_HEIGHT >= HEIGHT):
        paddle2_vel = 5
    if key == simplegui.KEY_MAP['up'] and not (paddle2_pos - HALF_PAD_HEIGHT <= 0):
        paddle2_vel = -5
    if key == simplegui.KEY_MAP['s'] and not (paddle1_pos + HALF_PAD_HEIGHT >= HEIGHT):
        paddle1_vel = 5
    if key == simplegui.KEY_MAP['w'] and not (paddle1_pos - HALF_PAD_HEIGHT <= 0):
        paddle1_vel = -5
         
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0        
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0           
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game",new_game)


# start frame

frame.start()
