# /planning_poker/app/game.py
import pygame
from app.utils import save_backlog, calculate_rule_result

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

    while running:
        screen.fill((255, 255, 200))
        
        # Affiche la tâche actuelle
        task = tasks[current_task_index]
        task_text = font.render(f"Tâche: {task}", True, (0, 0, 0))
        screen.blit(task_text, (50, 50))

        # Affiche le joueur actuel
        current_player = players[current_player_index]
        player_text = font.render(f"Joueur actuel: {current_player}", True, (0, 0, 255))
        screen.blit(player_text, (50, 100))

        # Affiche les cartes disponibles
        for value, position in card_positions.items():
            screen.blit(card_images[value], position)

        # Affiche les votes déjà enregistrés
        for i, player in enumerate(players):
            vote = votes.get(player, "Pas encore voté")
            vote_text = font.render(f"{player}: {vote}", True, (0, 0, 0))
            screen.blit(vote_text, (50, 150 + i * 30))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_backlog("backlog.json", backlog)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for value, position in card_positions.items():
                    x, y = position
                    if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                        # Enregistre le vote
                        votes[current_player] = "Café" if value == "cafe" else "Intero" if value == "intero" else int(value)
                        current_player_index += 1

                        # Vérifie si tous les joueurs ont voté
                        if current_player_index >= len(players):
                            result = calculate_rule_result(votes, rule)
                            backlog[task] = result
                            current_task_index += 1
                            votes = {}
                            current_player_index = 0

                            # Vérifie si toutes les tâches sont terminées
                            if current_task_index >= len(tasks):
                                save_backlog("backlog_final.json", backlog)
                                running = False
                        break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_backlog("backlog.json", backlog)
                    running = False
