import pygame
import random
import os

def load_dice_images():
    """Lädt Würfelbilder 1-6"""
    dice_images = []
    for i in range(1,7):
        path = os.path.join("assets", f"dice{i}.png")
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.smoothscale(image, (60, 60))
        dice_images.append(image)
    return dice_images

last_dice = (1,1)  # initial

def roll_dice_animation(screen, position, dice_images, rolls=6, hex_radius=120):
    clock = pygame.time.Clock()
    dice1, dice2 = last_dice = (1,1)

    dice_size = int(hex_radius / 2)
    dice_images_scaled = [pygame.transform.smoothscale(img, (dice_size, dice_size)) for img in dice_images]
    spacing = int(dice_size * 1.2)

    for _ in range(rolls):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        last_dice = (dice1, dice2)

        # Würfelgrafiken während Animation
        screen.blit(dice_images_scaled[dice1-1], position)
        screen.blit(dice_images_scaled[dice2-1], (position[0]+spacing, position[1]))

        pygame.display.flip()
        pygame.time.delay(150)
        clock.tick(60)

    return last_dice, dice1 + dice2

