import pygame
import sys
import datetime

from entities import *
from parsing import *

import warnings

from generator import KnapsackRandomGenerator

pygame.init()

parser =  KnapsackParser()
generator = KnapsackRandomGenerator()

MAIN_AREA_X = 300

BACKGROUND_IMAGE = pygame.image.load("images/background.jpg")
ITEM_BOX_IMAGE = pygame.image.load("images/item_box.PNG")

FONT_SMALL = pygame.font.Font('./fonts/Vera.ttf', 14)
FONT_MED = pygame.font.Font('./fonts/Vera.ttf', 20)
FONT_LARGE = pygame.font.Font('./fonts/Vera.ttf', 28)

COLOR_WHITE = (255, 255, 255)

# Define the colors
DARK_BACKGROUND_COLOR = (9, 26, 69)
LIGHT_BACKGROUND_COLOR = (15, 46, 133)


def render_item( screen, item, posx, posy ):
    
    box_height = max( item.weight*2, 64 )

    if box_height == 64:
        screen.blit(ITEM_BOX_IMAGE, (MAIN_AREA_X + posx * 202 + 16, 66 + posy))
    else:
        top_part = ITEM_BOX_IMAGE.subsurface((0, 0, 198, 24))
        screen.blit(top_part, (MAIN_AREA_X + posx * 202 +   16, 66 + posy))
        
        n = box_height - 48
        for i in range(n):
            middle_part = ITEM_BOX_IMAGE.subsurface((0, 32, 198, 1))
            screen.blit(middle_part, (MAIN_AREA_X + posx * 202 +   16, 66 + 24 + i + posy))

        bottom_part = ITEM_BOX_IMAGE.subsurface((0, 40, 198, 24))
        screen.blit(bottom_part, (MAIN_AREA_X + posx * 202 +   16, 66 + 24 + n + posy))

    icon = pygame.transform.scale(
        pygame.image.load(f"images/icons/{item.name}.png"),
        (32, 32))
    screen.blit(icon, (MAIN_AREA_X + posx * 202 +   32, 82 + posy))

    item_name = FONT_SMALL.render(item.name, True, COLOR_WHITE)
    screen.blit(item_name, (MAIN_AREA_X + posx * 202 +   68, 50 + posy + 32))

    item_wv = FONT_SMALL.render("w=" + str(item.weight) + ", v=" + str(item.value), True, COLOR_WHITE)
    screen.blit(item_wv, (MAIN_AREA_X + posx * 202 +   68, 50 + posy + 50 ))

    return box_height
    
def render(screen, knapsack):
    
    # Clear the screen
    #screen.fill((0, 0, 0))
    # Resize the image to fit the screen
    # background = pygame.transform.scale(BACKGROUND_IMAGE, (screen.get_width(), screen.get_height()))
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    screen.blit(FONT_MED.render("L: Load Knapsack", True, COLOR_WHITE), (30, 75))
    screen.blit(FONT_MED.render("X: Exit", True, COLOR_WHITE), (30, 115))

    if knapsack is not None:
        # Draw knapsack capacity
        text = FONT_MED.render("Capacity: " + str(knapsack.capacity), True, COLOR_WHITE)
        screen.blit(text, (MAIN_AREA_X + 32, 26))
        
        # Draw items and their values
        posy = 0
        posx = 0
        for i, item in enumerate(knapsack.items):
            # text = font.render(item.name + ": w=" + str(item.weight) + " v=" + str(item.value), True, COLOR_WHITE)
            # screen.blit(text, (10, 50 + i * 24))
            height = render_item( screen, item, posx, posy )
            posy += height
            if posy > screen.get_height()-250:
                posy = 0
                posx += 1


def main():
    
    # screen = pygame.display.set_mode((800, 600))
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("Knapsack")

    # Display the menu
    render(screen, None)

    clock = pygame.time.Clock()
    knapsack = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.unicode == 'l':
                    # knapsack = parser.from_file("data/k01.kps")
                    knapsack = generator.generate(30)
                    # debug
                    with open(f"data/knapsack_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.kps", "w") as f:
                        f.write(knapsack.to_repr())
                elif event.unicode == 'x':
                    pygame.quit()
                    sys.exit()

        if knapsack:
            # knapsack.update()
            render(screen, knapsack)

        pygame.display.flip()
        clock.tick(60)

# # Background update thread
# def background_update():
#     while True:
#         knapsack.update_values()
#         time.sleep(2)
        
# # Start background thread
# background_thread = threading.Thread(target=background_update)
# background_thread.start()

if __name__=="__main__":
    main()