from model.empresa import Empresa
from conexao import Conexao
from functions.validacoes import *
from functions.formatacao import *
from prettytable import from_db_cursor

class DAOEmpresa:

    def menu(self):
        operacoes = {
            'Adicionar empresa': self.adicionar,
            'Lista de empresas': self.lista,
            'Deletar empresa': self.deleta
        }

        while True:
            limpa_tela()
            titulo('SISTEMA DE CADASTRAMENTO OU REMOÇÃO DE EMPRESAS')

            for pos, op in enumerate(operacoes.keys()):
                print(f'{pos+1:2}. {op}')
                if pos+1 == len(operacoes):
                    print(f'{pos+2:2}. Voltar')
                    
            linha()
            while not (escolha := input(' Qual operação que deseja realizar? ')).strip().isdigit() or (escolha := int(escolha)) not in list(range(1, len(operacoes)+2)):
                titulo('Por favor, digite uma opição válida!')

            if escolha == 4:
                break
            
            for pos, op in enumerate(operacoes.values()):
                if pos+1 == escolha:
                    op()


    def adicionar(self):
        try:
            con = Conexao.get_connection()
            cursor = con.cursor()

            limpa_tela()
            titulo('CADASTRAMENTO DE EMPRESAS')

            razao_social = input('\n Razão Social: ').strip().title()

            while True:
                while True:
                    try:
                        cep = CEP(input('\n CEP: ').strip())
                        break
                    except ValueError as e:
                        print(e)

                endereco = cep.logradouro()
                bairro   = cep.bairro()
                cidade   = cep.cidade()
                estado   = cep.estado()

                print(f'\n{endereco}, {bairro}, {cidade} - {estado}\n')

                resp = ' '
                while resp not in 'SN':
                    resp = input(' Os dados estão corretos? [S/N] ').strip().upper()[0]

                if resp == 'S':
                    break
                
                elif resp == 'N':
                    resp = ' '
                    while resp not in 'SN':
                        resp = input(' Deseja preencher os dados manualmente? [S/N] ').strip().upper()[0]

                    if resp == 'S':
                        while True:
                            try:
                                cep = CEP(input('CEP: ').strip())
                                break
                            except ValueError as e:
                                print(e)

                        endereco = input(' Digite a rua: ').strip().title()
                        bairro   = input(' Digite o bairro: ').strip().title()
                        cidade   = input(' Digite a cidade: ').strip().title()
                        estado   = input(' Digite o estado: ').strip().upper()

                        print(f'\n{endereco}, {bairro}, {cidade} - {estado}\n')

                        resp = ' '
                        while resp not in 'SN':
                            resp = input('Os dados estão corretos? [S/N] ').strip().upper()[0]
                        if resp == 'S':
                            break

            while True:
                try:
                    cnpj = CNPJ(input('\n CNPJ: ').strip())
                    break
                except ValueError as e:
                    print(e)

            nova_empresa = Empresa(
                razao_social=razao_social, 
                cep=cep, 
                estado=estado, 
                cidade=cidade, 
                bairro=bairro, 
                endereco=endereco, 
                cnpj=cnpj
            )

            query = "INSERT INTO empresa(RazãoSocial, CEP, Estado, Cidade, Bairro, Endereço, CNPJ) VALUES(%s,%s,%s,%s,%s,%s,%s)"

            dados = nova_empresa.razao_social,\
                    nova_empresa.cep,\
                    nova_empresa.estado,\
                    nova_empresa.cidade,\
                    nova_empresa.bairro,\
                    nova_empresa.endereco,\
                    nova_empresa.cnpj

            cursor.execute(query, dados)
            con.commit()
            subtitulo(f'{razao_social} FOI ADICIONADA COM SUCESSO!'.upper())
            input()

        except TypeError as error:
            print(f"Falha ao adicionar a empresa: {error}")
            input()

        finally:
            cursor.close()
            con.close()

    def lista(self):
        try:
            limpa_tela()
            titulo('LISTA DE EMPRESAS')

            con = Conexao.get_connection()
            cursor = con.cursor()

            query = 'SELECT ID, RazãoSocial, CEP, Estado, Cidade, Bairro, Endereço, CNPJ FROM empresa'
            cursor.execute(query)
            tabela = from_db_cursor(cursor)
            print(tabela)
            
        except TypeError as error:
            print(f"Falha ao mostrar a lista de empresas: {error}")

        finally:
            cursor.close()
            con.close()

        input()

    def deleta(self):
        try:
            con = Conexao.get_connection()
            cursor = con.cursor()

            limpa_tela()
            titulo('REMOÇÃO DE EMPRESA')

            while not (escolha := input('\n 1. Remover por ID\
                                         \n 2. Pesquisar por nome da empresa\
                                         \n 3. Lista completa de empresas\
                                         \n 4. Sair\
                                         \n Escolha uma opção: ')).strip().isdigit() or (escolha := int(escolha)) not in range(1,5):
                subtitulo('Por favor, escolha uma opção válida!')
            if escolha != 4:
                if escolha == 2:
                    while True:
                        nome_empresa = input(' Nome da Empresa: ').title()
                        cursor.execute("SELECT * FROM empresa")

                        resultados = cursor.fetchall()
                        nomes = []

                        for nome in resultados:
                            nomes.append(nome[0])
                        
                        if nome_empresa in nomes:
                            subtitulo(f'RESULTADOS PARA {nome_empresa}'.upper())

                            cursor.execute('SELECT * FROM empresa WHERE RazãoSocial = %s', nome_empresa)
                            tabela = from_db_cursor(cursor)
                            print(tabela)
                            break

                        else:
                            subtitulo('Não há resultados para a pesquisa')

                        resp = ' '
                        while resp not in 'SN':
                            resp = input(' Deseja fazer uma nova pesquisa? [S/N] ').strip().upper()

                        if resp == 'N':
                            break
                        limpa_tela()
                
                elif escolha == 3:
                    query = 'SELECT * FROM empresa'
                    cursor.execute(query)
                    tabela = from_db_cursor(cursor)
                    print(tabela)
                        
                query = 'SELECT ID, RazãoSocial FROM empresa'
                cursor.execute(query)
                resultados = cursor.fetchall()
                ids = [0]

                for id in resultados:
                    ids.append(id[0])

                while not (id_empresa := input(' Digite o ID da empresa que deseja remover\
                                              \n Ou digite 0 para cancelar: ')).strip().isdigit() or (id_empresa := int(id_empresa)) not in ids:
                    print('Por favor, digite um ID válido.')
                
                if id_empresa != 0:
                    for id, razao_social in resultados:
                        if id_empresa == id:
                            resp = ' '
                            while resp not in 'SN':
                                resp = input(f'Deseja realmente remover a empresa {razao_social}? [S/N] ').strip().upper()[0]

                            if resp == 'S':
                                subtitulo(f'REMOVENDO A EMPRESA {razao_social} DO ID {id}.'.upper())
                                input()
                                query = 'DELETE FROM empresa WHERE ID = %s'
                                cursor.execute(query, id_empresa)
                                con.commit()
                else:
                    subtitulo('OPERAÇÃO CANCELADA PELO USUÁRIO')
                    input()
            
            else:
                subtitulo('OPERAÇÃO CANCELADA PELO USUÁRIO')
                input()

        except TypeError as error:
            print(f"Falha em remover a empresa: {error}")
            input()
            
        finally:
            cursor.close()
            con.close()