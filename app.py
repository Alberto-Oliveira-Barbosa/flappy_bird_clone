import pygame
import os
import random

# configuração da tela
TELA_LARGURA = 500
TELA_ALTURA = 800
pygame.font.init()
FONTE_PLACAR = pygame.font.SysFont('arial', 50)

# personagem e cenário
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','base.png')))
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','pipe.png')))
IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','bg.png')))




class Passaro:
    
    IMAGENS_PASSARO = [
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
        self,imagem = self.IMAGENS_PASSARO[0]

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

    def desenhar(self):
        pass


class Cano:
    pass

class Chao:
    pass


