# /planning_poker/main.py
import pygame
from app.menu import run_menu
from app.utils import save_backlog

# Pygame setup
pygame.init()
WINDOW_SIZE = (1400, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Planning Poker")

# Main loop
def main():
    try:
        run_menu(screen)
    except KeyboardInterrupt:
        print("Fin de l'application.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
