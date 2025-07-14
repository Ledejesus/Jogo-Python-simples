import pgzrun
from random import randint
from pygame import Rect
from config import *

game_state = "menu"
hero = Actor('hero_idle1', (100, 300))
hero.vy = 0
hero.on_ground = True
hero.anim_index = 0
hero.anim_timer = 0

enemies = []
boss = None
coin = None
music_on = True
score = 0
lives = 3
current_level = 1

def reset_game():
    global hero, enemies, coin, game_state, score, lives, current_level, boss
    hero.x, hero.y = 100, 300
    hero.vy = 0
    hero.on_ground = True
    score = 0
    lives = 3
    current_level = 1
    spawn_enemies()
    coin = Actor("coin", (700, 280))
    boss = None
    game_state = "playing"

def spawn_enemies():
    global enemies
    enemies = []
    for _ in range(3):
        enemy = Actor("enemy_walk1", (randint(300, WIDTH - 50), 300))
        enemy.vx = randint(-2, 2)
        enemies.append(enemy)

def draw():
    screen.clear()
    if game_state == "menu":
        screen.fill((100, 100, 255))
        draw_menu()
    elif game_state == "playing":
        screen.blit('background', (0, 0))
        hero.draw()
        if current_level == 1:
            for e in enemies:
                e.draw()
            if coin:
                coin.draw()
        elif current_level == 2:
            boss.draw()
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
        screen.draw.text(f"Lives: {lives}", (10, 50), fontsize=30, color="white")
    elif game_state == "gameover":
        screen.fill((30, 0, 0))
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")
        screen.draw.text("Press ENTER to try again", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")
    elif game_state == "win":
        screen.fill((0, 100, 0))
        screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="yellow")
        screen.draw.text("Press ENTER to play again", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")

def update(dt):
    global game_state, score, lives, current_level, boss, coin
    if game_state == "playing":
        update_hero(dt)
        if current_level == 1:
            update_enemies(dt)
            for e in enemies:
                if hero.colliderect(e):
                    lives -= 1
                    hero.x = 100
                    hero.y = 300
                    sounds.hit.play()
                    if lives <= 0:
                        game_state = "gameover"
            if coin and hero.colliderect(coin):
                score += 10
                current_level = 2
                boss = Actor("enemy_walk1", (WIDTH // 2, 300))
                boss.vx = 3
                coin = None
                sounds.coin.play()
        elif current_level == 2:
            boss.x += boss.vx
            if boss.left < 0 or boss.right > WIDTH:
                boss.vx *= -1
            if hero.colliderect(boss):
                lives -= 1
                hero.x = 100
                hero.y = 300
                sounds.hit.play()
                if lives <= 0:
                    game_state = "gameover"
            elif hero.x > WIDTH - 50:
                score += 20
                game_state = "win"
                sounds.coin.play()

def draw_menu():
    screen.draw.text("My Platformer Game", center=(WIDTH // 2, 100), fontsize=40, color="white")
    screen.draw.text("1. Start Game", center=(WIDTH // 2, 200), fontsize=30, color="yellow")
    screen.draw.text("2. Toggle Music", center=(WIDTH // 2, 250), fontsize=30, color="yellow")
    screen.draw.text("3. Exit", center=(WIDTH // 2, 300), fontsize=30, color="yellow")

def on_key_down(key):
    global game_state, music_on
    if game_state == "menu":
        if key == keys.K_1:
            reset_game()
            if music_on:
                music.play('bg_music')
        elif key == keys.K_2:
            music_on = not music_on
            if music_on:
                music.play('bg_music')
            else:
                music.stop()
        elif key == keys.K_3:
            exit()
    elif game_state in ["gameover", "win"]:
        if key == keys.RETURN:
            reset_game()

def update_hero(dt):
    if keyboard.left:
        hero.x -= 5
    if keyboard.right:
        hero.x += 5
    if keyboard.space and hero.on_ground:
        hero.vy = -12
        hero.on_ground = False
        sounds.jump.play()

    hero.vy += 0.5
    hero.y += hero.vy

    if hero.y >= 300:
        hero.y = 300
        hero.vy = 0
        hero.on_ground = True

    hero.anim_timer += dt
    if hero.anim_timer > 0.2:
        hero.anim_index = (hero.anim_index + 1) % 2
        hero.image = f"hero_idle{hero.anim_index + 1}"
        hero.anim_timer = 0

def update_enemies(dt):
    for enemy in enemies:
        enemy.x += enemy.vx
        if enemy.left < 0 or enemy.right > WIDTH:
            enemy.vx *= -1

pgzrun.go()
