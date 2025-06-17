import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
#from Recursos.basicos import inicializarBancoDeDados
#from Recursos.basicos import escreverDados
import json

pygame.init()
#inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("TRON: Legacy")
icone = pygame.image.load("Recursos/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
azul = (0, 221, 252)
menuTron = pygame.image.load("Recursos/menuTron.png")
menuJogar = pygame.image.load("Recursos/menuJogar.png")
menuSair = pygame.image.load("Recursos/menuSair.png")
menuCreditos = pygame.image.load("Recursos/menuCreditos.png")
fundoCreditos = pygame.image.load("Recursos/fundoCreditos.png")
mainJogador = pygame.image.load("Recursos/mainJogador.png")
mainObstaculo = pygame.image.load("Recursos/mainObstaculo.png")
mainFundo = pygame.image.load("Recursos/mainFundo.png")
fundoMorte = pygame.image.load("Recursos/fundoMorte.png")
#somColisao = pygame.mixer.Sound("assets/missile.wav")
#somMoeda = pygame.mixer.Sound("assets/explosao.wav")
fonteNome = pygame.font.SysFont("TRON",20)
pygame.mixer.music.load("Recursos/somMenu.mp3")
pygame.mixer.music.play(-1)

def jogar():
    largura_janela = 300
    altura_janela = 50

    pygame.mixer.music.load("Recursos/mainSom.mp3")
    pygame.mixer.music.play(-1)

    # Inicializações da jogabilidade
    player_speed_y = 0
    gravity = 0.5
    fly_force = -10

    player_rect = mainJogador.get_rect()
    player_rect.x = 100
    player_rect.y = tamanho[1] // 2

    obstacles = []
    obstacle_timer = 0

    bg_x = 0
    velocidade_fundo = 2

    pontos = 0
    rodando = True
    pausado = False

    # Define a contagem regressiva
    def contagemRegressiva():
        for i in range(3, 0, -1):
            tela.blit(mainFundo, (0, 0))
            tela.blit(mainJogador, player_rect)
            texto = fonteNome.render(str(i), True, azul)
            tela.blit(texto, (tamanho[0] // 2 - texto.get_width() // 2, tamanho[1] // 2))
            pygame.display.update()
            pygame.time.delay(1000)

        tela.blit(mainFundo, (0, 0))
        tela.blit(mainJogador, player_rect)
        texto = fonteNome.render("GO!", True, azul)
        tela.blit(texto, (tamanho[0] // 2 - texto.get_width() // 2, tamanho[1] // 2))
        pygame.display.update()
        pygame.time.delay(1000)

    def telaPausa():
        textoPausa = fonteNome.render("Jogo Pausado - Pressione ESPAÇO", True, azul)
        tela.blit(textoPausa, (tamanho[0] // 2 - textoPausa.get_width() // 2, tamanho[1] // 2))
        pygame.display.update()

    contagemRegressiva()

    while rodando:
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    player_speed_y = fly_force
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if pausado:
            telaPausa()
            continue
                            

        # Movimento fundo
        bg_x -= velocidade_fundo
        if bg_x <= -tamanho[0]:
            bg_x = 0

        # Desenhar fundo com rolagem infinita
        tela.blit(mainFundo, (bg_x, 0))
        tela.blit(mainFundo, (bg_x + tamanho[0], 0))

        # Física do player
        player_speed_y += gravity
        player_rect.y += player_speed_y

        # Limites vertical
        if player_rect.y < 0:
            player_rect.y = 0
            player_speed_y = 0
        if player_rect.y >= tamanho[1] - player_rect.height:
            dead()
            return
        
        # Criar obstáculos
        obstacle_timer += 1
        if obstacle_timer > 120:
            obstacle_timer = 0
            obst_y = random.randint(50, tamanho[1] - 70)
            new_obst = mainObstaculo.get_rect(topleft=(tamanho[0], obst_y))
            obstacles.append(new_obst)

        # Mover e desenhar obstáculos
        for obst in obstacles[:]:
            obst.x -= 6
            tela.blit(mainObstaculo, obst)
            if obst.right < 0:
                obstacles.remove(obst)
                pontos += 1  # Pontuar ao passar um obstáculo

            # Detectar colisão player x obstáculo
            if player_rect.colliderect(obst):
                pygame.mixer.music.stop()
                dead()
                return 
        
        # Desenhar player
        tela.blit(mainJogador, player_rect)

        # Desenhar pontos na tela (você pode adaptar depois)
        # fonteMenu.render deve estar definida no seu código

        pygame.display.update()

def capturar_nome():
    global nome
    nome = ""

    def obter_nome():
        nonlocal entry_nome
        nome_input = entry_nome.get()
        if not nome_input:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            global nome
            nome = nome_input
            root.destroy()

    root = tk.Tk()
    largura_janela = 300
    altura_janela = 50
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Identifique-se, Usuário:")

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    root.mainloop()

def start():
    larguraButtonJogar = 380
    alturaButtonJogar  = 85
    larguraButtonSair = 380
    alturaButtonSair  = 85
    larguraButtonCreditos = 380
    alturaButtonCreditos = 85

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if jogarRect.collidepoint(evento.pos):
                    larguraButtonJogar = 380
                    alturaButtonJogar  = 85
                if sairRect.collidepoint(evento.pos):
                    larguraButtonSair = 380
                    alturaButtonSair  = 85

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                if jogarRect.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonJogar = 380
                    alturaButtonJogar  = 45
                    capturar_nome()
                    telaBoasVindas()
                if sairRect.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonSair = 380
                    alturaButtonSair  = 85
                    quit()
                if creditosRect.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonCreditos = 380
                    alturaButtonCreditos = 85
                    creditos()
                    
            
        tela.fill(branco)
        tela.blit(menuTron, (0,0) )

        jogarButton = pygame.image.load("Recursos/menuJogar.png")
        jogarRect = jogarButton.get_rect(topleft=(315, 235))
        tela.blit(jogarButton, (315, 235))
        
        sairButton = pygame.image.load("Recursos/menuSair.png")
        sairRect = sairButton.get_rect(topleft=(315, 345))
        tela.blit(sairButton, (315, 345))
        
        creditosButton = pygame.image.load("Recursos/menuCreditos.png")
        creditosRect = creditosButton.get_rect(topleft=(315, 455))
        tela.blit(creditosButton, (315, 455))
        
        pygame.display.update()
        relogio.tick(60)

def creditos():
    larguraButtonCreditos = 401
    alturaButtonCreditos = 91

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if voltarRect.collidepoint(evento.pos):
                    larguraButtonVoltar = 401
                    alturaButtonVoltar = 91
            elif evento.type == pygame.MOUSEBUTTONUP:
                if voltarRect.collidepoint(evento.pos):
                    larguraButtonVoltar = 401
                    alturaButtonVoltar = 91
                    return

        tela.fill(branco)
        tela.blit(fundoCreditos, (0,0))

        voltarButton = pygame.image.load("Recursos/menuVoltar.png")
        voltarRect = voltarButton.get_rect(topleft=(50, 50))
        tela.blit(voltarButton, (50,50))

        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    #pygame.mixer.Sound.play(explosaoSound)
    larguraButtonVoltar = 415
    alturaButtonVoltar = 120
     
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    #label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    #label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    #listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    #listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    #log_partidas = open("base.atitus", "r").read()
    #log_partidas = json.loads(log_partidas)
    #for chave in log_partidas:
        #listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if voltarRect.collidepoint(evento.pos):
                    larguraButtonVoltar = 415
                    alturaButtonVoltar = 120
            elif evento.type == pygame.MOUSEBUTTONUP:
                if voltarRect.collidepoint(evento.pos):
                    pygame.mixer.music.load("Recursos/somMenu.mp3")
                    pygame.mixer.music.play(-1)
                    larguraButtonVoltar = 415
                    alturaButtonVoltar = 120
                    return
                        
        tela.fill(branco)
        tela.blit(fundoMorte, (0,0) )

        voltarButton = pygame.image.load("Recursos/morteVoltar.png")
        voltarRect = voltarButton.get_rect(topleft=(275, 345))
        tela.blit(voltarButton, (275, 345))

        pygame.display.update()
        relogio.tick(60)

def telaBoasVindas():
    fundoBoasVindas = pygame.image.load("Recursos/fundoBoasVindas.png")
    textoBemVindo = fonteNome.render(f"Bem-Vindo {nome}", True, azul)
    textoInstrucoes = fonteNome.render(f"Recolha os fragmentos da sua nave", True, azul)
    #falar("Bem Vindo", nome)

    while True:
        tela.fill(branco)
        tela.blit(fundoBoasVindas, (0, 0))
        tela.blit(textoBemVindo, (370, 155))
        tela.blit(textoInstrucoes, (200, 215))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    jogar()
                    return

        pygame.display.update()
        relogio.tick(60)

start()