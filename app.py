import pygame
import os 
from src.config import TELA_ALTURA, TELA_LARGURA, FPS
from src.Passaro import Passaro
from src.Cano import Cano
from src.Piso import Piso

def desenhar_tela(tela, passaro, canos, piso, pontos, vidas):

    pygame.font.init()
    FONTE_PLACAR = pygame.font.SysFont('arial', 50)
    SPRITE_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'images','bg.png')))
    
    tela.blit(SPRITE_FUNDO, (0,0))

    passaro.desenhar(tela)
    
    for cano in canos:
        cano.desenhar(tela)
    
    txt_placar = FONTE_PLACAR.render(f"PONTUAÇÃO: {pontos}",1,(255,255,255))
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
                vidas =- 1
                
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

        for cano in remover_canos:
            canos.remove(cano)

        colidiu_piso = (passaro.y + passaro.imagem.get_height()) > piso.y
        colidiu_teto = passaro.y < 0 

        if colidiu_piso or colidiu_teto:
            vidas =- 1

        desenhar_tela(tela, passaro, canos, piso, pontos, vidas)


if __name__ == '__main__':
    run_game()
