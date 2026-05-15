import random
import pygame
import sys
import os

# ----------------------------- Configurações Iniciais -----------------------------
width, height = 800, 600
text_color = (0, 255, 255)
commands_color = (255, 0, 0)
shots_color = (255, 50, 50)

state_display = "MENU"
game_run = True

# ----------------------------- Variáveis Globais do Jogo -----------------------------
gamer = {"rect": pygame.Rect(0, 0, 70, 50), "vel": 5}
shots = []
aliens = []
direction_aliens = 1
vel_alien_x = 2
vel_alien_y = 15
score = 0

# Variáveis para armazenar as imagens
background_menu = None
background_game = None
background_gameover = None
img_gamer = None
img_alien = None
sound_shot = None
sound_hit = None
sound_gameover = None
sound_start = None

# def apply_color_filter(image, color):
#     tinted_image = image.copy()
#     overlay = pygame.Surface(tinted_image.get_size(), pygame.SRCALPHA)
#     overlay.fill(color)
#     tinted_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
#     return tinted_image


# ----------------------------- Escolhe uma imagem para ser o fundo do jogo -----------------------------
def choice_background_level():
    global background_game
    folder_path = "assets/images/background"

    try:
        if os.path.exists(folder_path):
            backgrounds = os.listdir(folder_path)
            # Filtra apenas arquivos de imagem válidos
            list_background_game = [bg for bg in backgrounds if bg.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if list_background_game:
                chosen_background_game = random.choice(list_background_game)
                path_background_game = os.path.join(folder_path, chosen_background_game)
                render_background_game = pygame.image.load(path_background_game).convert()
                dark_overlay = pygame.Surface(render_background_game.get_size())
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(150)

                render_background_game.blit(dark_overlay, (0, 0))
                background_game = pygame.transform.scale(render_background_game, (width, height))
        else:
            print("Aviso: Diretório de fundos não encontrado.")
    except Exception as e:
        print(f"Erro ao selecionar fundo: {e}")


# ----------------------------- Inicializar -----------------------------
def boot():
    global img_gamer, img_alien, sound_shot, sound_hit, sound_gameover, sound_start, background_menu, background_game, background_gameover
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SkyWalkers Invaders")
    time_clock = pygame.time.Clock()

    try:
        path_img_gamer = pygame.image.load("assets/images/gamer.png").convert_alpha()
        path_img_alien = pygame.image.load("assets/images/enemy.png").convert_alpha()
        path_background_menu = pygame.image.load('assets/images/menu.png').convert()
        path_background_gameover = pygame.image.load('assets/images/menu.png').convert()

        # Ajusta a escala da imagem
        img_gamer = pygame.transform.scale(path_img_gamer, (gamer["rect"].width, gamer["rect"].height))

        # change_enemy_color = apply_color_filter(path_img_alien, (57, 255, 20, 255))
        # img_alien = pygame.transform.scale(change_enemy_color, (40, 30))
        img_alien = pygame.transform.scale(path_img_alien, (40, 30))
        background_menu = pygame.transform.scale(path_background_menu, (width, height))
        background_gameover = pygame.transform.scale(path_background_gameover, (width, height))

        choice_background_level()

        sound_shot = pygame.mixer.Sound("assets/sounds/shot.wav")
        sound_shot.set_volume(0.3)
        sound_hit = pygame.mixer.Sound("assets/sounds/hit.wav")
        sound_hit.set_volume(0.3)
        sound_gameover = pygame.mixer.Sound("assets/sounds/gameover.mp3")
        sound_gameover.set_volume(0.3)
        sound_start = pygame.mixer.Sound("assets/sounds/start.wav")
        sound_start.set_volume(0.3)

    except Exception as e:
        print(f"Aviso: Arquivos não encontrados ou erro de carregamento: {e}")

    return screen, time_clock


# ----------------------------- Cria mais ondas -----------------------------
def create_aliens():
    global aliens
    aliens.clear()
    for line in range(4):
        for column in range(10):
            alien_x = 50 + column * 60
            alien_y = 50 + line * 40
            aliens.append(pygame.Rect(alien_x, alien_y, 40, 30))


# ----------------------------- Reinicia jogo -----------------------------
def reset_game():
    global shots, direction_aliens, score, vel_alien_x
    gamer["rect"].x = width // 2 - 25
    gamer["rect"].y = height - 60
    vel_alien_x = 2
    shots.clear()
    direction_aliens = 1
    score = 0
    choice_background_level()
    create_aliens()


# ----------------------------- Menu -----------------------------
def screen_menu(screen):
    global state_display, background_menu
    screen.blit(background_menu, (0, 0))

    try:
        font_title = pygame.font.Font("assets/fonts/Starjout.ttf", 55)
        font_sub = pygame.font.Font("assets/fonts/sub_title.ttf", 25)
    except:
        font_title = pygame.font.SysFont("Arial", 60, bold=True)
        font_sub = pygame.font.SysFont("Arial", 30)

    title_text = font_title.render("SkyWalkers Invaders", True, (255, 232, 31))
    text_sub = font_sub.render("PRESSIONE ESPAÇO PARA JOGAR", True, text_color)


    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 80))
    screen.blit(text_sub, (width // 2 - text_sub.get_width() // 2, height // 2 + 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if sound_start: sound_start.play()
                reset_game()
                state_display = "JOGO"


# ----------------------------- Jogo -----------------------------
def screen_game(screen):
    global state_display, direction_aliens, score, vel_alien_x, background_game
    screen.blit(background_game, (0, 0))

    # Processa ao eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(shots) < 5:
                    new_shots = pygame.Rect(gamer["rect"].centerx - 2, gamer["rect"].top, 4, 15)
                    shots.append(new_shots)
                    if sound_shot:
                        sound_shot.play()

    # Movimentação do jogador
    key_map = pygame.key.get_pressed()
    if key_map[pygame.K_LEFT] and gamer["rect"].left > 0:
        gamer["rect"].x -= gamer["vel"]
    if key_map[pygame.K_RIGHT] and gamer["rect"].right < width:
        gamer["rect"].x += gamer["vel"]

    for shot in shots[:]:
        shot.y -= 10
        if shot.bottom < 0:
            shots.remove(shot)

    # Lógica de movimentação dos aliens
    limit = False
    for alien in aliens:
        alien.x += vel_alien_x * direction_aliens
        if alien.right >= width or alien.left <= 0:
            limit = True

    if limit:
        direction_aliens *= -1
        for alien in aliens:
            alien.y += vel_alien_y
            if alien.bottom >= gamer["rect"].top:
                state_display = "GAMEOVER"
                if sound_gameover: sound_gameover.play()

    # Verifica a colisão do tiro
    for shot in shots[:]:
        for alien in aliens[:]:
            if shot.colliderect(alien):
                if shot in shots: shots.remove(shot)
                if alien in aliens: aliens.remove(alien)
                score += 10
                if sound_hit: sound_hit.play()
                break

    # Se limpara a tela passa de fase
    if len(aliens) == 0:
        vel_alien_x += 1
        create_aliens()
        choice_background_level()
        screen.blit(background_game, (0, 0))

    # Faz os desenhos na tela
    if img_gamer:
        screen.blit(img_gamer, gamer["rect"])
    else:
        pygame.draw.rect(screen, (0, 255, 0), gamer["rect"])

    for shot in shots:
        pygame.draw.rect(screen, shots_color, shot)

    for alien in aliens:
        if img_alien:
            screen.blit(img_alien, alien)
        else:
            pygame.draw.rect(screen, (230, 60, 90), alien)

    # Pontuação
    font_score = pygame.font.SysFont("Arial", 25)
    screen.blit(font_score.render(f"PONTOS: {score}", True, text_color), (10, 10))


# ----------------------------- Game Over -----------------------------
def screen_gameover(screen):
    global state_display, score, background_gameover
    screen.blit(background_gameover, (0, 0))
    font_sub = pygame.font.SysFont("Arial", 30)

    try:
        font_title = pygame.font.Font("assets/fonts/Starjout.ttf", 55)
    except:
        font_title = pygame.font.SysFont("Arial", 70, bold=True)

    title_text = font_title.render("GAME OVER", True, text_color)
    text_score = font_sub.render(f"PONTUAÇÃO FINAL: {score}", True, shots_color)
    text_sub = font_sub.render("PRESSIONE 'R' PARA RECOMEÇAR", True, text_color)

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 60))
    screen.blit(text_score, (width // 2 - text_score.get_width() // 2, height // 2 + 20))
    screen.blit(text_sub, (width // 2 - text_sub.get_width() // 2, height // 2 + 70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if sound_start: sound_start.play()
                state_display = "MENU"


# ----------------------------- Loop Principal -----------------------------
screen, time_clock = boot()

while game_run:
    if state_display == "MENU":
        screen_menu(screen)
    elif state_display == "JOGO":
        screen_game(screen)
    elif state_display == "GAMEOVER":
        screen_gameover(screen)

    pygame.display.flip()
    time_clock.tick(60)