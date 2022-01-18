from validate_docbr import CNPJ as ValidaCNPJ
import requests

class CNPJ:
    
    def __init__(self, documento):
        if self.valida(documento):
            self.cnpj = documento
        else:
            raise ValueError('CNPJ inválido!!')

    def __str__(self):
        return self.cnpj

    def valida(self, documento):
        validador = ValidaCNPJ()
        return validador.validate(documento)


class CEP:
    def __init__(self, cep):
        cep = str(cep)
        if self.cep_e_valido(cep):
            self.cep = cep
        else:
            raise ValueError('Por favor, digite um CEP válido.')

    def __str__(self):
        return self.cep

    def format_cep(self):
        return f'{self.cep[:]}'

    def cep_e_valido(self, cep):
        if len(cep) == 8:
            return True
        else:
            return False

    
    def acessa_via_cep(self):
        url = f'https://viacep.com.br/ws/{self.cep}/json/'
        r = requests.get(url)
        dados = r.json()
        return dados
    
    def bairro(self):
        return self.acessa_via_cep()['bairro']

    def cidade(self):
        return self.acessa_via_cep()['localidade']
    
    def estado(self):
        return self.acessa_via_cep()['uf']
        
    def logradouro(self):
        return self.acessa_via_cep()['logradouro']

