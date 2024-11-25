import pygame as py
from entities.snake import Snake
from entities.food import Food
from entities.colisao import colisoes
from entities.points import points
from entities.pathEnemy import PathEnemy
from telas.cenarioMain import tela
from entities.enemy_shooter import enemy_shooter
from entities.timer import timer
from entities.enemy_blue_team import Blue_team

py.init()  # Inicializador do jogo
clock = py.time.Clock()

# Variáveis de jogo
gameRunning = True  # Para testar telas
v_jogo = 10
alturaTela = 640
larguraTela = 640
fase = 1

# Instancias
snake = Snake()
food = Food()
points = points()
pathEnemy = PathEnemy()
bt_enemy = Blue_team(food)
tela = tela(alturaTela, larguraTela, points)
timer = timer()

enemy_shooter_bottom = enemy_shooter(190, 570, 2000, 90, 20)
enemy_shooter_up = enemy_shooter(370, -10, 2000, 270, 20)
enemy_shooter_left = enemy_shooter(-10, 190, 2000, 0, 20)
enemy_shooter_right = enemy_shooter(570, 370, 2000, 180, 20)

colisao = colisoes(snake, food, points, larguraTela, alturaTela, enemy_shooter_bottom.bullets,
                   enemy_shooter_up.bullets, enemy_shooter_left.bullets, enemy_shooter_right.bullets,
                   bt_enemy.azuis, bt_enemy)

while True:  # Loop para encerrar o jogo, caso o usuário pressione o botão de fechar pagina, e para que todo o jogo aconteça.
    while gameRunning:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()

            elif event.type == py.KEYDOWN:
                if event.key == py.K_LEFT and snake.direcao != 'RIGHT':
                    snake.direcao = 'LEFT'
                elif event.key == py.K_RIGHT and snake.direcao != 'LEFT':
                    snake.direcao = 'RIGHT'
                elif event.key == py.K_UP and snake.direcao != 'DOWN':
                    snake.direcao = 'UP'
                elif event.key == py.K_DOWN and snake.direcao != 'UP':
                    snake.direcao = 'DOWN'
                elif event.key == py.K_r:
                    points.resetar()
                    snake.resetar()
                    timer.resetar()
                    colisao.status = 'vivo'
                    gameRunning = True
                elif event.key == py.K_q:
                    py.quit()
                    exit()

        snake.movimento()
        pontos = points.pontos_final
        # desenhar na tela (obs.: ordem de cima para baixo)
        if colisao.status != 'morto':
            if fase == 1:
                tela.tela_jogo()
                food.desenhar(tela.screen)
                snake.cobra_tela(tela.screen)
                points.desenhar(tela.screen)
                timer.desenhar(tela.screen)
                timer.contar_tempo()

                enemy_shooter_bottom.desenhar(tela.screen)
                enemy_shooter_up.desenhar(tela.screen)
                enemy_shooter_left.desenhar(tela.screen)
                enemy_shooter_right.desenhar(tela.screen)

                enemy_shooter_bottom.atirar()
                enemy_shooter_up.atirar()
                enemy_shooter_left.atirar()
                enemy_shooter_right.atirar()

                enemy_shooter_bottom.atualizar_tiros(tela.screen)
                enemy_shooter_up.atualizar_tiros(tela.screen)
                enemy_shooter_left.atualizar_tiros(tela.screen)
                enemy_shooter_right.atualizar_tiros(tela.screen)

                colisao.snake_tiro1()
                colisao.snake_tiro2()
                colisao.snake_tiro3()
                colisao.snake_tiro4()

                if timer.tempo == -1:
                    colisao.status = 'morto'

                if points.pontos == 10:
                    timer.resetar()
                    fase = 2

            if fase == 2:
                tela.tela_jogo()
                food.desenhar(tela.screen)
                snake.cobra_tela(tela.screen)
                points.desenhar(tela.screen)
                pathEnemy.desenhar(tela.screen)
                timer.desenhar(tela.screen)
                timer.contar_tempo()

                colisao.snake_pathEnemy(pathEnemy)

                aaa = pathEnemy.posicoes = [(400, 200), (400, 400)]
                pathEnemy.andar(aaa, snake)

                if timer.tempo == -1:
                    colisao.status = 'morto'

                if points.pontos == 10:
                    fase = 3

            if fase == 3:
                tela.tela_jogo()
                food.desenhar(tela.screen)
                snake.cobra_tela(tela.screen)
                points.desenhar(tela.screen)
                bt_enemy.destruir_chao()
                bt_enemy.desenhar_chao(tela.screen)
                bt_enemy.desenhar_inimigo(tela.screen)
                bt_enemy.mover(larguraTela, alturaTela)
                timer.desenhar(tela.screen)
                timer.contar_tempo()

                colisao.snake_azul()
                colisao.snake_boss_azul()

                if timer.tempo == -1:
                    colisao.status = 'morto'

                if points.pontos == 11:
                    tela.tela_parabens()
                    gameRunning = False
                    # Ver um jeito de ainda dar pra reiniciar.
        else:
            fase = 1
            timer.resetar()
            points.total_pontos()
            tela.tela_fim_jogo()

        colisao.snake_food()
        colisao.snake_snake()
        colisao.snake_paredes()

        # jogo (refresh da tela e tick)
        py.display.update()
        clock.tick(v_jogo)
