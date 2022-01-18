class Pessoa:

    def __init__(self, nome, sobrenome, cep, estado, cidade, bairro, endereco, id_empresa, empresa):
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__endereco = endereco
        self.__bairro = bairro
        self.__cep = cep
        self.__cidade = cidade
        self.__estado = estado
        self.__id_empresa = id_empresa
        self.__empresa = empresa
    

    @property
    def nome(self): return self.__nome    

    @property
    def sobrenome(self): return self.__sobrenome

    @property
    def endereco(self): return self.__endereco

    @property
    def bairro(self): return self.__bairro

    @property
    def cep(self): return self.__cep

    @property
    def cidade(self): return self.__cidade

    @property
    def estado(self): return self.__estado

    @property
    def id_empresa(self): return self.__id_empresa

    @property
    def empresa(self): return self.__empresa


    @nome.setter
    def nome(self, nome): self.__nome = nome

    @sobrenome.setter
    def sobrenome(self, sobrenome): self.__sobrenome = sobrenome

    @endereco.setter
    def endereco(self, endereco): self.__endereco = endereco

    @bairro.setter
    def bairro(self, bairro): self.__bairro = bairro

    @cidade.setter
    def cidade(self, cidade): self.__cidade = cidade

    @estado.setter
    def estado(self, estado): self.__estado = estado
    