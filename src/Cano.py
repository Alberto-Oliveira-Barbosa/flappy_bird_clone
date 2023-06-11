import pygame
import os
import random
from src.config import VELOCIDADE_GERAL

class Cano:
    DISTANCIA_ENTRE_CANOS = 200
    VELOCIDADE = VELOCIDADE_GERAL
    SPRITE_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','pipe.png')))


    def __init__(self,x):
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

        distancia_topo = (self.x - passaro.x, self.posicao_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.posicao_base - round(passaro.y))

        colisao_topo = passaro_mask.overlap(topo_mask, distancia_topo)
        colisao_base = passaro_mask.overlap(base_mask, distancia_base)

        if colisao_base or colisao_topo:
            return True
        else:
            return False
