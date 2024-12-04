# /planning_poker/app/menu.py
import pygame
from app.settings import run_settings
from app.utils import Button

def run_menu(screen):
    running = True
    font = pygame.font.Font(None, 36)

    # Boutons
    start_button = Button(200, 200, 400, 50, "Démarrer une partie")
    quit_button = Button(200, 300, 400, 50, "Quitter l'application")

    while running:
        screen.fill((255, 255, 255))
        
        title = font.render("Planning Poker - Menu Principal", True, (0, 0, 0))
        screen.blit(title, (200, 100))
        
        start_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if start_button.is_clicked(event):
                run_settings(screen)
            if quit_button.is_clicked(event):
                running = False

        pygame.time.wait(100)
