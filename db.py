import psycopg2


class DB:
    def connect(self):
        return psycopg2.connect(host='localhost', database='p2',
                               user='postgres', password='312912')

    def get_cursor(self):
        con = psycopg2.connect(host='localhost', database='p2',
                               user='postgres', password='312912')
        return con.cursor()

    def next_url(self, cursor):
        # Executar o sql
        cursor.execute(
            f"""select new_url from urls""")

        # Recuperando o retorno do BD
        urls = cursor.fetchall()

        # Fechar o cursor
        cursor.close()

        if urls is None:
            return '00000'
        else:
            return '{:0>5}'.format( int(max(urls)[0]) + 1 )

    def find_last_url(self, cursor):
        cursor.execute(
            f"""select new_url from urls""")
        urls = cursor.fetchall()
        cursor.close()

        return '{:0>5}'.format(max(urls)[0])

    # Função Cadastrar url
    def insert_url(self, con, old_url):

        cursor = con.cursor()
        cursor.execute(f"""INSERT INTO 
        urls(old_url, new_url, acessos)
        VALUES (%s, %s, %s)""",
                       (old_url, self.next_url(con.cursor()), 0))
        con.commit()
        cursor.close()

    def change_url_by_old_url(self, cursor, url):
        cursor.execute(f"""select old_url from urls where new_url like '{url}'""")
        url = cursor.fetchone()
        cursor.close()

        return url[0]

    def update_acessos(self, con, new_url):

        cursor = con.cursor()
        cursor.execute(
            f"""select acessos from urls where new_url like '{new_url}'""")
        acessos = cursor.fetchone()
        acessos = acessos[0] + 1

        cursor.execute(
            f"""update urls set acessos={acessos} where new_url like '{new_url}'"""
        )
        con.commit()
        cursor.close()

    def get_all(self, cursor):
        cursor.execute(
            f"""select * from urls"""
        )
        all = cursor.fetchall()
        return all

"""
db = DB()
con = db.connect()
cursor = db.get_cursor()
#print(db.get_idlogin(cursor, 'rafael', '123'))
#db.update_user(con, 'admin', 'admin', True, 'admin', 'super', 'admin@admin')
db.change_url_by_old_url(cursor, '00004')
"""

"""
print(urls)
print(max(urls))
a = max(urls)[0]
print(a)
print(type(a))
a = int(a) + 1
a = '{:0>5}'.format(a)
print(a)
"""