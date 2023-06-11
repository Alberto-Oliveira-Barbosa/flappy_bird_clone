import pygame
import os
import random

# configuração do jogo
TELA_LARGURA = 500
TELA_ALTURA = 800
VELOCIDADE_GERAL = 5
FPS = 30

class Passaro:
    
    SPRITES_PASSARO = [
        pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','bird1.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','bird2.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','bird3.png'))),
    ]

    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.SPRITES_PASSARO[0]

    def pular(self):
        self.salto = -10.5
        self.velocidade = self.salto
        self.tempo = 0
        self.altura = self.y

    def mover(self):

        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # angulo do passaro
        if deslocamento <0 or self.y <(self.altura+ 50):
            if self.angulo< self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
            else:
                if self.angulo > -90:
                    self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self,tela):
        self.contagem_imagem += 1

        # seleciona as imagens para a batida de asas
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.SPRITES_PASSARO[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.SPRITES_PASSARO[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.SPRITES_PASSARO[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.SPRITES_PASSARO[1]
        # elif self.contagem_imagem < self.SPRITES_PASSARO + 1:
        else:
            self.imagem = self.SPRITES_PASSARO[0]
        
        # ajusta a imagem da queda do pássaro
        if self.angulo <= -80:
            self.imagem = self.SPRITES_PASSARO[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        # desenha a rotação dos passaro dentro da caixa de colisão
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        caixa_colisao = imagem_rotacionada.get_rect(center=centro_imagem)
        tela.blit(imagem_rotacionada, caixa_colisao.topleft)

    def get_mask(self):
        # cria uma mascara de colisão para o formato da imagem
        return pygame.mask.from_surface(self.imagem)



class Cano:
    DISTANCIA_ENTRE_CANOS = 200
    VELOCIDADE = VELOCIDADE_GERAL
    SPRITE_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','pipe.png')))


    def __init__(self,x) -> None:
        self.x = x
        self.altura = 0
        self.posicao_topo = 0
        self.posicao_base = 0
        self.CANO_TOPO = pygame.transform.flip(self.SPRITE_CANO, False, True)
        self.CANO_BASE = self.SPRITE_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        limite_superior = 50
        limite_inferior = 450
        self.altura = random.randrange(limite_superior, limite_inferior)
        # lembrando que no pygame a posisão 0 para X/Y é no topo esquerdo
        # da tela e por isso um aumento em Y é direcionado para baixo 
        self.posicao_topo = self.altura - self.CANO_TOPO.get_height()
        self.posicao_base = self.altura + self.DISTANCIA_ENTRE_CANOS

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.posicao_topo))
        tela.blit(self.CANO_BASE, (self.x, self.posicao_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, round(self.posicao_topo) - round(passaro.y))
        distancia_base = (self.x - passaro.x, round(self.posicao_base) - round(passaro.y))

        colisao_topo = passaro_mask.overlap(topo_mask, distancia_topo)
        colisao_base = passaro_mask.overlap(base_mask, distancia_base)

        if colisao_base or colisao_topo:
            return True
        else:
            return False


class Piso:
    SPRITE_PISO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','base.png')))
    VELOCIDADE = VELOCIDADE_GERAL
    LARGURA = SPRITE_PISO.get_width()
    IMAGEM = SPRITE_PISO

    def __init__(self, y) -> None:
        self.y = y
        self.piso_inicial_x = 0
        self.piso_posterior_x = self.LARGURA

    def mover(self):
        self.piso_inicial_x -= self.VELOCIDADE
        self.piso_posterior_x -= self.VELOCIDADE

        if self.piso_inicial_x + self.LARGURA < 0:
            self.piso_inicial_x = self.LARGURA + self.piso_posterior_x

        if self.piso_posterior_x + self.LARGURA < 0:
            self.piso_posterior_x = self.LARGURA + self.piso_inicial_x

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.piso_inicial_x, self.y))
        tela.blit(self.IMAGEM, (self.piso_posterior_x, self.y))


def desenhar_tela(tela, passaro, canos, piso, pontos, vidas):

    pygame.font.init()
    FONTE_PLACAR = pygame.font.SysFont('arial', 50)
    SPRITE_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','bg.png')))
    
    tela.blit(SPRITE_FUNDO, (0,0))

    passaro.desenhar(tela)
    
    for cano in canos:
        cano.desenhar(tela)
    
    txt_placar = FONTE_PLACAR.render(f"PONTUAÇÃO: {pontos}\nVIDAS: {vidas}",1,(255,255,255))
    tela.blit(txt_placar, (TELA_LARGURA - 10 - txt_placar.get_width(), 10))
    piso.desenhar(tela)
    pygame.display.update()


def run_game():
    ativo = True
    adicionar_cano = False
    remover_canos = []
    posicao_piso_inicial = 730
    posicao_cano_inicial = 700
    posicao_canos_posteriores = 600
    posicao_passaro_inicial = (230,350)
    vidas = 3
    
    pontos = 0
    passaro = Passaro(*posicao_passaro_inicial)
    piso = Piso(posicao_piso_inicial)
    canos = [Cano(posicao_cano_inicial)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    timer = pygame.time.Clock()

    while ativo:
        timer.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ativo = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    passaro.pular()

        passaro.mover()
        piso.mover()

        for cano in canos:
            if cano.colidir(passaro):
                # passaros.pop()
                print('colidiu - 219')
                vidas =- 1
                continue
            # passaro passou do ponto inicial do cano
            # adiciona um novo cano
            if not cano.passou and passaro.x > cano.x:
                cano.passou = True
                adicionar_cano = True
            
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(posicao_canos_posteriores))

        if len(remover_canos) > 0:
            for cano in remover_canos:
                canos.remove(cano)

        colidiu_piso = (passaro.y + passaro.imagem.get_height()) > piso.y
        colidiu_teto = passaro.y < 0 

        if colidiu_piso or colidiu_teto:
            vidas =- 1

        desenhar_tela(tela, passaro, canos, piso, pontos, vidas)


if __name__ == '__main__':
    run_game()
