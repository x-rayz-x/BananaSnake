import pygame, sys
from pygame.math import Vector2
import random

# snake class
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        
        self.head_up = pygame.image.load('snake/up.png').convert_alpha()
        self.head_down = pygame.image.load('snake/down.png').convert_alpha()
        self.head_right = pygame.image.load('snake/right.png').convert_alpha()
        self.head_left = pygame.image.load('snake/left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('snake/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('snake/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('snake/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('snake/tail_left.png').convert_alpha()
        
        self.body_vertical = pygame.image.load('snake/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('snake/body_hortizontal.png').convert_alpha()
        
        self.body_tr = pygame.image.load('snake/tr.png').convert_alpha()
        self.body_tl = pygame.image.load('snake/tl.png').convert_alpha()
        self.body_br = pygame.image.load('snake/br.png').convert_alpha()
        self.body_bl = pygame.image.load('snake/bl.png').convert_alpha()
        self.crunch  = pygame.mixer.Sound('Crunch.mp3')
    
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, block in enumerate(self.body):
            # we still need a rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            # what direction is the face heading"
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else: 
                previous__block = self.body[index + 1] - block
                next_block =  self.body[index - 1] - block
                # check if previous and next block have same x or y
                if previous__block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous__block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else: # bascially checks whether x and y of previous block and next block match those that are diagonal
                    if previous__block.x == -1 and next_block.y == -1 or previous__block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous__block.x == -1 and next_block.y == 1 or previous__block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous__block.x == 1 and next_block.y == -1 or previous__block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous__block.x == 1 and next_block.y == 1 or previous__block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                
   
    def update_head_graphics(self):
        # difference in vectors between head and first block
        head_relation = self.body[1] - self.body[0]
        # head is left of the next block
        if head_relation == Vector2(1,0): self.head = self.head_left 
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up 
        elif head_relation == Vector2(0,-1): self.head = self.head_down 
        
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        # head is left of the next block
        if tail_relation == Vector2(1,0): self.tail = self.tail_left 
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up 
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down


    # make a way to move the snake
    def move_snake(self):
        # if function result is true then execute this
        if self.new_block == True:
            body_copy = self.body[:]
            # change direction of head
            body_copy.insert(0, body_copy[0] + self.direction )
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            # change direction of head
            body_copy.insert(0, body_copy[0] + self.direction )
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def play_sound(self):
        self.crunch.play()
        
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]

# fruit(apple) class
class FRUIT:
    def __init__(self):
        # this changes fruit position 
        self.randomize()
        
    #method to draw fruit
    def draw_fruit(self):
        # create a rectangle (x,y,w,h) pygame loves integers, but vector values are float by deafult
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        # draw the rectangle, surface, color, rectangle
        #pygame.draw.rect(screen, (126, 166, 140),fruit_rect)
        screen.blit(banana, fruit_rect)
    
    def randomize(self):
        # create an x and y position on the grid
        # cell-number -1 to make sure it doesnt go out of border
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        # 2d vector for easy access and math rather than a list
        self.pos = Vector2(self.x, self.y)

# game logic             
class MAIN:
    def __init__(self):
        # create the fruit and snake
        self.snake = SNAKE()
        self.fruit = FRUIT()
        
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        
    def draw_elements(self):
        #draw fruit and snake
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

        
    def check_collision(self):
        # check whether fruit and snake are in the same pos
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit
            self.fruit.randomize()
            # add another block to the snake
            self.snake.add_block()
            # play crunch
            self.snake.play_sound()
            
        # prevent fruit on snake body
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            
    def check_fail(self):
        # check if snake is outside of screen
        # checks if head is between borders (x)
        if not 0 <= self.snake.body[0].x < cell_number:
            self.game_over()
        elif not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        else: 
            pass
        # check if snake head and snake body has same position
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        
    def game_over(self):
        self.snake.reset()
    
    def draw_grass(self):
        grass_color = (167, 209, 61)
        
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col* cell_size , row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else: 
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col* cell_size , row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        # text, anti alias, color
        score_surface = game_font.render(score_text , False, (56, 74, 12))
        # right bottom
        score_x = int(cell_size*cell_number - 60)
        score_y = int(cell_size*cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
    
        
        # use the rect as a reference for our banana
        banana_rect = banana.get_rect(midright = (score_rect.left - 2, score_rect.top + 8))
        
        
        # background
        bg_rect = pygame.Rect(banana_rect.left, banana_rect.top,banana_rect.width + score_rect.width + 5, banana_rect.height)
        
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface,score_rect )
        screen.blit(banana, banana_rect )
        
        # frame around box
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
    
# remove sound buffer   
pygame.mixer.pre_init(44100, -16, 2, 512)

#LETS MAKE SNAKE!
pygame.init()

#cells of the grid
cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size ))
clock = pygame.time.Clock()

#import banana image
banana = pygame.image.load('banana.png').convert_alpha()

# create a font object
game_font = pygame.font.Font('PixelGameFont.ttf', 25)
# timer for move method
SCREEN_UPDATE = pygame.USEREVENT
# trigger screen update every 150ms
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
            
        # changing movement based off keyboard key input
        # also prevent snake from going into itself 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            
            
        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)
        
    