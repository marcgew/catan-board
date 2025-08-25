import pygame
import sys
import math
import random
from dice import load_dice_images, roll_dice_animation

# Bildschirm & Hex
WIDTH, HEIGHT = 1920, 1800
HEX_RADIUS = 120

# Farben
BLACK = (0,0,0)
RED = (255,0,0)
HIGHLIGHT_COLOR = (255,255,0)

# --- Hex-Funktionen ---
def axial_to_pixel(q, r, size, center):
    x = size * math.sqrt(3) * (q + r/2) + center[0]
    y = size * 3/2 * r + center[1]
    return (int(x), int(y))

def draw_hex(surface, center, hex_asset, number=None, highlight_intensity=0):
    hex_surf = pygame.Surface((hex_asset.get_width(), hex_asset.get_height()), pygame.SRCALPHA)
    hex_center = (hex_surf.get_width()//2, hex_surf.get_height()//2)

    # --- Schwarzer Hintergrund-Hex
    size = hex_surf.get_height() // 2
    points = [
        (hex_center[0] + size * math.cos(math.radians(60*i-30)),
         hex_center[1] + size * math.sin(math.radians(60*i-30)))
        for i in range(6)
    ]
    pygame.draw.polygon(hex_surf, (0,0,0), points)  # Schwarzer Hintergrund

    # --- Asset drüber
    hex_surf.blit(hex_asset, (0,0))

    # --- Puls-Rand
    if highlight_intensity > 0:
        border_color = (255,255,0)
        width = int(1 + 2*highlight_intensity)
        border_surf = pygame.Surface((hex_surf.get_width(), hex_surf.get_height()), pygame.SRCALPHA)
        pygame.draw.polygon(border_surf, border_color, points, width)
        hex_surf.blit(border_surf, (0,0))
    else:
        # Optional normale schwarze Umrandung
        width = 1
        pygame.draw.polygon(hex_surf, (0,0,0), points, width)

    # --- Zahl
    if number is not None:
        pygame.draw.circle(hex_surf, (255,255,255), hex_center, 18)
        color_num = (255,0,0) if number in (6,8) else (0,0,0)
        font = pygame.font.SysFont("Arial", 18, bold=True)
        num_surface = font.render(str(number), True, color_num)
        num_rect = num_surface.get_rect(center=hex_center)
        hex_surf.blit(num_surface, num_rect)

    # Blit auf Hauptsurface
    surf_rect = hex_surf.get_rect(center=center)
    surface.blit(hex_surf, surf_rect)


# --- Ressourcen / Zahlen ---
def generate_catan_coords():
    coords = []
    for r in range(-2, 3):
        for q in range(-2, 3):
            if -2 <= q + r <= 2:
                coords.append((q,r))
    return coords

def randomize_resources():
    resources = ["forest"]*4 + ["field"]*4 + ["mountain"]*3 + ["pasture"]*4 + ["brick"]*3 + ["desert"]
    random.shuffle(resources)
    return resources

def randomize_numbers(resources):
    numbers = [5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]
    result = []
    n_index = 0
    for res in resources:
        if res == "desert":
            result.append(None)
        else:
            result.append(numbers[n_index])
            n_index += 1
    return result

# --- Main ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Catan Board - 6 Assets & Würfel")
    clock = pygame.time.Clock()
    center_screen = (WIDTH//2, HEIGHT//2)

    ASSETS = {
        "forest": "assets/forest.png",
        "field": "assets/field.png",
        "mountain": "assets/mountain.png",
        "pasture": "assets/pasture.png",
        "brick": "assets/brick.png",
        "desert": "assets/desert.png"
    }

    hex_assets = {}
    for key, path in ASSETS.items():
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (HEX_RADIUS*2,HEX_RADIUS*2))
        hex_assets[key] = img

    coords = generate_catan_coords()
    resources = randomize_resources()
    numbers = randomize_numbers(resources)

    dice_images = load_dice_images()
    highlight_number = None

    running = True
    while running:
        screen.fill((100,149,237))  # Meer

        # Pulswert
        t = pygame.time.get_ticks() / 500
        pulse = (math.sin(t*math.pi*2)+1)/2

        # Hexes zeichnen
        for i, (q,r) in enumerate(coords):
            pos = axial_to_pixel(q,r,HEX_RADIUS, center_screen)
            res = resources[i]
            num = numbers[i]
            draw_hex(screen, pos, hex_assets[res], number=num,
                     highlight_intensity=pulse if num==highlight_number else 0)

      

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    highlight_number = roll_dice_animation(screen, (100, HEIGHT-500), dice_images)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
