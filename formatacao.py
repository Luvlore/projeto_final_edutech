import os

def linha():
    print('-'*150)

def centralizado(texto):
    print(f'{texto:^150}')

def pula_linha():
    print()

def subtitulo(texto):
    linha()
    centralizado(texto)
    linha()

def titulo(texto):
    linha()
    pula_linha()
    centralizado(texto)
    pula_linha()
    linha()

def limpa_tela():
    os.system('cls')