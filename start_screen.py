#Start Screen

import pygame
from pygame.locals import *
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
# Game Resolution
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# Text Renderer
def text_format(message, textSize, textColor):
    newFont = pygame.font.Font(None, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Game Framerate
clock = pygame.time.Clock()
FPS = 30


def main_menu():
    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if selected == "start":
                    if event.key == pygame.K_UP:
                        selected = "start"
                    elif event.key == pygame.K_DOWN:
                        selected = "tutorial"
                elif selected == "tutorial":
                    if event.key == pygame.K_UP:
                        selected = "start"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                elif selected == "quit":
                    if event.key == pygame.K_UP:
                        selected = "tutorial"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        print("Start")
                    if selected == "tutorial":
                        print("Tutorial")
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(blue)
        title = text_format("Weather Surfer", 90, yellow)
        if selected == "start":
            text_start = text_format("START", 75, white)
        else:
            text_start = text_format("START", 75, black)
        if selected == "quit":
            text_quit = text_format("QUIT", 75, white)
        else:
            text_quit = text_format("QUIT", 75, black)
        if selected == "tutorial":
            text_tutorial = text_format("TUTORIAL", 75, white)
        else:
            text_tutorial = text_format("TUTORIAL", 75, black)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        tutorial_rect = text_tutorial.get_rect()
        quit_rect = text_quit.get_rect()
        # Main Menu Text
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_tutorial, (screen_width / 2 - (tutorial_rect[2] / 2), 360))
        screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2), 420))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")


main_menu()
pygame.quit()
quit()
