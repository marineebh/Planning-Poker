"""
@file settings.py
@brief Gère les paramètres et les réglages du jeu, y compris la configuration du backlog, des joueurs et de la règle de calcul.
@version 1.0
@author ldebret & mblanchon
@date 2024-12-08
"""

# Importation des bibliothèques
import pygame
from app.game import run_game
from app.utils import load_backlog, load_cards, Button

"""
@brief Fonction principale pour gérer les réglages avant de commencer la partie.
@details Cette fonction permet de configurer les paramètres du jeu, notamment le backlog, les joueurs et la règle de calcul. Elle permet également de lancer la partie lorsque tous les paramètres sont définis.
@param screen L'écran Pygame sur lequel afficher les réglages du jeu.
"""
def run_settings(screen):
    backlog = {}
    players = []
    rule = "Unanimité"
    cards = load_cards("assets/cards")
    font = pygame.font.Font(None, 36)
    input_active = False
    input_text = ""
    running = True

    # Création des boutons pour interagir avec l'utilisateur
    load_backlog_button = Button(200, 200, 400, 50, "Charger un backlog")
    create_player_button = Button(200, 300, 400, 50, "Ajouter un joueur")
    start_game_button = Button(200, 400, 400, 50, "Commencer la partie")
    rule_button = Button(200, 500, 400, 50, f"Règle: {rule}")

    # Zone de saisie pour l'ajout de joueurs
    input_box = pygame.Rect(200, 350, 400, 50)
    color_inactive = pygame.Color('lightskyblue')
    color_active = pygame.Color('dodgerblue')
    color = color_inactive

    while running:
        screen.fill((200, 200, 255))
        
        # Affichage du titre
        title = font.render("Réglages", True, (0, 0, 0))
        screen.blit(title, (200, 100))

        # Affichage des boutons
        load_backlog_button.draw(screen)
        create_player_button.draw(screen)
        start_game_button.draw(screen)
        rule_button.draw(screen)
        
        # Affichage des joueurs ajoutés
        for i, player in enumerate(players):
            player_name = font.render(player, True, (0, 0, 0))
            screen.blit(player_name, (600, 200 + 30 * i))

        # Affichage de la zone de saisie si elle est active
        if input_active:
            pygame.draw.rect(screen, color, input_box, 2)
            text_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Vérification des clics de boutons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_backlog_button.is_clicked(event):
                    print(f"Chargement du backlog: {backlog}")
                    backlog = load_backlog()
                    print(f"Backlog chargé: {backlog}")
                
                if create_player_button.is_clicked(event):
                    input_active = True
                    color = color_active
                    print("Bouton Ajouter un joueur cliqué")
                
                if start_game_button.is_clicked(event) and backlog and players:
                    print(f"Début de partie - Backlog: {backlog}")
                    print(f"Nombre de joueurs: {len(players)}")
                    if start_game_button.is_clicked(event):
                        print("Bouton Commencer cliqué")
                        if backlog and players:
                            print("Conditions remplies pour lancer la partie")
                            run_game(screen, backlog, players, rule)
                
                if rule_button.is_clicked(event):
                    rule = "Médiane" if rule == "Unanimité" else "Moyenne" if rule == "Médiane" else "Unanimité"
                    rule_button.text = f"Règle: {rule}"

            # Gestion de la saisie de texte pour l'ajout de joueurs
            if input_active and event.type == pygame.TEXTINPUT:
                input_text += event.text

            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.strip():
                    players.append(input_text.strip())
                    print(f"Player added: {input_text}")
                    input_text = ""
                    input_active = False
                    color = color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

        pygame.time.wait(100)
