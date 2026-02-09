from flask import Flask, render_template, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import pymysql

# Instala o driver pymysql como substituto para o MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# --- CONFIGURAÇÃO DO BANCO DE DATOS ---
# Lembre-se de substituir 'SUA_SENHA' pela senha real do seu MySQL Workbench
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:labinfo@localhost/db_biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELO DO BANCO DE DATOS ---
class Livro(db.Model):
    __tablename__ = 'livro'
    ID_Conteudo = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(200), nullable=False)
    Sinopse = db.Column(db.Text)
    CapaPath = db.Column(db.String(255))

# --- ROTAS ---

@app.route('/')
def index():
    # Busca todos os livros para exibir nos cards do index.html
    todos_livros = Livro.query.all()
    return render_template('index.html', livros=todos_livros)

@app.route('/arquivo/<int:idconteudo>')
def arquivo(idconteudo):
    """Função que entrega o PDF baseado no ID do livro"""
    # Monta o nome: livro1.pdf, livro2.pdf, etc.
    nome_do_pdf = f"livro{idconteudo}.pdf"
    
    try:
        # Busca o arquivo dentro da pasta static/pdf/
        return send_from_directory('static/pdf', nome_do_pdf)
    except FileNotFoundError:
        return "<h1>Erro: Arquivo PDF não encontrado na pasta static/pdf/</h1>", 404

@app.route('/comunismo')
def comunismo():
    return render_template('comunismo.html')

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    app.run(debug=True)