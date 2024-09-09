import pygame, random
def floor_adjust():
    window.blit(floor,(floor_pos, 650))
    window.blit(floor,(floor_pos + 432, 650))
def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = green_pipe.get_rect(midtop = (500, random_pipe_height))
    top_pipe = green_pipe.get_rect(midtop = (500, random_pipe_height - 650))

    return bottom_pipe, top_pipe
def pipe_movement(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            window.blit(green_pipe,pipe)
        else:
            flip_pipe = pygame.transform.flip(green_pipe,False,True) 
            window.blit(flip_pipe,pipe)
def collision(pipes):
    for pipe in pipes:
        if bird_reck.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_reck.top <= -75 or bird_reck.bottom >= 650:
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, - bird_movement*2, 1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_reck.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255)) 
        score_rect = score_surface.get_rect(center = (216,100))
        window.blit(score_surface,score_rect)
    elif game_state == 'game_over' :
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255)) 
        score_rect = score_surface.get_rect(center=(216, 100))
        window.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255)) 
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        window.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency= 44100, size = -16, channels = 2, buffer = 512)
pygame.init()
window = pygame.display.set_mode((432,768)) 
#create a background
background = pygame.transform.scale2x(pygame.image.load('/Users/xuanhuong/Desktop/PythonProjects/''Flappybird/Image/' 'background-night.png')).convert_alpha() #chèn ảnh: dùng location của ảnh
#create a floor
floor = pygame.transform.scale2x(pygame.image.load('/Users/xuanhuong/Desktop/PythonProjects/''Flappybird/Image/''floor.png')).convert_alpha()
#create a yellow bird
bird_up = pygame.transform.scale2x(pygame.image.load('/Users/xuanhuong/Desktop/PythonProjects/''Flappybird/Image/''yellowbird-upflap.png').convert_alpha())
bird_down = pygame.transform.scale2x(pygame.image.load('/Users/xuanhuong/Desktop/PythonProjects/''Flappybird/Image/''yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('/Users/xuanhuong/Desktop/PythonProjects/''Flappybird/Image/''yellowbird-midflap.png').convert_alpha())
bird_list = [bird_up,bird_mid,bird_down]
bird_index = 0
bird = bird_list[bird_index]
bird_reck = bird.get_rect(center = ( 100, 384))
#create timer for bird
bird_flap = pygame.USEREVENT + 1 #differentiate with pipe
pygame.time.set_timer(bird_flap,200)
#create pipe
green_pipe = pygame.image.load('/Users/xuanhuong/Desktop/PythonProjects/''Flappybird/Image/''pipe-green.png').convert()
green_pipe = pygame.transform.scale2x(green_pipe)
pipe_height = [150 , 250, 350 ]
game_over_surface = pygame.transform.scale2x(pygame.image.load('/Users/xuanhuong/Desktop/PythonProjects/''Flappybird/Image/''gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))

flap_sound = pygame.mixer.Sound('/Users/xuanhuong/Desktop/PythonProjects/Flappybird/Sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('/Users/xuanhuong/Desktop/PythonProjects/Flappybird/Sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('/Users/xuanhuong/Desktop/PythonProjects/Flappybird/Sound/sfx_point.wav')
point_sound_countdown = 100
game_active = True
pipe_list = []
#create timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200) #after 1.2sec


floor_pos = 0
gravity = 0.25
game_font = pygame.font.Font('/Users/xuanhuong/Desktop/PythonProjects/Flappybird/Font/04B_19.TTF', 40)
bird_movement = 0
score = 0
high_score = 0
clock = pygame.time.Clock() 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                bird_movement = 0
                bird_movement = -11
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active= True
                pipe_list.clear()
                bird_reck.center = (100,384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_reck = bird_animation()



    window.blit(background,(0,0))
    if game_active:
        bird_movement += gravity 
        rotated_bird = rotate_bird(bird)
        bird_reck.centery += bird_movement 
        window.blit(rotated_bird,bird_reck)
        game_active = collision(pipe_list)

        pipe_list = pipe_movement(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        point_sound_countdown -= 1
        if point_sound_countdown <= 0:
            point_sound.play()
            point_sound_countdown = 100

    else:
        window.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    floor_pos -= 1
    floor_adjust()
    if floor_pos <= -432:
        floor_pos = 0

    pygame.display.update()
    clock.tick(120) #set fps
pygame.quit()
