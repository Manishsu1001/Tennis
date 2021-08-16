import pygame
import random

pygame.font.init()

#display_window
WIDTH = 1000
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
#COLORS
WHITE = (0,0,0)
WHITE1 = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
#BASIC_SETTINGS
FPS = 60
SCORES_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',120)
#BATS
BAT_W = 100
BAT_H = 20
BAT_V = 13
LIM_L = 20
LIM_R = 600

#BALL_VELOCITY
BALL_SIZE = 15
#EVENTS
RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2
RED_MISS = pygame.USEREVENT + 3 
BLUE_MISS = pygame.USEREVENT + 4
L_WALL_HIT = pygame.USEREVENT + 5
R_WALL_HIT = pygame.USEREVENT + 6

def draw_win(red,blue,ball,red_p,blue_p):
    WIN.fill(WHITE)
    boundary_l = pygame.Rect(LIM_R,0,20,HEIGHT)
    boundary_r = pygame.Rect(LIM_L-20,0,20,HEIGHT)
    pygame.draw.rect(WIN,WHITE1,boundary_l)
    pygame.draw.rect(WIN,WHITE1,boundary_r)
    pygame.draw.rect(WIN,RED,red)
    pygame.draw.rect(WIN,BLUE,blue)
    pygame.draw.rect(WIN,YELLOW,ball)
    red_score = SCORES_FONT.render('SCORE: '+str(red_p),1,WHITE1)
    blue_score = SCORES_FONT.render('SCORE: '+str(blue_p),1,WHITE1)
    WIN.blit(red_score,(LIM_R + (WIDTH - LIM_R - red_score.get_width())//2,200))
    WIN.blit(blue_score,(LIM_R + (WIDTH - LIM_R - blue_score.get_width())//2,400))
    pygame.display.update()

def red_control(kp,red):
    if kp[pygame.K_a] and red.x - BAT_V > LIM_L:
        red.x -= BAT_V
    if kp[pygame.K_d] and red.x + BAT_V + BAT_W< LIM_R:
        red.x += BAT_V

def blue_control(kp,blue):
    if kp[pygame.K_LEFT] and blue.x - BAT_V > LIM_L:
        blue.x -= BAT_V
    if kp[pygame.K_RIGHT] and blue.x + BAT_V +BAT_W < LIM_R:
        blue.x += BAT_V

def ballhitbat(ball,red,blue,VEL_X,VEL_Y):
    if red.colliderect(ball):
        pygame.event.post(pygame.event.Event(RED_HIT))
    if blue.colliderect(ball):
        pygame.event.post(pygame.event.Event(BLUE_HIT))
    if ball.y + VEL_Y < 0 :
        pygame.event.post(pygame.event.Event(RED_MISS))
    if ball.y + VEL_Y > HEIGHT:
        pygame.event.post(pygame.event.Event(BLUE_MISS))
    if ball.x + VEL_X < LIM_L:
        pygame.event.post(pygame.event.Event(L_WALL_HIT))
    if ball.x + VEL_X + BALL_SIZE>LIM_R :
        pygame.event.post(pygame.event.Event(R_WALL_HIT))
def game_won(winner):
    winnertext = WINNER_FONT.render(winner,1,WHITE1)
    WIN.blit(winnertext,((LIM_R-LIM_L-winnertext.get_width())//2,(HEIGHT-winnertext.get_height())//2))
    pygame.display.update()
def draw_ball(ball):
    WIN.draw.pygame.draw.rect(WIN, YELLOW,ball,) 
    
def start_time(tym1, tym2):
    if tym1 < 3000:
        tym = 3- int(tym1/1000)
    else:
        tym = 3- int(tym2/1000)
    text = SCORES_FONT.render('Start in ' + str(tym) , 1 , WHITE1)
    WIN.blit(text,(LIM_R + (WIDTH - LIM_R-text.get_width())//2,HEIGHT//2 - text.get_height()//2)) 
    pygame.display.update()

def randomgo():
    randomness = random.randint(0,4)
    if randomness in [0,1]:
        return -7
    if randomness in[2,3]:
        return 7
    if randomness == 4:
        return 0
def main():
    red_p = 0
    blue_p = 0
    red = pygame.Rect(100,10,BAT_W,BAT_H)
    blue = pygame.Rect(100,570,BAT_W,BAT_H)
    ball = pygame.Rect(LIM_R//2-LIM_L//2,HEIGHT//2,BALL_SIZE,BALL_SIZE)
    # INI1 = random.randint(8,12)
    # INI2 = random.randint(8,12)
    INI1 = 7
    INI2 = 7
    initial_ball_speeds = [INI1,-INI1,INI2,-INI2]
    VEL_X = initial_ball_speeds[random.randint(0,1)]
    VEL_Y = initial_ball_speeds[random.randint(2,3)]
    run = True
    x_r = -5000
    x_b = -5000
    clk = pygame.time.Clock()
    while run:
        y_r = pygame.time.get_ticks()
        y_b = pygame.time.get_ticks()
        clk.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == RED_HIT or event.type == BLUE_HIT:
                VEL_Y = -VEL_Y
                VEL_X = randomgo()
            if event.type == RED_MISS:
                ball = pygame.Rect(LIM_R//2-LIM_L//2,HEIGHT//2,BALL_SIZE,BALL_SIZE)
                blue_p += 1
                x_r = pygame.time.get_ticks()
            if event.type == BLUE_MISS:
                ball = pygame.Rect(LIM_R//2-LIM_L//2,HEIGHT//2,BALL_SIZE,BALL_SIZE)
                red_p += 1
                x_b = pygame.time.get_ticks()
            if event.type == L_WALL_HIT or event.type == R_WALL_HIT:
                VEL_X = -VEL_X
            
        wintext = ""
        if red_p >= 10:
            wintext = "RED WON"
        if blue_p >= 10:
            wintext = "BLUE WON"
        if wintext != "":
            game_won(wintext)
            pygame.time.delay(5000)
            pygame.quit()

        # if randomness < 5 and ball.x + VEL_X < LIM_R:
            # ball.x += VEL_X
        # elif randomness < 10  and randomness >= 5 and ball.x -VEL_X > LIM_L:
            # ball.x -= VEL_X
        # else:
            # ball.x += 0
        ball.x += VEL_X
        ball.y += VEL_Y
        draw_win(red,blue,ball,red_p,blue_p)
        ballhitbat(ball,red,blue,VEL_X,VEL_Y)
        key_pressed = pygame.key.get_pressed()
        red_control(key_pressed,red)
        blue_control(key_pressed,blue)
        time1 = y_r - x_r
        time2 = y_b - x_b
        if  time1< 3000 or time2<3000:
            ball.x,ball.y = LIM_R//2-LIM_L//2,HEIGHT//2
            start_time(time1,time2)
            

if __name__ == '__main__':
    main()
        