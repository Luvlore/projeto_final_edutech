from DAO.daopessoa import DAOPessoa
from DAO.daoempresa import DAOEmpresa
from functions.formatacao import *

def menu():

    opcoes = {
        'Funcionários': DAOPessoa,
        'Empresas': DAOEmpresa
    }        
    
    while True:
        limpa_tela()
        titulo('BEM VINDO(A) AO SISTEMA DE CADASTRAMENTO/REMOÇÃO')

        for pos, op in enumerate(opcoes.keys()):
            print(f'{pos+1:2}. {op}')
            if pos + 1 >= len(opcoes):
                print(f'{pos+2:2}. Sair')

        linha()

        while not (escolha := input(' Escolha uma opção: ')).strip().isdigit() or (escolha := int(escolha)) not in list(range(1, len(opcoes)+2)):
            print('Pro favor, digite uma opção válida!')

        if escolha < len(opcoes) + 1:
            limpa_tela()
            for pos, op in enumerate(opcoes.values()):
                if escolha == pos+1:
                    op().menu()
        else:
            subtitulo('FIM DO PROGRAMA')
            break


if __name__ == '__main__':
    menu()