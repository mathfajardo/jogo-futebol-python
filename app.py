# importando bibliotecas
import pygame  
import sys 

# inicializa os módulos do pygame
pygame.init()  

# implementa as musicas do jogo
pygame.mixer.music.set_volume(0.10) 
musicafundo = pygame.mixer.music.load('musica/musica_padrao.mp3')  
pygame.mixer.music.play(-1)  
mscfim = pygame.mixer.Sound('musica/musica_derrota.wav')  
mscwin = pygame.mixer.Sound('musica/musica_vitoria.mp3')  

# define a tela e o titulo da janela do jogo
tela = pygame.display.set_mode((1000, 600))  
pygame.display.set_caption("Jogo de Futebol")  

# carrega as imagens
fundo_inicio = pygame.image.load('imagens/telaInicio.png')  
fundo_pergunta = pygame.image.load('imagens/pergunta1.png') 
fundo_acerto = pygame.image.load('imagens/ganhou.png') 
fundo_derrota = pygame.image.load('imagens/perdeu.png')  
fundo_dificuldade = pygame.image.load('imagens/telaDificuldade.png') 

# define as dificuldades e perguntas do jogo
dificuldades = {  
    'Fácil': {
        'tempo': 60,  
        'perguntas_respostas': [  
            ("Maior artilheiro da história do Tottenham: _ _ _ _ _   _ _ _ _", "Harry Kane"),
            ("Unico jogador a ganhar 3 copas: _ _ _ _", "Pelé"),
            ("Quem venceu a Liga dos Campeões 2019: _ _ _ _ _ _ _ _ _", "Liverpool")
        ]
    },
    'Médio': {
        'tempo': 45,  
        'perguntas_respostas': [  
            ("Artilheiro do ano de 2023: _ _ _ _ _ _ _ _ _   _ _ _ _ _ _ _", "Cristiano Ronaldo"),
            ("Maior artilheiro Brasileiro da libertadores: _ _ _ _ _ _ _", "Gabigol"),
            ("Unico campeão invicto da história da PremierLeague: _ _ _ _ _ _ _", "Arsenal"),
            ("Artilheiro da PremierLeague na temporada 18-19: _ _ _ _ _", "Salah"),
            ("Campeão da Libertadores da América em 2019: _ _ _ _ _ _ _ _", "Flamengo")
        ]
    },
    'Difícil': {
        'tempo': 30, 
        'perguntas_respostas': [  
            ("Quem marcou o gol da vitória na final da Copa do Mundo de 2014", "Gotze"),
            ("Quem tem o recorde de mais gols feitos em um único ano na Italia", "Higuain"),
            ("Jogador a marcar gols em todas as partidas de uma edição da Copa", "Jairzinho"),
            ("Jogador com mais partidas disputadas pela seleção brasileira", "Cafu"),
            ("Time argentino foi o primeiro a vencer a Copa Intercontinental", "Racing")
        ]
    }
}

# inicia com a tela inicio
na_tela_de_inicio = True 
na_tela_de_pergunta = False  
na_tela_de_acerto = False 
na_tela_de_derrota = False  # 
na_tela_de_dificuldade = False  

# inicia as variáveis
pergunta_atual = 0  
resposta_usuario = ""  
pontuacao = 0  
dificuldade_selecionada = None  # Armazena a dificuldade selecionada pelo usuário

tempo_total = 30  
tempo_restante = tempo_total  
fonte_tempo = pygame.font.Font("imagens/font.ttf", 10) 
relogio = pygame.time.Clock()  


som_tocado = False  

# define função para desenhar o botão na tela
def desenhar_botao(texto, pos_x, pos_y, largura, altura):  
    mouse = pygame.mouse.get_pos()  
    clique = pygame.mouse.get_pressed()  

    
    cor_botao = (173, 216, 230) if pos_x + largura > mouse[0] > pos_x and pos_y + altura > mouse[1] > pos_y else (135, 206, 250)

    pygame.draw.rect(tela, cor_botao, (pos_x, pos_y, largura, altura))  
    fonte_botao = pygame.font.Font("imagens/font.ttf", 20)  
    texto_botao = fonte_botao.render(texto, True, (0, 0, 0))  
    tela.blit(texto_botao, (pos_x + (largura - texto_botao.get_width()) // 2, pos_y + (altura - texto_botao.get_height()) // 2))  

    return clique[0] == 1 and pos_x + largura > mouse[0] > pos_x and pos_y + altura > mouse[1] > pos_y

# define função para reiniciar o jogo
def reiniciar_jogo():  
    global na_tela_de_inicio, na_tela_de_pergunta, na_tela_de_acerto, na_tela_de_derrota, na_tela_de_dificuldade
    global pergunta_atual, resposta_usuario, pontuacao, tempo_restante, som_tocado, dificuldade_selecionada

    na_tela_de_inicio = True 
    na_tela_de_pergunta = False 
    na_tela_de_acerto = False  
    na_tela_de_derrota = False  
    na_tela_de_dificuldade = True 

    pergunta_atual = 0  
    resposta_usuario = ""  
    pontuacao = 0  
    tempo_restante = tempo_total  
    som_tocado = False  
    dificuldade_selecionada = None  

# Inicia o loop principal do jogo
loop = True  
while loop:  
    # obtém todos os eventos do pygame
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            loop = False 
        if event.type == pygame.KEYDOWN:  
            if na_tela_de_inicio and event.key == pygame.K_RETURN:  
                na_tela_de_inicio = False  
                na_tela_de_dificuldade = True  
            elif na_tela_de_dificuldade: 
                if event.key == pygame.K_1: 
                    dificuldade_selecionada = 'Fácil'
                elif event.key == pygame.K_2: 
                    dificuldade_selecionada = 'Médio' 
                elif event.key == pygame.K_3:  
                    dificuldade_selecionada = 'Difícil' 

                if dificuldade_selecionada: 
                    tempo_total = dificuldades[dificuldade_selecionada]['tempo'] 
                    perguntas_respostas = dificuldades[dificuldade_selecionada]['perguntas_respostas'] 
                    tempo_restante = tempo_total 
                    na_tela_de_dificuldade = False  
                    na_tela_de_pergunta = True 

            elif na_tela_de_pergunta:
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]: 
                    resposta_usuario = resposta_usuario[:-1] 
                elif event.key == pygame.K_RETURN:  
                    if resposta_usuario.lower().strip() == perguntas_respostas[pergunta_atual][1].lower().strip(): 
                        pontuacao += 1 
                        resposta_usuario = "" 
                    else:
                        resposta_usuario = ""  
                    pergunta_atual += 1  
                    if pergunta_atual >= len(perguntas_respostas): 
                        if pontuacao == len(perguntas_respostas): 
                            na_tela_de_pergunta = False  
                            na_tela_de_acerto = True 
                        else:
                            na_tela_de_pergunta = False 
                            na_tela_de_derrota = True  
                else:
                    resposta_usuario += event.unicode  

    if na_tela_de_pergunta: 
        tempo_restante -= relogio.get_time() / 1000  
        if tempo_restante <= 0:  
            na_tela_de_pergunta = False 
            na_tela_de_derrota = True  

    if na_tela_de_inicio:  
        tela.blit(fundo_inicio, (0, 0))  
    
    elif na_tela_de_dificuldade:  
        tela.blit(fundo_dificuldade, (0, 0))  
        if desenhar_botao("Fácil (Aperte 1)", 300, 150, 400, 50):
            dificuldade_selecionada = 'Fácil'
        if desenhar_botao("Médio (Aperte 2)", 300, 250, 400, 50):  
            dificuldade_selecionada = 'Médio' 
        if desenhar_botao("Difícil (Aperte 3)", 300, 350, 400, 50): 
            dificuldade_selecionada = 'Difícil'  
        if dificuldade_selecionada:  
            tempo_total = dificuldades[dificuldade_selecionada]['tempo'] 
            perguntas_respostas = dificuldades[dificuldade_selecionada]['perguntas_respostas']  
            tempo_restante = tempo_total 
            na_tela_de_dificuldade = False 
            na_tela_de_pergunta = True  

    elif na_tela_de_pergunta:  
        tela.blit(fundo_pergunta, (0, 0))  
        
        fonte = pygame.font.Font("imagens/font.ttf", 15) 
        texto_pergunta = fonte.render(perguntas_respostas[pergunta_atual][0], True, (0, 0, 0))  
        tela.blit(texto_pergunta, (5, 205))  
        
        fonte_resposta = pygame.font.Font("imagens/font.ttf", 20) 
        texto_resposta = fonte_resposta.render(resposta_usuario, True, (0, 0, 0))  
        tela.blit(texto_resposta, (430, 505))  
        
        texto_tempo = fonte_tempo.render(f"Tempo restante: {int(tempo_restante)}s", True, (0, 0, 0))  
        tela.blit(texto_tempo, (3, 8)) 

    elif na_tela_de_acerto:  
        tela.blit(fundo_acerto, (0, 0))  
        fonte_resultado = pygame.font.Font("imagens/font.ttf", 15)  
        texto_resultado = fonte_resultado.render(f"Acertou {pontuacao} de {len(perguntas_respostas)} perguntas!", True, (0, 0, 0))  
        tela.blit(texto_resultado, (10, 10))  
        if not som_tocado: 
            mscwin.play()  
            som_tocado = True 

        if desenhar_botao("Jogar novamente", 360, 100, 300, 50):  
            reiniciar_jogo() 
    
    elif na_tela_de_derrota: 
        tela.blit(fundo_derrota, (0, 0)) 
        fonte_resultado = pygame.font.Font("imagens/font.ttf", 15) 
        texto_resultado = fonte_resultado.render(f"Você acertou {pontuacao} de {len(perguntas_respostas)} perguntas.", True, (0, 0, 0)) 
        tela.blit(texto_resultado, (10, 10)) 
        if not som_tocado: 
            mscfim.play() 
            som_tocado = True  

        if desenhar_botao("Jogar novamente", 360, 250, 300, 50):  
            reiniciar_jogo()  

    pygame.display.flip() 
    relogio.tick(30)  

# encerra o jogo
pygame.quit()  
sys.exit()  
