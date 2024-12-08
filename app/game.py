"""
@file game.py
@brief Gère le déroulement du jeu de Planning Poker.
@version 1.0
@author ldebret & mblanchon
@date 2024-12-08
"""

# Importation des bibliothèques
import pygame
from app.utils import save_backlog, calculate_rule_result, Button

"""
@brief Fonction principale qui gère l'exécution du jeu de Planning Poker.
@details Cette fonction initialise le jeu, affiche les cartes et permet aux joueurs de voter. 
Elle gère également les événements liés à l'affichage des résultats et à la navigation entre les tâches.
@param screen L'écran Pygame sur lequel afficher l'interface du jeu.
@param backlog Liste des tâches à estimer.
@param players Liste des joueurs participant au jeu.
@param rule La règle utilisée pour calculer les résultats des votes.
"""
def run_game(screen, backlog, players, rule):
    pygame.init()
    font = pygame.font.Font(None, 36)
    running = True

    # Charger les images des cartes
    card_values = ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "cafe", "intero"]
    card_images = {value: pygame.image.load(f"assets/cards/{value}.png") for value in card_values}

    # Positionner les cartes sur l'écran
    card_positions = {}
    x_offset = 100
    y_offset = 400
    card_width, card_height = 80, 120  # Taille des cartes
    for i, value in enumerate(card_values):
        card_positions[value] = (x_offset + i * (card_width + 10), y_offset)

    tasks = list(backlog.keys())
    current_task_index = 0
    votes = {}
    current_player_index = 0

    # Création des boutons "Révéler les cartes" et "Suivant"
    reveal_button = Button(500, 600, 200, 50, "Révéler les cartes")
    next_button = Button(500, 700, 200, 50, "Suivant")
    all_voted = False
    cards_revealed = False
    show_pause_message = False

    while running:
        screen.fill((255, 255, 200))

        # Affiche la tâche actuelle
        task = tasks[current_task_index]
        task_text = font.render(f"Tâche: {task}", True, (0, 0, 0))
        screen.blit(task_text, (50, 50))

        # Affiche le joueur actuel
        current_player = players[current_player_index] if current_player_index < len(players) else "Tous ont voté"
        player_text = font.render(f"Joueur actuel: {current_player}", True, (0, 0, 255))
        screen.blit(player_text, (50, 100))

        # Affiche les cartes disponibles si tous n'ont pas voté
        if not all_voted:
            for value, position in card_positions.items():
                screen.blit(card_images[value], position)

        # Affiche les votes déjà enregistrés ou dévoilés
        for i, player in enumerate(players):
            vote = votes.get(player, "Pas encore voté") if cards_revealed else "?"
            vote_text = font.render(f"{player}: {vote}", True, (0, 0, 0))
            screen.blit(vote_text, (50, 150 + i * 30))

        # Affiche les boutons
        if all_voted and not cards_revealed:
            reveal_button.draw(screen)
        if all_voted and cards_revealed and not show_pause_message:
            next_button.draw(screen)

        # Affiche le message de pause café si nécessaire
        if show_pause_message:
            pause_text = font.render("Pause Café !", True, (255, 0, 0))
            screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, 300))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Sauvegarde le backlog avant la fermeture du jeu
                save_backlog(backlog=backlog)
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Enregistre les votes si c'est le tour des joueurs
                if not all_voted:
                    for value, position in card_positions.items():
                        x, y = position
                        if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                            votes[current_player] = "Café" if value == "cafe" else "Intero" if value == "intero" else int(value)
                            current_player_index += 1

                            # Vérifie si tous les joueurs ont voté
                            if current_player_index >= len(players):
                                all_voted = True
                            break

                # Bouton "Révéler les cartes"
                if all_voted and not cards_revealed and reveal_button.is_clicked(event):
                    cards_revealed = True

                # Bouton "Suivant"
                if all_voted and cards_revealed and next_button.is_clicked(event):
                    result = calculate_rule_result(votes, rule)
                    if result == -1:
                        # Réinitialiser les votes et l'index des joueurs
                        votes = {}
                        current_player_index = 0
                        all_voted = False
                        cards_revealed = False
                    elif any(v == "Café" for v in votes.values()):
                        show_pause_message = True
                        pygame.time.set_timer(pygame.USEREVENT, 3000)  # Afficher le message pendant 3 secondes
                    else:
                        backlog[task] = result
                        current_task_index += 1
                        votes = {}
                        current_player_index = 0
                        all_voted = False
                        cards_revealed = False

                        # Vérifie si toutes les tâches sont terminées
                        if current_task_index >= len(tasks):
                            save_backlog(backlog=backlog)
                            running = False

            elif event.type == pygame.USEREVENT and show_pause_message:
                # Masquer le message de pause café après 3 secondes
                show_pause_message = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_backlog(backlog=backlog)
                    running = False
