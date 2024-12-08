# /planning_poker/app/utils.py
import json
import statistics

def load_backlog(filepath="backlog_json/backlog_exemple.json"):
    try:
        print(f"Tentative de chargement du fichier : {filepath}")
        with open(filepath, "r", encoding='utf-8') as file:
        #with open(f"E:/s1/3conception_agile/CAPI/V5/app/backlog_exemple.json", "r", encoding='utf-8') as file:
            data = json.load(file)
            print(f"Fichier chargé avec succès. Contenu : {data}")
            return data
    except FileNotFoundError:
        print(f"Fichier non trouvé : {filepath}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
        return {}



def save_backlog(file_path, backlog):
    with open(file_path, 'w') as f:
        # Serialize the dictionary into a single JSON string and write it in one go
        json_data = json.dumps(backlog)
        f.write(json_data)

        

def load_cards(filepath):
    """
    Load the cards from a JSON file.
    Returns a default card set if the file is not found or invalid.
    """
    try:
        with open("{filepath}/cards.json", "r") as file:
            data = json.load(file)
            return data.get("cards", ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "café", "intero"])
    except FileNotFoundError:
        print("Cartes introuvables, utilisation des cartes par défaut.")
        return ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "café", "intero"]

def calculate_rule_result(votes, rule):
    values = [v for v in votes.values() if isinstance(v, int)]
    if not values:
        return -1  # No valid votes
    if rule == "Unanimité":
        return values[0] if len(set(values)) == 1 else -1
    elif rule == "Médiane":
        return statistics.median(values)
    elif rule == "Moyenne":
        return round(sum(values) / len(values), 2)
    return -1



# /planning_poker/app/utils.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, color=(0, 128, 0), hover_color=(0, 255, 0), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            return self.rect.collidepoint(event.pos)
        return False
