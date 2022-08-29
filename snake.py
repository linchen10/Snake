import pygame, sys, random
from pygame.math import Vector2

#make a fruit class
class FRUIT:
    def __init__(self):
        self.randomize()

    #draw fruit
    def draw_fruit(self):
        #pygame.Rect(x,y,w,h)
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        #surface.blit(background, rectangle)
        screen.blit(apple, fruit_rect)
        
    #randomize x and y where fruit appears
    def randomize(self):
        self.x = random.randint(0,cell_num-1)
        self.y = random.randint(0,cell_num-1)
        self.pos = Vector2(self.x,self.y)

#make a snake class
class SNAKE:
    def __init__(self):
        #snake's original position and direction
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        #import snake graphics
        self.head_up = pygame.image.load('OneDrive/Documents/Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('OneDrive/Documents/Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('OneDrive/Documents/Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('OneDrive/Documents/Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('OneDrive/Documents/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('OneDrive/Documents/Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('OneDrive/Documents/Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('OneDrive/Documents/Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('OneDrive/Documents/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('OneDrive/Documents/Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('OneDrive/Documents/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('OneDrive/Documents/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('OneDrive/Documents/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('OneDrive/Documents/Graphics/body_bl.png').convert_alpha()

        #crunch sound
        self.crunch_sound = pygame.mixer.Sound('OneDrive/Documents/Sound/crunch.wav')
    
    #draw and update the snake's head graphics, body graphics, and tail graphics
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect =  pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index ==  len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else: 
                #checks blocks next to each other for body turn graphics
                previous_block =  self.body[index +1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x: #x is the same then blocks are vertical
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y: #y is the same then blocks are horizontal
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)
    
    #update head graphics based on vector position of snake's second block - snake's head
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    #update tail graphics based on vector position of snake's second to last block - snake's last block
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    #stimulate the snake moving by making a copy of the body 
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:] #includes all elements in the list 
            body_copy.insert(0,body_copy[0] + self.direction) #add one element in the front that's was first element in previous list plus the direction
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1] #includes all elements in the list except the last one
            body_copy.insert(0,body_copy[0] + self.direction) #add one element in the front that's was first element in previous list plus the direction
            self.body = body_copy[:]

    #add a block    
    def add_block(self):
        self.new_block=True

    #play a crunch sound
    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    #reset the body to original position 
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    #move the snake, check for collision
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    #draw the grass, fruit, snake, and score
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        
    #when the snake's head eats the apple, a new random apple is generated and it will not be on the snake's body
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    #if the snake hits the screen edges the game resets
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_num  or not 0 <= self.snake.body[0].y < cell_num:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    #resets the snake when it's game over
    def game_over(self):
        self.snake.reset()

    #draws a darker shade of green every other block every row
    def draw_grass(self):
        grass_color = (167,209,62)
        for row in range(cell_num):
            if row % 2 == 0:
                for col in range(cell_num):
                    if col %2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_num):
                    if col %2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    #counts the number of apples eaten, puts a picture of an apple next to the score, and draws a rectangular outline around the two objects
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True ,(56,74,12)) #text, aa, color
        score_x = int(cell_size * cell_num - 60)
        score_y = int(cell_size * cell_num - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 10, apple_rect.height)
        pygame.draw.rect(screen, (167,209,61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect,2)

#starts pygame
pygame.mixer.pre_init(44100,-16,2,512) #play sound immediately on collision
pygame.init()

#create display surface
cell_size = 40
cell_num = 20
screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num))

#set max
clock = pygame.time.Clock()

#apple graphics
apple =  pygame.image.load('OneDrive/Documents/Graphics/apple.png').convert_alpha()

#game font
game_font = pygame.font.Font('OneDrive/Documents/Font/PoetsenOne-Regular.ttf', 25)

#screen update
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150) #screen_update will be triggered every 150ms
main_game = MAIN()

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #checks for QUIT event
            pygame.quit() #deactivates pygame
            sys.exit() #terminate program
        if event.type  ==  SCREEN_UPDATE:
            main_game.update()
        #if a button is pressed, the snake goes in a different direction
        #the snake can't turn left if it's facing right or down if it's facing up etc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                   main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
    screen.fill((175,215,70)) #fill the screen with a certain color
    main_game.draw_elements()
    pygame.display.update() #redraws screen over and over again
    clock.tick(60) # speed to 60 fps
