from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
app = Flask(__name__, template_folder='template', static_folder='static', static_url_path='/static/')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'



def query_banco(sql):
    banco = sqlite3.connect('TerceiraIdade.db')
    cursor = banco.cursor()
    cursor.execute(sql)
    banco.commit()
    banco.close()


@app.route('/')
def pagina_principal():
    if 'username' not in session:
        return render_template('login.html')
    
    if 'Logado in session':
        print(session['username'])
        return render_template('index.html')
        
@app.route('/logar', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        banco = sqlite3.connect('TerceiraIdade.db')
        cursor = banco.cursor()
        nome =  request.form['usuario']
        senha =  request.form['senha']
        sql = "SELECT * FROM login WHERE login = '{}' and senha = '{}'".format(nome, senha)
        resultados = cursor.execute(sql).fetchall()
        for login in resultados:
            if login[1] == nome and login[2] == senha:
                session['Logado'] = True
                session['username'] = nome
                return redirect(url_for("pagina_principal"))
            else:
                msg_erro = 'Erro'
                
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')



@app.route('/valores', methods=['GET', 'POST'])
def valores():
    if request.method == 'POST':
        nome = request.form['nome']
        necessidade = request.form['necessidade']
        tempo = request.form['tempo']
        vezes_dia = request.form['vezes_dia']
        inicio = request.form['inicio']
        fim = request.form['fim']
        sql = "INSERT INTO rotina(nome, necessidade, duracao, qtd_Vezes_dia, hr_Inicio, hr_Termino) VALUES('{}','{}','{}','{}','{}','{}')".format(nome, necessidade, tempo, vezes_dia, inicio, fim)
        query_banco(sql)
        return '1'
    return "2"

@app.route('/admin')
def admin():
    if 'username' not in session:
        return render_template('login.html')
    banco = sqlite3.connect('TerceiraIdade.db')
    cursor = banco.cursor()
    sql = "SELECT * FROM rotina"
    resultados = cursor.execute(sql).fetchall()
    print(resultados)
    return render_template("admin.html", resultados = resultados)

@app.route('/excluirRotina', methods=['GET', 'POST'])
def excluirRotina():
    if request.method == 'POST':
        id = request.form['excluir']
        sql = "DELETE FROM rotina WHERE id = '{}'".format(id)
        query_banco(sql)
        return "1"

@app.route('/editarRotina', methods=['GET', 'POST'])
def editarRotina():
    if request.method == 'POST':
        id = request.form["id"]
        nome = request.form["nome"]
        necessidade = request.form["necessidade"]
        duracao = request.form["duracao"]
        v_dia = request.form["v_dia"]
        inicio = request.form["inicio"]
        fim = request.form["fim"]
        
        sql = "UPDATE rotina SET nome = '{}', necessidade = '{}', duracao = '{}', qtd_Vezes_dia = '{}', hr_Inicio = '{}', hr_Termino = '{}' WHERE id = '{}'".format(nome, necessidade, duracao, v_dia, inicio, fim, id)
        query_banco(sql)
        return "1"
    return "2"

if __name__ == '__main__':
    app.run(port=8080, debug=True)