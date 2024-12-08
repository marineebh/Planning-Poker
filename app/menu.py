"""
@file menu.py
@brief Gère l'affichage du menu principal de l'application Planning Poker.
@version 1.0
@author ldebret & mblanchon
@date 2024-12-08
"""

# Importation des bibliothèques
import pygame
from app.settings import run_settings
from app.utils import Button

"""
@brief Fonction principale du menu de l'application Planning Poker.
@details Cette fonction gère l'affichage du menu principal, avec les options "Démarrer une partie" et "Quitter l'application".
Elle attend l'interaction de l'utilisateur et lance l'action correspondante (démarrer le jeu ou quitter l'application).
@param screen L'écran Pygame sur lequel afficher le menu.
"""
def run_menu(screen):
    running = True
    font = pygame.font.Font(None, 36)

    # Création des boutons "Démarrer une partie" et "Quitter l'application"
    start_button = Button(200, 200, 400, 50, "Démarrer une partie")
    quit_button = Button(200, 300, 400, 50, "Quitter l'application")

    while running:
        screen.fill((255, 255, 255))
        
        # Affiche le titre du menu
        title = font.render("Planning Poker - Menu Principal", True, (0, 0, 0))
        screen.blit(title, (200, 100))
        
        # Affiche les boutons
        start_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quitte l'application
                running = False
            if start_button.is_clicked(event):
                # Lance les paramètres du jeu
                run_settings(screen)
            if quit_button.is_clicked(event):
                # Quitte l'application
                running = False

        pygame.time.wait(100)
