import pygame
import os

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
