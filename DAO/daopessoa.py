from model.pessoa import Pessoa
from model.contato import Contato
from conexao import Conexao
from functions.validacoes import CEP
from functions.formatacao import *
from prettytable import from_db_cursor

class DAOPessoa:

    def menu(self):
        operacoes = {
            'Adicionar funcionário': self.adicionar,
            'Lista de funcionários': self.lista,
            'Deletar funcionário': self.deleta,
        }

        while True:
            limpa_tela()
            titulo('SISTEMA DE CADASTRAMENTO OU REMOÇÃO DE FUNCIONÁRIOS')

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
        limpa_tela()
        
        titulo('CADASTRAMENTO DE FUNCIONÁRIOS')
        centralizado('Escolha uma opção para encontrar uma empresa e vincular a um funcionário.')
        linha()
        print(' 1. Ver a lista de empresas\
             \n 2. Pesquisar empresa\
             \n 3. Sair')
        linha()

        while not (escolha := input(' Escolha uma opção: ')).strip().isdigit() or (escolha := int(escolha)) not in list(range(1, 4)):
            subtitulo('Por favor, digite uma opção válida.')

        try:
            con = Conexao.get_connection()
            cursor = con.cursor()
            if escolha != 3:
                if escolha == 1:
                    query = 'SELECT * FROM empresa'
                    cursor.execute(query)
                    tabela = from_db_cursor(cursor)
                    print(tabela)
                
                elif escolha == 2:
                    while True:
                        consulta = input(' Digite o nome da empresa: ').strip().title()
                        query = 'SELECT * FROM empresa WHERE RazãoSocial = %s'
                        cursor.execute(query, consulta)
                        tabela = from_db_cursor(cursor)
                        print(tabela)
                        
                        resp = ' '
                        while resp not in 'SN':
                            resp = input(' A empresa que procura está nesta lista? [S/N] ').strip().upper()[0]
                        if resp == 'S':
                            break
                
                query = 'SELECT ID FROM empresa'
                cursor.execute(query)
                resultados = cursor.fetchall()
                ids = []

                for id in resultados:
                    ids.append(id[0])

                while not (id_empresa := input(' Digite o ID da empresa: ')).strip().isdigit() or (id_empresa := int(id_empresa)) not in ids:
                    subtitulo('Por favor, digite um ID válido.')

                query = 'SELECT RazãoSocial FROM empresa WHERE ID = %s'
                cursor.execute(query, id_empresa)
                empresa = cursor.fetchone()

                nome = input('Nome: ').title().strip()
                sobrenome = input('Sobrenome: ').title().strip()
                    

                while True:
                    while True:
                        try:
                            cep = CEP(input(' CEP: ').strip())
                            break
                        except ValueError as e:
                            print(e)

                    endereco = cep.logradouro()
                    bairro   = cep.bairro()
                    cidade   = cep.cidade()
                    estado   = cep.estado()

                    subtitulo(f'{endereco}, {bairro}, {cidade} - {estado}')
                    
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
                                        cep = CEP(input(' CEP: ').strip())
                                        break
                                    except ValueError as e:
                                        print(e)

                                endereco = input(' Digite a rua: ').strip().title()
                                bairro   = input(' Digite o bairro: ').strip().title()
                                cidade   = input(' Digite a cidade: ').strip().title()
                                estado   = input(' Digite o estado: ').strip().upper()

                                subtitulo(f'\n{endereco}, {bairro}, {cidade} - {estado}\n')

                                resp = ' '
                                while resp not in 'SN':
                                    resp = input(' Os dados estão corretos? [S/N] ').strip().upper()[0]
                                if resp == 'S':
                                    break

                while not (telefone := input(' Telefone: ')).strip().isdigit():
                    subtitulo('Por favor, digite apenas números.')

                while not "@" in (email := input(' Email: ').strip()):
                    subtitulo('Por favor, digite um email válido.')

                nova_pessoa = Pessoa(
                    nome=nome, 
                    sobrenome=sobrenome, 
                    endereco=endereco, 
                    bairro=bairro, 
                    cep=cep, 
                    cidade=cidade, 
                    estado=estado, 
                    id_empresa=id_empresa, 
                    empresa=empresa
                )
                novo_contato = Contato(telefone=telefone, email=email)

                query = "INSERT INTO pessoa(Nome, Sobrenome, Endereco, Bairro, CEP, Cidade, Estado, IDEmpresa, Empresa, Telefone, Email) VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                dados = nova_pessoa.nome, \
                        nova_pessoa.sobrenome, \
                        nova_pessoa.endereco, \
                        nova_pessoa.bairro, \
                        nova_pessoa.cep, \
                        nova_pessoa.cidade, \
                        nova_pessoa.estado, \
                        nova_pessoa.id_empresa, \
                        nova_pessoa.empresa, \
                        novo_contato.telefone, \
                        novo_contato.email

                cursor.execute(query, dados)
                con.commit()
                
                subtitulo(f'FUNCIONÁRIO(A) {nome} {sobrenome} ADICIONADO(A) COM SUCESSO'.upper())
                input()
            else:
                titulo('CANCELANDO OPERAÇÃO')
                input()
        
        except TypeError as error:
            print(f'Falha ao adicionar o funcionário à tabela: {error}')
            input()

        finally:
            cursor.close()
            con.close()

    def lista(self):
        try:
            limpa_tela()
            titulo("LISTA DE FUNCIONÁRIOS")

            con = Conexao.get_connection()
            cursor = con.cursor()

            query = 'SELECT ID, Nome, Sobrenome, Empresa, CEP, Estado, Cidade, Bairro, Endereco, Telefone, Email FROM pessoa'
            cursor.execute(query)
            tabela = from_db_cursor(cursor)
            print(tabela)

        except TypeError as error:
            print(f"Falha ao mostrar a lista de funcionários: {error}")

        finally:
            cursor.close()
            con.close()
        
        input()

    def deleta(self):
        try:
            con = Conexao.get_connection()
            cursor = con.cursor()
            while True:
                limpa_tela()
                titulo('REMOÇÃO DE FUNCIONÁRIOS')

                while not (escolha := input('\n 1. Remover pelo ID\
                                             \n 2. Pequisa pelo nome\
                                             \n 3. Lista completa de funcionários\
                                             \n 4. Voltar\
                                             \n Escolha uma opção: ')).strip().isdigit() or (escolha := int(escolha)) not in range(1,5):
                    subtitulo('Por favor, escolha uma opção válida!')

                if escolha != 4:
                    if escolha == 2:
                        while True:
                            nome_pessoa = input('Nome do(a) funcionário(a): ').strip()

                            query = "SELECT * FROM empresa"
                            cursor.execute(query)
                            resultados = cursor.fetchall()
                            nomes = []

                            for nome in resultados:
                                nomes.append(nome[0])
                            
                            if nome_pessoa in nomes:
                                subtitulo(f'RESULTADOS PARA {nome_pessoa}'.upper())
                                query = 'SELECT ID, Nome, Sobrenome, Empresa FROM pessoa WHERE Nome = %s'
                                cursor.execute(query, nome_pessoa)
                                tabela = from_db_cursor(cursor)
                                print(tabela)

                            else:
                                subtitulo('Não há resultados para a sua pesquisa')

                            resp = ' '
                            while resp not in 'SN':
                                resp = input('Deseja tentar novamente? [S/N] ').strip().upper()[0]

                            if resp == 'N':
                                break
                    
                    if escolha == 3:
                        subtitulo('LISTA DE FUNCIONÁRIOS')
                        query = 'SELECT ID, Nome, Sobrenome, Empresa FROM pessoa'
                        cursor.execute(query)
                        tabela = from_db_cursor(cursor)
                        print(tabela)
                            
                    query = 'SELECT ID, Nome, Sobrenome FROM pessoa'
                    cursor.execute(query)
                    resultados = cursor.fetchall()
                    ids = [0]

                    for id in resultados:
                        ids.append(id[0])

                    while not (id_pessoa := input('Digite o ID do funcionário que deseje remover\
                                                 \nOu digite 0 para cancelar: ')).strip().isdigit() or (id_pessoa := int(id_pessoa)) not in ids:
                        subtitulo('Por favor, digite um ID válido.')

                    if id_pessoa != 0:
                        for id, nome, sobrenome in resultados:
                            if id_pessoa == id:
                                resp = ' '
                                while resp not in 'SN':
                                    resp = input(f'Deseja realmente remover o(a) funcionário(a) {nome} {sobrenome}? [S/N] '.upper()).strip().upper()[0]

                                if resp == 'S':
                                    subtitulo(f'REMOVENDO O(A) FUNCIONÁRIO(A) {nome} {sobrenome} DO ID {id}.'.upper())
                                    input()
                                    query = 'DELETE FROM pessoa WHERE pessoa.ID = %s'
                                    cursor.execute(query, id_pessoa)
                                    con.commit()

                    else:
                        subtitulo('OPERAÇÃO CANCELADA PELO USUÁRIO')
                        input()
                        break

                else:
                    subtitulo('OPERAÇÃO CANCELADA PELO USUÁRIO')
                    input()

        except TypeError as error:
            print(f"Falha em remover o funcionário: {error}")
            input()

        finally:
            cursor.close()
            con.close()