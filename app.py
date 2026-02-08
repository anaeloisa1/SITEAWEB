from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURAÇÃO DO MYSQL ---
# Formato: mysql+pymysql://USUARIO:SENHA@HOST/NOME_DO_BANCO
# Certifique-se de ter criado o banco 'db_biblioteca' no Workbench antes de rodar
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:labinfo@localhost/db_biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELO DO BANCO DE DADOS ---
class Livro(db.Model):
    __tablename__ = 'livro'
    id = db.Column(db.Integer, primary_key=True)
    ID_Conteudo = db.Column(db.Integer, unique=True, nullable=False)
    Titulo = db.Column(db.String(100), nullable=False)
    Sinopse = db.Column(db.Text, nullable=False)
    CapaPath = db.Column(db.String(200), nullable=False)

# --- ROTAS ---

@app.route('/')
def index():
    # Busca todos os livros cadastrados no MySQL
    todos_livros = Livro.query.all()
    return render_template('index.html', livros=todos_livros)

@app.route('/cadastro')
def cadastro_conteudo():
    return "<h1>Página de Cadastro</h1><p>Em breve você poderá cadastrar livros aqui.</p>"

@app.route('/arquivo/<int:idconteudo>')
def pdf(idconteudo):
    # Rota para a página individual do livro
    return f"Página do livro com ID: {idconteudo}"

@app.route('/conteudos/<tipo>')
def pag_conteudos(tipo):
    # Rota para ver todos os conteúdos de um tipo específico
    return f"Listagem de todos os conteúdos do tipo: {tipo}"

# --- INICIALIZAÇÃO ---

if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas no MySQL automaticamente se não existirem
        db.create_all()
        
        # Adiciona um livro de exemplo caso o banco esteja vazio
        if not Livro.query.first():
            exemplo = Livro(
                ID_Conteudo=1, 
                Titulo="Diários de Motocicleta", 
                Sinopse="O relato das viagens de Ernesto Guevara pela América Latina.", 
                CapaPath="capas.jpg" # O arquivo deve estar em static/diarios.jpg
            )
            db.session.add(exemplo)
            db.session.commit()
            print("Banco de dados pronto e livro de exemplo adicionado!")

    app.run(debug=True)