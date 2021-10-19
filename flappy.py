'''
Author: Raj Madhu
Github: https://github.com/rajmadhu0406
'''

import pygame,sys,random

from pygame.constants import GL_MULTISAMPLEBUFFERS

#this fn will draw 2 floors which will move one after other to show cont. motion
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,532))
    screen.blit(floor_surface,(floor_x_pos+420,532))

def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(600,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midbottom=(600,random_pipe_pos-300))
    #returns tuple
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        #moves to left
        pipe.centerx-=5
    # return pipe list of pipes that are not seen
    visible_pipes=[pipe for pipe in pipes if pipe.right>-50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=700:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)  #we don't want to flip in x direction so false and for y, true
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            # print("collision")
            death_sound.play()
            can_score=True
            return False
    #check for bird moving in the clouds
    if bird_rect.top <=-200 or bird_rect.bottom >=532:
        # print("collision")
        #can_score = True
        return False
    #return true to game_active variable if there are no colisions
    return True

def rotate_bird(bird):
    # rotozoom can scale and rotate surface
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird=bird_frames[bird_index]
    #take centery from previous bird position
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):

    if game_state=='main_game':
        score_surface=game_font.render(str(int(score)),True,(255,255,255))
        score_rect=score_surface.get_rect(center=(210,80))
        screen.blit(score_surface,score_rect)

    #if game over then also show highscore
    if game_state=='game_over':
        score_surface=game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect=score_surface.get_rect(center=(210,80))
        screen.blit(score_surface,score_rect)

        high_score_surface=game_font.render(f'High score: {int(high_score)}',True,(0,0,0))
        high_score_rect=high_score_surface.get_rect(center=(210,500))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score>high_score:
        high_score=score
    return high_score

def pipe_score_check():
    global score,can_score

    if pipe_list:
        for pipe in pipe_list:    
            if 95<pipe.centerx<105 and can_score==True:
                score+=1
                score_sound.play()
                can_score=False
            if pipe.centerx<0:
                can_score=True



#pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512)

# initializing pygame
pygame.init()

# creating black screen (width x height)
screen=pygame.display.set_mode((420,700))  
# screen=pygame.display.set_mode((576,1024))

# clock needed to limit frame rates
clock=pygame.time.Clock()
# Game font
game_font=pygame.font.Font('04B_19.TTF',40)

#Game variables
gravity=0.25
bird_movement=0
game_active=True
score=0
high_score=0
can_score=True

#setting up background variable
bg_surface=pygame.image.load('assets/background-day.png').convert()  #convert turns the images into a file which is easier to understand for pygame
# resizing background image
bg_surface = pygame.transform.scale(bg_surface, (int(bg_surface.get_width() * 1.5), int(bg_surface.get_height() * 1.5)))


floor_surface=pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (int(floor_surface.get_width() * 1.5), int(floor_surface.get_height() * 1.5)))
# variable to change the frame x position, so it looks like its moving
floor_x_pos=0

# BIRD MOVEMENT

bird_downflap=pygame.image.load('assets/bluebird-downflap.png').convert_alpha() #convert alpha to remove black bg
bird_downflap = pygame.transform.scale(bird_downflap, (int(bird_downflap.get_width() * 1.5), int(bird_downflap.get_height() * 1.5)))

bird_midflap=pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap, (int(bird_midflap.get_width() * 1.5), int(bird_midflap.get_height() * 1.5)))

bird_upflap=pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (int(bird_upflap.get_width() * 1.5), int(bird_upflap.get_height() * 1.5)))

bird_frames=[bird_downflap,bird_midflap,bird_upflap]
bird_index=0
bird_surface=bird_frames[bird_index]
# get a imaginary rectangle around image which help in detecting colision
bird_rect=bird_surface.get_rect(center=(100,300))

BIRDFLAP=pygame.USEREVENT + 1  # +1 for second event
pygame.time.set_timer(BIRDFLAP,200)
# bird_surface=pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface, (int(bird_surface.get_width() * 1.5), int(bird_surface.get_height() * 1.5)))
# bird_rect=bird_surface.get_rect(center=(100,300))

pipe_surface=pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (int(pipe_surface.get_width() * 1.5), int(pipe_surface.get_height() * 1.5)))
# This list contains lots of rectangle that are moving left and new pipes are created after small time intervals
pipe_list=[]
#timer
SPAWNPIPE=pygame.USEREVENT
# event will be triggered every 1.2 sec
pygame.time.set_timer(SPAWNPIPE,1200)
#pipe height for random to choose from
pipe_height=[250,400,500]

#images to display when game gets over
game_over_surface=pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (int(game_over_surface.get_width() * 1.2), int(game_over_surface.get_height() * 1.2)))
game_over_rect=game_over_surface.get_rect(center=(210,280))

# add sound effect
flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound=pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound=pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown=100

while True:

    # looks for every event in the game
    for event in pygame.event.get():
        # quit event type
        if event.type==pygame.QUIT:
            pygame.quit()
            #shuting down the game
            sys.exit()

        if event.type==pygame.KEYDOWN:
            # checking keyboard input
            if event.key==pygame.K_SPACE and game_active==True:
                # print("jump")
                #reseting movement so jump height remains same
                bird_movement=0
                bird_movement-=7
                flap_sound.play()

            # if collision occurs
            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                #clearing  pipes if game over
                pipe_list.clear()
                #recenter and reset bird for new game
                bird_rect.center=(100,300)
                bird_movement=0
                score=0


        #PIPES
        if event.type==SPAWNPIPE:
            # print("pipe")
            # pipe_list.append(create_pipe())
            pipe_list.extend(create_pipe())
            # print(pipe_list)
        
        if event.type==BIRDFLAP:
            if bird_index>2:
                bird_index+=1
            else:
                bird_index=0
            
            bird_surface,bird_rect=bird_animation()

    #adding backgroung image
    screen.blit(bg_surface,(0,0))

    # if game is active, then only show bird and pipes
    if game_active==True:
        #BIRD
        #changing bird position
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird_surface)
        #moving bird rectangle downwards (falling)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active=check_collision(pipe_list)
        
        #PIPES
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # score+=0.01
        
        #SCORES
        pipe_score_check()
        score_display('main_game')
        # score_sound_countdown-=1
        # if score_sound_countdown<=0:
        #     score_sound.play()
        #     score_sound_countdown=100

    
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score=update_score(score,high_score)
        score_display('game_over')

    
    #FLOOR
    floor_x_pos-=1
    draw_floor()
    if floor_x_pos<=-420: #to move the floor indefinetely
        floor_x_pos=0

    #takes everything drawn above and keeps continuosly updating it
    pygame.display.update()
    # 120 frames per second
    clock.tick(120)






