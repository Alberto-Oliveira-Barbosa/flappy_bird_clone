import pygame
import os
import random

# configuração da tela
TELA_LARGURA = 500
TELA_ALTURA = 800
VELOCIDADE_GERAL = 5
pygame.font.init()
FONTE_PLACAR = pygame.font.SysFont('arial', 50)

# personagem e cenário
SPRITE_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','bg.png')))




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
        elif self.contagem_imagem < self.SPRITES_PASSARO * 2:
            self.imagem = self.SPRITES_PASSARO[1]
        elif self.contagem_imagem < self.SPRITES_PASSARO * 3:
            self.imagem = self.SPRITES_PASSARO[2]
        elif self.contagem_imagem < self.SPRITES_PASSARO * 3:
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
        pygame.mask.from_surface(self.imagem)



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

    def definir_atura(self):
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
        tela.blit(self.CANO_TOPO(self.x, self.posicao_topo))
        tela.blit(self.CANO_BASE(self.x, self.posicao_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, round(self.posicao_topo) - round(passaro.y))
        distancia_base = (self.x - passaro.x, round(self.posicao_base) - round(passaro.y))

        colisao_topo = passaro_mask.mask.overlap(topo_mask, distancia_topo)
        colisao_base = passaro_mask.mask.overlap(base_mask, distancia_base)

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
            self.piso_inicial_x += self.LARGURA

        if self.piso_posterior_x + self.LARGURA < 0:
            self.piso_posterior_x += self.LARGURA

    
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.piso_inicial_x, self.y))
        tela.blit(self.IMAGEM, (self.piso_posterior_x, self.y))


