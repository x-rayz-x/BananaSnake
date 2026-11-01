import pygame
import sys

# initializes pygame modules
pygame.init()
# create a window
screen = pygame.display.set_mode((400, 500))

# create clock object(to vary while loop speed for different computers)
clock = pygame.time.Clock()

# test 
test_surface = pygame.Surface((100, 200))
test_surface.fill(pygame.Color("blue"))

# make a rectangle (x,y,w,h)
test_rectangle = pygame.Rect(100, 200, 100, 100)

# make a rectangle from surface (position=( x, y))
test_rectangle = test_surface.get_rect(center = (200, 250))

while True:
    # look through every possible event
    for event in pygame.event.get():
        # event type (exit)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # color the screen
    screen.fill(pygame.Color("gold"))
    # RGB tuple
    screen.fill((175, 215, 70))
    
    # draw the rect (surface, color, rectangle)
    pygame.draw.rect(screen, pygame.Color("red") , test_rectangle)
    
    #move to the right
    test_rectangle.right += 1
    
    # show the surface (x,y)
    # center is top left, so for y increase goes downward and decrease goes upward
    
    # we created a new surface, drew a rectange around it, put it in the center, and placed the surface around the rectangle
    screen.blit(test_surface,test_rectangle)
    
    #updates the display  (draws elements)
    pygame.display.update()
    
    # change tick (framerate)
    clock.tick(60)
    
''' Display surface - canvas
# surface - a layer that shows graphics (multiple) 
# text, image, empty space, sprites 

Rect - a rectangle used for drawing and placement'''