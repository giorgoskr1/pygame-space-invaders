# imports

import os
import pygame
from random import randrange
import json


pygame.font.init()
pygame.mixer.init()

# globals

# Window + FPS

FPS = 60
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# fixed variables

VEL_Y = 8
MAX_BULLETS = 5
BULLET_VEL = 10
RED_VEL = 1
MAX_RED_SPACESHIPS = 3

# lists which store bullets and spaceships

yellow_bullets = []
red_spaceships = []
red_bullets = []


# Fonts
health_font = pygame.font.SysFont('comicsans', 40)
score_font = pygame.font.SysFont('comicsans', 30)
title_font = pygame.font.SysFont('comicsans', 70)
text_font = pygame.font.SysFont('comicsans', 36)

# folder used to load assets

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# caption

pygame.display.set_caption("Space Invaders 1980")

# colors (rgb)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# loading images

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(THIS_FOLDER, 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (60, 48)), 180)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(THIS_FOLDER, 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (44, 28))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join(THIS_FOLDER, 'space.png')), (WIDTH, HEIGHT))

# loading sound effects

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(THIS_FOLDER, 'grenade1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(THIS_FOLDER, 'gun.mp3'))
CRASH_SOUND = pygame.mixer.Sound(os.path.join(THIS_FOLDER, 'Sound Effect- Crash.mp3'))


def load_high_score():
    try:
        with open('high_score.json') as f:
            high_score = json.load(f)
    except FileNotFoundError:
        with open('high_score.json', 'w') as f:
            json.dump(0, f)
            high_score = 0
    return high_score


# draw functions

def draw_init():
    WIN.blit(SPACE, (0, 0))
    title_text = title_font.render("SPACE INVADERS", 1, YELLOW)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    text = text_font.render("Can you save the world? Press Q to start fighting!", 1, WHITE)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))
    controls = health_font.render("CONTROLS:", 1, WHITE)
    WIN.blit(controls, (WIDTH // 2 - text.get_width() // 2, 150))
    move_text = text_font.render("    MOVE: Left and Right Arrows", 1, WHITE)
    WIN.blit(move_text, (WIDTH // 2 - move_text.get_width() // 2, 180))
    fire_text = text_font.render("    FIRE: Space", 1, WHITE)
    WIN.blit(fire_text, (WIDTH // 2 - text.get_width() // 2 + 105, 210))
    rules_text = text_font.render("RULES:", 1, WHITE)
    WIN.blit(rules_text, (WIDTH // 2 - text.get_width() // 2, 250))
    first = text_font.render("1) You can fire up to 5 bullets each time", 1, WHITE)
    WIN.blit(first, (150, 290))
    second = text_font.render("2) The collision with a red spaceship costs 5HP",1 , WHITE)
    WIN.blit(second, (150, 320))
    third = text_font.render("3) Each red spaceship that gets out of bounds costs you 1HP", 1, WHITE)
    WIN.blit(third, (150, 350))
    forth = text_font.render("4) Each time you are hit by a bullet you will lose 1HP", 1, WHITE)
    WIN.blit(forth, (150, 380))
    l = health_font.render("GOOD LUCK !!!", 1, WHITE)
    WIN.blit(l, (WIDTH // 2 - text.get_width() // 2, 430))
    pygame.display.update()


def draw_end(print_sth, score):
    lost_text = title_font.render("You Lost!", 1, RED)
    WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, 100))
    if print_sth is True:
        score_text = health_font.render(f"Your score: {score} (New High Score!)", 1, WHITE)
    else:
        score_text = health_font.render(f"Your score: {score}", 1, WHITE)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 180))
    final_text = health_font.render("Press Q to try again, S to go to the main menu or Esc to give up", 1, WHITE)
    WIN.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, 250))
    pygame.display.update()


def draw_window(yellow, yellow_bullets, reds, red_bullets, health, score, high):
    WIN.blit(SPACE, (0, 0))

    health_text = health_font.render(f"Health: {str(health)}", 1, WHITE)
    WIN.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))

    score_text = score_font.render(f"Score: {str(score)}", 1, WHITE)
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 40))

    if high:
        new_text = score_font.render("New High Score!!!", 1, WHITE)
        WIN.blit(new_text, (WIDTH - new_text.get_width() - 10, 60))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for red in reds:
        WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for r_bullet in red_bullets:
        pygame.draw.rect(WIN, RED, r_bullet)
    pygame.display.update()


# movement functions


def yellow_movement(keys_pressed, yellow):
    if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and yellow.x + VEL_Y + 60 < WIDTH:
        yellow.x += VEL_Y
    if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and yellow.x - VEL_Y > 0:
        yellow.x -= VEL_Y


def yellow_bullets_movement(yellow_bullets, reds, n, bul, score):
    for bullet in yellow_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y - BULLET_VEL <= 0:
            yellow_bullets.remove(bullet)
            continue
        for red in reds:
            if red.colliderect(bullet):
                reds.remove(red)
                yellow_bullets.remove(bullet)
                BULLET_HIT_SOUND.play()
                if bul >= 2:
                    score += 10
                else:
                    score += n + 2
    return score


def red_spaceships_movement(reds, yellow, vel_var):
    num = 0
    for red in reds:
        if RED_VEL + vel_var > 3:
            red.y += 3
        else:
            red.y += int(RED_VEL + vel_var)
        if red.y + RED_VEL >= HEIGHT:
            reds.remove(red)
            num += 1
        if yellow.colliderect(red):
            num += 5
            CRASH_SOUND.play()
            reds.remove(red)
    return num


def red_bullets_movement(bullets, yellow):
    num = 0
    for bullet in bullets:
        bullet.y += 5
        if bullet.y + 5 >= HEIGHT:
            bullets.remove(bullet)
        if yellow.colliderect(bullet):
            num += 1
            bullets.remove(bullet)
    return num


def main():

    # high score

    high_score = load_high_score()

    # variables

    score = 0
    ok = True
    print_sth = False
    init = True
    end = False
    vel_var = 0
    n_var = 0
    bul_var = 0.0005
    red_bul = 0
    health = 100

    # yellow spaceship

    yellow = pygame.Rect(WIDTH // 2, HEIGHT - 53, 60, 48)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > high_score:
                    with open("high_score.json", "w") as f:
                        json.dump(score, f)
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < 5 and init is False and end is False:
                    bullet = pygame.Rect(yellow.x + 30, yellow.y + 48, 5, 10)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_q and init is True:
                    init = False
                    high_score = load_high_score()
                if event.key == pygame.K_q and end is True:
                    end = False
                    init = False
                    health = 100
                    red_spaceships.clear()
                    red_bullets.clear()
                    yellow_bullets.clear()
                    red_bul = 0
                    vel_var = 0
                    score = 0
                    n_var = 0
                    high_score = load_high_score()
                if event.key == pygame.K_s and end is True:
                    init = True
                    end = False
                    health = 100
                    red_spaceships.clear()
                    red_bullets.clear()
                    yellow_bullets.clear()
                    red_bul = 0
                    vel_var = 0
                    score = 0
                    n_var = 0
                    high_score = load_high_score()
                if event.key == pygame.K_ESCAPE and (end is True or init is True):
                    pygame.quit()
                if event.key == pygame.K_ESCAPE and end is False and init is False:
                    init = False
                    end = True
                    health = 100
                    red_spaceships.clear()
                    red_bullets.clear()
                    yellow_bullets.clear()
                    red_bul = 0
                    vel_var = 0
                    score = 0
                    n_var = 0
        if len(red_spaceships) < int(MAX_RED_SPACESHIPS + n_var) and init is False and end is False:
            red = pygame.Rect(randrange(50, 850, 50), 0, 44, 28)
            if len(red_spaceships) > 0:
                while red.x == red_spaceships[-1].x:
                    red.x = randrange(50, 850, 50)
            red_spaceships.append(red)
            ok = True
        if red_bul >= 2 and len(red_bullets) < 4 and init is False and end is False:
            for red in red_spaceships:
                if ok is True:
                    bullet = pygame.Rect(red.x + 22, red.y + 28, 5, 10)
                    red_bullets.append(bullet)
            ok = False

        if init is False and end is False:
            keys_pressed = pygame.key.get_pressed()
            yellow_movement(keys_pressed, yellow)
            num = red_spaceships_movement(red_spaceships, yellow, vel_var)
            health = health - num
            score = yellow_bullets_movement(yellow_bullets, red_spaceships, int(MAX_RED_SPACESHIPS + n_var), int(red_bul), score)
            num = red_bullets_movement(red_bullets, yellow)
            health = health - num
        if init:
            draw_init()
        elif end:
            draw_end(score > high_score, score)
        else:
            draw_window(yellow, yellow_bullets, red_spaceships, red_bullets, health, score, score > high_score)
        vel_var += 0.0001
        if n_var <= 3:
            n_var += 0.001
        red_bul += bul_var
        if health <= 0:
            if score > high_score:
                with open("high_score.json", "w") as f:
                    json.dump(score, f)
            end = True


if __name__ == '__main__':
    main()