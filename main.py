import pygame
import sys

# ----------------------------- Configurações Iniciais -----------------------------
width, height = 800, 600
background_color_menu = (50, 0, 50)
background_color_game = (10, 10, 30)
background_color_gameover = (100, 0, 0)
text_color = (255, 255, 255)
commands_color = (120, 162, 200)

# Cores dos Elementos provisórios

shots_color = (255, 50, 50)

# Variáveis de Controle de Estado
state_display = "MENU"
game_run = True

# ----------------------------- Variáveis Globais do Jogo -----------------------------
gamer = {"rect": pygame.Rect(0, 0, 50, 40), "vel": 5}
shots = []
aliens = []
direction_aliens = 1  # 1 para direita, -1 para esquerda
vel_alien_x = 2  # Velocidade horizontal da horda
vel_alien_y = 15  # Quanto a horda desce ao bater na parede
score = 0

# Variáveis para armazenar as imagens
img_gamer = None
img_alien = None
sound_shot = None

# ----------------------------- Inicializar -----------------------------
def boot():
    global img_gamer, img_alien, sound_shot
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SkyWalkers Invaders")
    time_clock = pygame.time.Clock()

    try:
        path_img_gamer = pygame.image.load("assets/gamer.png").convert_alpha()
        path_img_alien = pygame.image.load("assets/enemy.png").convert_alpha()

        # Ajusta a escala da imagem para o tamanho do retângulo de colisão
        img_gamer = pygame.transform.scale(path_img_gamer, (gamer["rect"].width, gamer["rect"].height))
        img_alien = pygame.transform.scale(path_img_alien, (40, 30))

        sound_shot = pygame.mixer.Sound("assets/shot.wav")
        sound_shot.set_volume(0.3)

    except:
        print("Aviso: Arquivos de imagem não encontrados. Usando retângulos coloridos.")

    return screen, time_clock

# ----------------------------- Cria mais ondas -----------------------------
def create_aliens():
    # Gera a formação inicial de inimigos
    global aliens
    aliens.clear()
    for line in range(4):
        for column in range(10):
            alien_x = 50 + column * 60
            alien_y = 50 + line * 40
            aliens.append(pygame.Rect(alien_x, alien_y, 40, 30))

# ----------------------------- Reinicia  jogo -----------------------------
def reset_game():
    # Prepara as variáveis para um novo jogo
    global shots, direction_aliens, score, vel_alien_x
    gamer["rect"].x = width // 2 - 25
    gamer["rect"].y = height - 50
    vel_alien_x = 2
    shots.clear()
    direction_aliens = 1
    score = 0
    create_aliens()


# ----------------------------- Menu -----------------------------

def screen_menu(screen):
    global state_display
    screen.fill(background_color_menu)
    font_title = pygame.font.SysFont("Arial", 60, bold=True)
    font_sub = pygame.font.SysFont("Arial", 30)
    font_commands = pygame.font.SysFont("Arial", 25, bold=True)
    font_commands1 = pygame.font.SysFont("Arial", 20, bold=True)

    title_text = font_title.render("SkyWalkers Invaders", True, (0, 255, 0))
    text_sub = font_sub.render("PRESSIONE ESPAÇO PARA JOGAR", True, text_color)
    commands_text = font_commands.render("Comandos: ", True, commands_color)
    commands_text1 = font_commands1.render("space = atirar", True, commands_color)
    commands_text2 = font_commands1.render("← → = movimentar-se", True, commands_color)


    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 80))
    screen.blit(text_sub, (width // 2 - text_sub.get_width() // 2, height // 2 - 10))
    screen.blit(commands_text, (width // 2 - 160, height // 2 + 70))
    screen.blit(commands_text1, (width // 2 - 80, height // 2 + 95))
    screen.blit(commands_text2, (width // 2 - 80, height // 2 + 115))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()  # Prepara tudo antes de ir para o jogo
                state_display = "JOGO"


# ----------------------------- Jogo -----------------------------
def screen_game(screen):
    global state_display, direction_aliens, score, vel_alien_x
    screen.fill(background_color_game)

    # PROCESSAR EVENTOS (Tiro e Saída)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Limita a 5 tiros na tela ao mesmo tempo
                if len(shots) < 5:
                    new_shots = pygame.Rect(gamer["rect"].centerx - 2, gamer["rect"].top, 4, 15)
                    shots.append(new_shots)
                    if sound_shot:
                        sound_shot.play()

    # MOVIMENTAÇÃO DO JOGADOR
    key_map = pygame.key.get_pressed()
    if key_map[pygame.K_LEFT] and gamer["rect"].left > 0:
        gamer["rect"].x -= gamer["vel"]
    if key_map[pygame.K_RIGHT] and gamer["rect"].right < width:
        gamer["rect"].x += gamer["vel"]


    for shot in shots[:]:
        shot.y -= 10  # Velocidade do tiro subindo
        if shot.bottom < 0:
            shots.remove(shot)  # Remove se sair da tela

    # MOVIMENTAÇÃO DOS ALIENS E LÓGICA DE PAREDE
    limit = False
    for alien in aliens:
        alien.x += vel_alien_x * direction_aliens
        # Verifica se algum alien tocou nas bordas
        if alien.right >= width or alien.left <= 0:
            limit = True

    # Se bater, inverte a direção e desce a horda inteira
    if limit:
        direction_aliens *= -1
        for alien in aliens:
            alien.y += vel_alien_y
            # GAMEOVER: Se a horda chegar no gamer
            if alien.bottom >= gamer["rect"].top:
                state_display = "GAMEOVER"

    # VERIFICAR COLISÕES (Tiros acertando Aliens)
    for shot in shots[:]:
        for alien in aliens[:]:
            if shot.colliderect(alien):
                if shot in shots: shots.remove(shot)
                if alien in aliens: aliens.remove(alien)
                score += 10
                break  # Evita que um shot destrua dois aliens sobrepostos

    # NOVA ONDA: Se limpar a tela, cria mais aliens
    if len(aliens) == 0:
        vel_alien_x += 1
        create_aliens()

    # DESENHAR TUDO NA TELA
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
    global state_display, score
    screen.fill(background_color_gameover)
    font_title = pygame.font.SysFont("Arial", 70, bold=True)
    font_sub = pygame.font.SysFont("Arial", 30)

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