import pygame
from pygame.locals import *

import sys
import datetime

from entities import *
from parsing import *
from environment import *
from agent import *

import warnings

from generator import KnapsackRandomGenerator

import threading

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
COLOR_GRAY = (128, 128, 128)

# Define the colors
DARK_BACKGROUND_COLOR = (9, 26, 69)
LIGHT_BACKGROUND_COLOR = (15, 46, 133)

env = KnapsackEnv()
agent = KnapsackRandomAgent(env)

def render_item( screen, item, posx, posy, selected, pointer ):
    
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

    color = COLOR_WHITE if selected else COLOR_GRAY

    item_name = FONT_SMALL.render(item.name, True, color)
    screen.blit(item_name, (MAIN_AREA_X + posx * 202 +   68, 50 + posy + 32))

    item_wv = FONT_SMALL.render("w=" + str(item.weight) + ", v=" + str(item.value), True, color)
    screen.blit(item_wv, (MAIN_AREA_X + posx * 202 +   68, 50 + posy + 50 ))

    # draw pointer for current_pos
    if ( pointer ):
        pygame.draw.circle(screen, (255, 0, 0), (MAIN_AREA_X + posx * 202 + 190, 66 + posy + box_height - 20), 5 )


    return box_height
    
def render(screen, env):
    
    # Clear the screen
    #screen.fill((0, 0, 0))
    # Resize the image to fit the screen
    # background = pygame.transform.scale(BACKGROUND_IMAGE, (screen.get_width(), screen.get_height()))
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    screen.blit(FONT_MED.render("L: Load Knapsack", True, COLOR_WHITE), (30, 75))
    screen.blit(FONT_MED.render("X: Exit", True, COLOR_WHITE), (30, 115))
    screen.blit(FONT_MED.render("------------------", True, COLOR_WHITE), (30, 140))

    if env is not None:
        if env.knapsack is not None:

            # Draw knapsack capacity
            text = FONT_MED.render("Capacity: " + str(env.knapsack.capacity), True, COLOR_WHITE)
            screen.blit(text, (MAIN_AREA_X + 32, 26))
            
            # Draw items and their values
            posy = 0
            posx = 0
            for i, item in enumerate(env.knapsack.items):
                # text = font.render(item.name + ": w=" + str(item.weight) + " v=" + str(item.value), True, COLOR_WHITE)
                # screen.blit(text, (10, 50 + i * 24))
                height = render_item( screen, item, posx, posy,
                                env.selected_items[i] == ITEM_SELECTED,
                                env.current_pos == i )
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
            
            # menu actions

                if event.unicode == 'l':
                    # knapsack = parser.from_file("data/k01.kps")
                    # env.reset( generator.generate(30) )
                    
                    threading.Thread(target=lambda: agent.play(n_episodes=1000, n_max_steps_per_episode=1000)).start()

                    # @TODO LAUNCH IN SEPARATE THREAD TO AVOID BLOCKING!!!

                    # debug:
                    # with open(f"data/knapsack_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.kps", "w") as f:
                    #     f.write(env.knapsack.to_repr())

                elif event.unicode == 'x':
                    pygame.quit()
                    sys.exit()

            # environment actions
                elif event.key == K_UP:
                    env.step(ACTION_UP)
                elif event.key == K_DOWN:
                    env.step(ACTION_DOWN)
                elif event.unicode == 's':
                    env.step(ACTION_SELECT)
                elif event.unicode == 'u':
                    env.step(ACTION_UNSELECT)
        
        clock.tick(60)

        if env:
            # knapsack.update()
            render(screen, env)

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