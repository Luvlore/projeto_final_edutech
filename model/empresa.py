class Empresa:

    def __init__(self, razao_social, cep, estado, cidade, bairro, endereco, cnpj):
        self.__razao_social = razao_social
        self.__cep = cep
        self.__estado = estado
        self.__cidade = cidade
        self.__bairro = bairro
        self.__endereco = endereco
        self.__cnpj = cnpj

    @property
    def razao_social(self): return self.__razao_social
    
    @property
    def cep(self):                   return self.__cep

    @property
    def estado(self):             return self.__estado

    @property
    def cidade(self):             return self.__cidade

    @property
    def bairro(self):             return self.__bairro

    @property
    def endereco(self):         return self.__endereco
    
    @property
    def cnpj(self):                 return self.__cnpj

    
    @razao_social.setter
    def razao_social(self, razao_social): self.__razao_social = razao_social

    @cep.setter
    def cep(self, cep):                                     self.__cep = cep

    @estado.setter
    def estado(self, estado):                         self.__estado = estado

    @cidade.setter
    def cidade(self, cidade):                         self.__cidade = cidade

    @bairro.setter
    def bairro(self, bairro):                         self.__bairro = bairro
    
    @endereco.setter
    def endereco(self, endereco):                 self.__endereco = endereco
   
    @cnpj.setter
    def cnpj(self, cnpj):                                 self.__cnpj = cnpj
