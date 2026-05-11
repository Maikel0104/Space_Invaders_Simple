import pygame
import sys

# --- Configurações Iniciais ---
LARGURA, ALTURA = 800, 600
COR_FUNDO_MENU = (50, 0, 50)
COR_FUNDO_JOGO = (10, 10, 30)  # Um azul bem escuro para o espaço
COR_FUNDO_GAMEOVER = (100, 0, 0)
COR_TEXTO = (255, 255, 255)

# Cores dos Elementos provisórios
COR_JOGADOR = (0, 255, 0)  # Verde
COR_ALIEN = (255, 50, 50)  # Vermelho
COR_TIRO = (255, 255, 0)  # Amarelo

# Variáveis de Controle de Estado
estado_tela = "MENU"
rodando = True

# --- Variáveis Globais do Jogo ---
jogador = {"rect": pygame.Rect(0, 0, 50, 20), "vel": 5}
tiros = []
aliens = []
direcao_aliens = 1  # 1 para direita, -1 para esquerda
vel_alien_x = 2  # Velocidade horizontal da horda
vel_alien_y = 15  # Quanto a horda desce ao bater na parede
pontuacao = 0


def inicializar():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Space Invaders Retrô")
    relogio = pygame.time.Clock()
    return tela, relogio


def criar_onda_aliens():
    """Gera a formação inicial de inimigos"""
    global aliens
    aliens.clear()
    for linha in range(4):  # 4 linhas de aliens
        for coluna in range(10):  # 10 colunas de aliens
            alien_x = 50 + coluna * 60
            alien_y = 50 + linha * 40
            aliens.append(pygame.Rect(alien_x, alien_y, 40, 30))


def resetar_jogo():
    """Prepara as variáveis para um novo jogo"""
    global tiros, direcao_aliens, pontuacao
    jogador["rect"].x = LARGURA // 2 - 25
    jogador["rect"].y = ALTURA - 50
    tiros.clear()
    direcao_aliens = 1
    pontuacao = 0
    criar_onda_aliens()


# --- Funções de Tela ---

def tela_menu(tela):
    global estado_tela
    tela.fill(COR_FUNDO_MENU)
    fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
    fonte_sub = pygame.font.SysFont("Arial", 30)

    texto_titulo = fonte_titulo.render("SPACE INVADERS", True, COR_JOGADOR)
    texto_sub = fonte_sub.render("PRESSIONE ESPAÇO PARA JOGAR", True, COR_TEXTO)

    tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, ALTURA // 2 - 50))
    tela.blit(texto_sub, (LARGURA // 2 - texto_sub.get_width() // 2, ALTURA // 2 + 30))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                resetar_jogo()  # Prepara tudo antes de ir para o jogo
                estado_tela = "JOGO"


def tela_jogo(tela):
    global estado_tela, direcao_aliens, pontuacao
    tela.fill(COR_FUNDO_JOGO)

    # 1. PROCESSAR EVENTOS (Tiro e Saída)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Limita a 3 tiros na tela ao mesmo tempo (clássico do Atari)
                if len(tiros) < 3:
                    novo_tiro = pygame.Rect(jogador["rect"].centerx - 2, jogador["rect"].top, 4, 15)
                    tiros.append(novo_tiro)

    # 2. MOVIMENTAÇÃO DO JOGADOR
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador["rect"].left > 0:
        jogador["rect"].x -= jogador["vel"]
    if teclas[pygame.K_RIGHT] and jogador["rect"].right < LARGURA:
        jogador["rect"].x += jogador["vel"]

    # 3. MOVIMENTAÇÃO DOS TIROS
    for tiro in tiros[:]:  # Iteramos sobre uma cópia da lista
        tiro.y -= 10  # Velocidade do tiro subindo
        if tiro.bottom < 0:
            tiros.remove(tiro)  # Remove se sair da tela

    # 4. MOVIMENTAÇÃO DOS ALIENS E LÓGICA DE PAREDE
    bateu_na_parede = False
    for alien in aliens:
        alien.x += vel_alien_x * direcao_aliens
        # Verifica se algum alien tocou nas bordas
        if alien.right >= LARGURA or alien.left <= 0:
            bateu_na_parede = True

    # Se bater, inverte a direção e desce a horda inteira
    if bateu_na_parede:
        direcao_aliens *= -1
        for alien in aliens:
            alien.y += vel_alien_y
            # GAMEOVER: Se a horda chegar no jogador
            if alien.bottom >= jogador["rect"].top:
                estado_tela = "GAMEOVER"

    # 5. VERIFICAR COLISÕES (Tiros acertando Aliens)
    for tiro in tiros[:]:
        for alien in aliens[:]:
            if tiro.colliderect(alien):
                if tiro in tiros: tiros.remove(tiro)
                if alien in aliens: aliens.remove(alien)
                pontuacao += 10
                break  # Evita que um tiro destrua dois aliens sobrepostos

    # 6. NOVA ONDA: Se limpar a tela, cria mais aliens
    if len(aliens) == 0:
        criar_onda_aliens()

    # 7. DESENHAR TUDO NA TELA
    pygame.draw.rect(tela, COR_JOGADOR, jogador["rect"])

    for tiro in tiros:
        pygame.draw.rect(tela, COR_TIRO, tiro)

    for alien in aliens:
        pygame.draw.rect(tela, COR_ALIEN, alien)

    # Pontuação no canto
    fonte_pontos = pygame.font.SysFont("Arial", 25)
    texto_pontos = fonte_pontos.render(f"PONTOS: {pontuacao}", True, COR_TEXTO)
    tela.blit(texto_pontos, (10, 10))


def tela_gameover(tela):
    global estado_tela, pontuacao
    tela.fill(COR_FUNDO_GAMEOVER)
    fonte_titulo = pygame.font.SysFont("Arial", 70, bold=True)
    fonte_sub = pygame.font.SysFont("Arial", 30)

    texto_titulo = fonte_titulo.render("GAME OVER", True, COR_TEXTO)
    texto_pontos = fonte_sub.render(f"PONTUAÇÃO FINAL: {pontuacao}", True, COR_TIRO)
    texto_sub = fonte_sub.render("PRESSIONE 'R' PARA RECOMEÇAR", True, COR_TEXTO)

    tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, ALTURA // 2 - 60))
    tela.blit(texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, ALTURA // 2 + 20))
    tela.blit(texto_sub, (LARGURA // 2 - texto_sub.get_width() // 2, ALTURA // 2 + 70))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                estado_tela = "MENU"


# --- Loop Principal ---
tela, relogio = inicializar()

while rodando:
    if estado_tela == "MENU":
        tela_menu(tela)
    elif estado_tela == "JOGO":
        tela_jogo(tela)
    elif estado_tela == "GAMEOVER":
        tela_gameover(tela)

    pygame.display.flip()
    relogio.tick(60)