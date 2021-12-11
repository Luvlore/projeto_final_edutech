import pymysql

class Conexao:

    @staticmethod
    def get_connection():
        con = pymysql.connect(
                host='localhost',
                user='root',
                passwd='',
                database='projeto_final'
            )

        return con
