import pygame  # Importa a biblioteca pygame
import sys  # Importa a biblioteca sys

pygame.init()  # Inicializa todos os módulos do pygame

pygame.mixer.music.set_volume(0.10)  # Define o volume da música de fundo para 10%
musicafundo = pygame.mixer.music.load('BoxCat Games - CPU Talk.mp3')  # Carrega a música de fundo
pygame.mixer.music.play(-1)  # Toca a música de fundo em loop infinito

mscfim = pygame.mixer.Sound('smw_bonus_game_end.wav')  # Carrega o som de fim de jogo
mscwin = pygame.mixer.Sound('sfx-victory6.mp3')  # Carrega o som de vitória

tela = pygame.display.set_mode((1000, 600))  # Define o tamanho da janela do jogo
pygame.display.set_caption("Jogo de Futebol")  # Define o título da janela do jogo

fundo_inicio = pygame.image.load('imagens/telaInicio.png')  # Carrega a imagem de fundo da tela de início
fundo_pergunta = pygame.image.load('imagens/pergunta1.png')  # Carrega a imagem de fundo da tela de perguntas
fundo_acerto = pygame.image.load('imagens/ganhou.png')  # Carrega a imagem de fundo da tela de acerto
fundo_derrota = pygame.image.load('imagens/perdeu.png')  # Carrega a imagem de fundo da tela de derrota
fundo_dificuldade = pygame.image.load('imagens/telaDificuldade.png')  # Carrega a imagem de fundo da tela de seleção de dificuldade

dificuldades = {  # Define as dificuldades do jogo
    'Fácil': {
        'tempo': 60,  # Define o tempo para a dificuldade fácil
        'perguntas_respostas': [  # Define as perguntas e respostas para a dificuldade fácil
            ("Maior artilheiro da história do Tottenham: _ _ _ _ _   _ _ _ _", "Harry Kane"),
            ("Unico jogador a ganhar 3 copas: _ _ _ _", "Pelé"),
            ("Quem venceu a Liga dos Campeões 2019: _ _ _ _ _ _ _ _ _", "Liverpool")
        ]
    },
    'Médio': {
        'tempo': 45,  # Define o tempo para a dificuldade média
        'perguntas_respostas': [  # Define as perguntas e respostas para a dificuldade média
            ("Artilheiro do ano de 2023: _ _ _ _ _ _ _ _ _   _ _ _ _ _ _ _", "Cristiano Ronaldo"),
            ("Maior artilheiro Brasileiro da libertadores: _ _ _ _ _ _ _", "Gabigol"),
            ("Unico campeão invicto da história da PremierLeague: _ _ _ _ _ _ _", "Arsenal"),
            ("Artilheiro da PremierLeague na temporada 18-19: _ _ _ _ _", "Salah"),
            ("Campeão da Libertadores da América em 2019: _ _ _ _ _ _ _ _", "Flamengo")
        ]
    },
    'Difícil': {
        'tempo': 30,  # Define o tempo para a dificuldade difícil
        'perguntas_respostas': [  # Define as perguntas e respostas para a dificuldade difícil
            ("Quem marcou o gol da vitória na final da Copa do Mundo de 2014", "Gotze"),
            ("Quem tem o recorde de mais gols feitos em um único ano na Italia", "Higuain"),
            ("Jogador a marcar gols em todas as partidas de uma edição da Copa", "Jairzinho"),
            ("Jogador com mais partidas disputadas pela seleção brasileira", "Cafu"),
            ("Time argentino foi o primeiro a vencer a Copa Intercontinental", "Racing")
        ]
    }
}

na_tela_de_inicio = True  # Indica se o jogo está na tela de início
na_tela_de_pergunta = False  # Indica se o jogo está na tela de perguntas
na_tela_de_acerto = False  # Indica se o jogo está na tela de acerto
na_tela_de_derrota = False  # Indica se o jogo está na tela de derrota
na_tela_de_dificuldade = False  # Indica se o jogo está na tela de seleção de dificuldade

pergunta_atual = 0  # Armazena o índice da pergunta atual
resposta_usuario = ""  # Armazena a resposta do usuário
pontuacao = 0  # Armazena a pontuação do usuário
dificuldade_selecionada = None  # Armazena a dificuldade selecionada pelo usuário


dificuldade_selecionada = None  # Armazena a dificuldade selecionada pelo usuário

tempo_total = 30  # Define o tempo total do jogo
tempo_restante = tempo_total  # Inicializa o tempo restante com o tempo total
fonte_tempo = pygame.font.Font("imagens/font.ttf", 10)  # Define a fonte para exibir o tempo
relogio = pygame.time.Clock()  # Cria um objeto de relógio para controlar o tempo do jogo


som_tocado = False  # Indica se o som de vitória ou derrota já foi tocado

def desenhar_botao(texto, pos_x, pos_y, largura, altura):  # Define a função para desenhar um botão na tela
    mouse = pygame.mouse.get_pos()  # Obtém a posição do mouse
    clique = pygame.mouse.get_pressed()  # Obtém o estado dos botões do mouse

    # Define a cor do botão com base na posição do mouse
    cor_botao = (173, 216, 230) if pos_x + largura > mouse[0] > pos_x and pos_y + altura > mouse[1] > pos_y else (135, 206, 250)

    pygame.draw.rect(tela, cor_botao, (pos_x, pos_y, largura, altura))  # Desenha o botão
    fonte_botao = pygame.font.Font("imagens/font.ttf", 20)  # Define a fonte do texto do botão
    texto_botao = fonte_botao.render(texto, True, (0, 0, 0))  # Renderiza o texto do botão
    tela.blit(texto_botao, (pos_x + (largura - texto_botao.get_width()) // 2, pos_y + (altura - texto_botao.get_height()) // 2))  # Desenha o texto do botão

    # Retorna True se o botão foi clicado
    return clique[0] == 1 and pos_x + largura > mouse[0] > pos_x and pos_y + altura > mouse[1] > pos_y

def reiniciar_jogo():  # Define a função para reiniciar o jogo
    global na_tela_de_inicio, na_tela_de_pergunta, na_tela_de_acerto, na_tela_de_derrota, na_tela_de_dificuldade
    global pergunta_atual, resposta_usuario, pontuacao, tempo_restante, som_tocado, dificuldade_selecionada

    na_tela_de_inicio = True  # Redefine a tela atual para a tela de início
    na_tela_de_pergunta = False  # Redefine a tela de pergunta
    na_tela_de_acerto = False  # Redefine a tela de acerto
    na_tela_de_derrota = False  # Redefine a tela de derrota
    na_tela_de_dificuldade = True  # Redefine a tela de seleção de dificuldade

    pergunta_atual = 0  # Redefine a pergunta atual
    resposta_usuario = ""  # Redefine a resposta do usuário
    pontuacao = 0  # Redefine a pontuação do usuário
    tempo_restante = tempo_total  # Redefine o tempo restante
    som_tocado = False  # Redefine a variável que indica se o som foi tocado
    dificuldade_selecionada = None  # Reinicie a dificuldade selecionada

loop = True  # Define a variável de controle do loop principal do jogo
while loop:  # Inicia o loop principal do jogo
    for event in pygame.event.get():  # Obtém todos os eventos do pygame
        if event.type == pygame.QUIT:  # Verifica se o evento é de sair do jogo
            loop = False  # Sai do loop do jogo
        if event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
            if na_tela_de_inicio and event.key == pygame.K_RETURN:  # Verifica se o usuário está na tela de início e pressionou Enter
                na_tela_de_inicio = False  # Sai da tela de início
                na_tela_de_dificuldade = True  # Vai para a tela de seleção de dificuldade
            elif na_tela_de_dificuldade:  # Verifica se o usuário está na tela de seleção de dificuldade
                if event.key == pygame.K_1:  # Verifica se o usuário pressionou a tecla 1
                    dificuldade_selecionada = 'Fácil'  # Seleciona a dificuldade fácil
                elif event.key == pygame.K_2:  # Verifica se o usuário pressionou a tecla 2
                    dificuldade_selecionada = 'Médio'  # Seleciona a dificuldade média
                elif event.key == pygame.K_3:  # Verifica se o usuário pressionou a tecla 3
                    dificuldade_selecionada = 'Difícil'  # Seleciona a dificuldade difícil

                if dificuldade_selecionada:  # Verifica se uma dificuldade foi selecionada
                    tempo_total = dificuldades[dificuldade_selecionada]['tempo']  # Define o tempo total para a dificuldade selecionada
                    perguntas_respostas = dificuldades[dificuldade_selecionada]['perguntas_respostas']  # Define as perguntas e respostas para a dificuldade selecionada
                    tempo_restante = tempo_total  # Redefine o tempo restante
                    na_tela_de_dificuldade = False  # Sai da tela de seleção de dificuldade
                    na_tela_de_pergunta = True  # Vai para a tela de perguntas

            elif na_tela_de_pergunta:  # Verifica se o usuário está na tela de perguntas
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:  # Verifica se o usuário pressionou a tecla Backspace
                    resposta_usuario = resposta_usuario[:-1]  # Remove o último caractere da resposta do usuário
                elif event.key == pygame.K_RETURN:  # Verifica se o usuário pressionou a tecla Enter
                    if resposta_usuario.lower().strip() == perguntas_respostas[pergunta_atual][1].lower().strip():  # Verifica se a resposta do usuário está correta
                        pontuacao += 1  # Incrementa a pontuação do usuário
                        resposta_usuario = ""  # Redefine a resposta do usuário
                    else:
                        resposta_usuario = ""  # Redefine a resposta do usuário
                    pergunta_atual += 1  # Vai para a próxima pergunta
                    if pergunta_atual >= len(perguntas_respostas):  # Verifica se todas as perguntas foram respondidas
                        if pontuacao == len(perguntas_respostas):  # Verifica se o usuário acertou todas as perguntas
                            na_tela_de_pergunta = False  # Sai da tela de perguntas
                            na_tela_de_acerto = True  # Vai para a tela de acerto
                        else:
                            na_tela_de_pergunta = False  # Sai da tela de perguntas
                            na_tela_de_derrota = True  # Vai para a tela de derrota
                else:
                    resposta_usuario += event.unicode  # Adiciona o caractere digitado pelo usuário à resposta

    if na_tela_de_pergunta:  # Verifica se o usuário está na tela de perguntas
        tempo_restante -= relogio.get_time() / 1000  # Decrementa o tempo restante
        if tempo_restante <= 0:  # Verifica se o tempo acabou
            na_tela_de_pergunta = False  # Sai da tela de perguntas
            na_tela_de_derrota = True  # Vai para a tela de derrota

    if na_tela_de_inicio:  # Verifica se o usuário está na tela de início
        tela.blit(fundo_inicio, (0, 0))  # Desenha a imagem de fundo da tela de início
    
    elif na_tela_de_dificuldade:  # Verifica se o usuário está na tela de seleção de dificuldade
        tela.blit(fundo_dificuldade, (0, 0))  # Desenha a imagem de fundo da tela de seleção de dificuldade
        if desenhar_botao("Fácil (Aperte 1)", 300, 150, 400, 50):  # Desenha o botão para selecionar a dificuldade fácil
            dificuldade_selecionada = 'Fácil'  # Seleciona a dificuldade fácil
        if desenhar_botao("Médio (Aperte 2)", 300, 250, 400, 50):  # Desenha o botão para selecionar a dificuldade média
            dificuldade_selecionada = 'Médio'  # Seleciona a dificuldade média
        if desenhar_botao("Difícil (Aperte 3)", 300, 350, 400, 50):  # Desenha o botão para selecionar a dificuldade difícil
            dificuldade_selecionada = 'Difícil'  # Seleciona a dificuldade difícil
        if dificuldade_selecionada:  # Verifica se uma dificuldade foi selecionada
            tempo_total = dificuldades[dificuldade_selecionada]['tempo']  # Define o tempo total para a dificuldade selecionada
            perguntas_respostas = dificuldades[dificuldade_selecionada]['perguntas_respostas']  # Define as perguntas e respostas para a dificuldade selecionada
            tempo_restante = tempo_total  # Redefine o tempo restante
            na_tela_de_dificuldade = False  # Sai da tela de seleção de dificuldade
            na_tela_de_pergunta = True  # Vai para a tela de perguntas

    elif na_tela_de_pergunta:  # Verifica se o usuário está na tela de perguntas
        tela.blit(fundo_pergunta, (0, 0))  # Desenha a imagem de fundo da tela de perguntas
        
        fonte = pygame.font.Font("imagens/font.ttf", 15)  # Define a fonte para exibir a pergunta
        texto_pergunta = fonte.render(perguntas_respostas[pergunta_atual][0], True, (0, 0, 0))  # Renderiza o texto da pergunta
        tela.blit(texto_pergunta, (5, 205))  # Desenha o texto da pergunta na tela
        
        fonte_resposta = pygame.font.Font("imagens/font.ttf", 20)  # Define a fonte para exibir a resposta
        texto_resposta = fonte_resposta.render(resposta_usuario, True, (0, 0, 0))  # Renderiza o texto da resposta do usuário
        tela.blit(texto_resposta, (430, 505))  # Desenha o texto da resposta na tela
        
        texto_tempo = fonte_tempo.render(f"Tempo restante: {int(tempo_restante)}s", True, (0, 0, 0))  # Renderiza o texto do tempo restante
        tela.blit(texto_tempo, (3, 8))  # Desenha o texto do tempo restante na tela
    
    elif na_tela_de_acerto:  # Verifica se o usuário está na tela de acerto
        tela.blit(fundo_acerto, (0, 0))  # Desenha a imagem de fundo da tela de acerto
        fonte_resultado = pygame.font.Font("imagens/font.ttf", 15)  # Define a fonte para exibir o resultado
        texto_resultado = fonte_resultado.render(f"Acertou {pontuacao} de {len(perguntas_respostas)} perguntas!", True, (0, 0, 0))  # Renderiza o texto do resultado
        tela.blit(texto_resultado, (10, 10))  # Desenha o texto do resultado na tela
        if not som_tocado:  # Verifica se o som de vitória ainda não foi tocado
            mscwin.play()  # Toca o som de vitória
            som_tocado = True  # Define que o som de vitória foi tocado

        if desenhar_botao("Jogar novamente", 360, 100, 300, 50):  # Desenha o botão para jogar novamente
            reiniciar_jogo()  # Reinicia o jogo
    
    elif na_tela_de_derrota:  # Verifica se o usuário está na tela de derrota
        tela.blit(fundo_derrota, (0, 0))  # Desenha a imagem de fundo da tela de derrota
        fonte_resultado = pygame.font.Font("imagens/font.ttf", 15)  # Define a fonte para exibir o resultado
        texto_resultado = fonte_resultado.render(f"Você acertou {pontuacao} de {len(perguntas_respostas)} perguntas.", True, (0, 0, 0))  # Renderiza o texto do resultado
        tela.blit(texto_resultado, (10, 10))  # Desenha o texto do resultado na tela
        if not som_tocado:  # Verifica se o som de fim de jogo ainda não foi tocado
            mscfim.play()  # Toca o som de fim de jogo
            som_tocado = True  # Define que o som de fim de jogo foi tocado

        if desenhar_botao("Jogar novamente", 360, 250, 300, 50):  # Desenha o botão para jogar novamente
            reiniciar_jogo()  # Reinicia o jogo
    
    pygame.display.flip()  # Atualiza a tela
    relogio.tick(30)  # Define a taxa de atualização do jogo para 30 frames por segundo

pygame.quit()  # Encerra todos os módulos do pygame
sys.exit()  # Encerra o programa
