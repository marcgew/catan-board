import random

# Farben für Ressourcen
COLORS = {
    "Holz": (34, 139, 34),
    "Lehm": (205, 92, 92),
    "Wolle": (144, 238, 144),
    "Getreide": (255, 215, 0),
    "Erz": (169, 169, 169),
    "Wüste": (210, 180, 140),
}

def generate_catan_coords():
    """Koordinaten 19 Felder (Standard-Catan)"""
    coords = [(0, 0)]  # Mitte
    coords += [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    coords += [(2, 0), (2, -1), (2, -2), (1, -2), (0, -2), (-1, -1),
               (-2, 0), (-2, 1), (-2, 2), (-1, 2), (0, 2), (1, 1)]
    return coords

def randomize_resources():
    """Ressourcen Ori Verteilung"""
    resources = (
        ["Holz"] * 4 +
        ["Getreide"] * 4 +
        ["Wolle"] * 4 +
        ["Lehm"] * 3 +
        ["Erz"] * 3 +
        ["Wüste"] * 1
    )
    random.shuffle(resources)
    return resources

def randomize_numbers(resources):
    """Zufällige Zahlenchips (18)"""
    numbers = (
        [2, 12] +
        [3, 3, 4, 4, 5, 5, 6, 6,
         8, 8, 9, 9, 10, 10, 11, 11]
    )
    random.shuffle(numbers)

    number_map = []
    num_index = 0
    for res in resources:
        if res == "Wüste":
            number_map.append(None)  # Keine Zahl auf der Wüste
        else:
            number_map.append(numbers[num_index])
            num_index += 1
    return number_map