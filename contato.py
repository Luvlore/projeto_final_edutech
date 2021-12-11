class Contato:

    def __init__(self, telefone, email):
        self.__telefone = telefone
        self.__email = email
    
    @property
    def telefone(self): return self.__telefone
    
    @property
    def email(self): return self.__email

    @telefone.setter
    def telefone(self, telefone): self.__telefone = telefone

    @email.setter
    def email(self, email): self.__email = email