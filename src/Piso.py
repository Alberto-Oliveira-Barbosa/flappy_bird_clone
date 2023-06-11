import pygame
import os
from src.config import VELOCIDADE_GERAL


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