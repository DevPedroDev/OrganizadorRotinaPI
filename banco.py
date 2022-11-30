
import sqlite3 

banco = sqlite3.connect('TerceiraIdade.db')
cursor = banco.cursor()

login = '''CREATE TABLE IF NOT EXISTS login(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login text,
    senha text
    );'''

rotina = '''CREATE TABLE IF NOT EXISTS rotina(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    necessidade TEXT,
    duracao TEXT,
    qtd_Vezes_dia TEXT,
    hr_Inicio TEXT,
    hr_Termino TEXT
    );'''

lista = [login, rotina]
for x in lista:
    cursor.execute(x)