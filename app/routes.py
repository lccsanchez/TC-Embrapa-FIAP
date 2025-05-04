from flask import jsonify, Blueprint, render_template, redirect, url_for, request, session, flash
from scraper import filtrar_dados, agrupar_dados
import urls
from app.models import User

processamento = Blueprint('processamento', __name__)
producao = Blueprint('producao', __name__)
comercio = Blueprint('comercio', __name__)
auth = Blueprint('auth', __name__)
home = Blueprint('home', __name__)

# Criar rotas para login e auth
@auth.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@auth.route('/autenticar', methods=['POST'])
def autenticar():
    from app.database import SessionLocal  # Importa a sessão do banco de dados
    db_session = SessionLocal()
    
    try:
        usuario = db_session.query(User).filter_by(nickname=request.form['user']).first()

        if usuario:
            if request.form['password'] == usuario.senha:
                session['usuario_logado'] = usuario.nickname
                proxima_pagina = request.form.get('proxima', url_for('home.index'))
                return redirect(proxima_pagina)
            else:
                flash('Senha incorreta!')
                return redirect('/login')
        
        else:
            flash('Usuário não encontrado!')
            return redirect(url_for('auth.login'))
    finally:
        db_session.close()

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('home.index'))
            
@home.route("/")
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('auth.login', proxima=url_for('home.index')))
    usuario_logado = session.get('usuario_logado')
    return render_template("index.html", usuario_logado=usuario_logado)

@processamento.route("/processamento", defaults={'classificacao': None, 'ano': None, 'categoria': None})
@processamento.route("/processamento/<classificacao>", defaults={'ano': None, 'categoria': None})
@processamento.route("/processamento/<classificacao>/<ano>", defaults={'categoria': None})
@processamento.route("/processamento/<classificacao>/<ano>/<categoria>")
def get_processamento(classificacao, ano, categoria):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('auth.login', proxima=url_for('processamento.get_processamento')))
    df = agrupar_dados(urls.urls_processamento)
    resultado = filtrar_dados(df, classificacao, ano, categoria)
    return jsonify(resultado)

@producao.route("/producao", defaults={'classificacao': None, 'ano': None, 'categoria': None})
@producao.route("/producao/<classificacao>", defaults={'ano': None, 'categoria': None})
@producao.route("/producao/<classificacao>/<ano>", defaults={'categoria': None})
@producao.route("/producao/<classificacao>/<ano>/<categoria>")
def get_producao(classificacao, ano, categoria):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('auth.login', proxima=url_for('producao.get_producao')))
    df = agrupar_dados(urls.url_producao)
    resultado = filtrar_dados(df, classificacao, ano, categoria)
    return jsonify(resultado)

@comercio.route("/comercio", defaults={'classificacao': None, 'ano': None, 'categoria': None})
@comercio.route("/comercio/<classificacao>", defaults={'ano': None, 'categoria': None})
@comercio.route("/comercio/<classificacao>/<ano>", defaults={'categoria': None})
@comercio.route("/comercio/<classificacao>/<ano>/<categoria>")
def get_comercio(classificacao, ano, categoria):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('auth.login', proxima=url_for('comercio.get_comercio')))
    df = agrupar_dados(urls.url_comercializacao)
    resultado = filtrar_dados(df, classificacao, ano, categoria)
    return jsonify(resultado)