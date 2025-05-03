from flask import jsonify, Blueprint, render_template, redirect, request, session, flash
from scraper import gerar_json_agrupado
import urls
from app.models import User

processamento = Blueprint('processamento', __name__)
producao = Blueprint('producao', __name__)
comercio = Blueprint('comercio', __name__)
auth = Blueprint('auth', __name__)
home = Blueprint('base', __name__)

# Criar rotas para login e auth
""" @auth.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima) """

""" @auth.route('/autenticate', methods=['POST'])
def autenticate():
    usuario = User.query.filter_by(nickname=request.form['nickname']).first()

    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(f'Bem-vindo, {usuario.nickname}!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha incorreta!')
            return redirect('/login')
    
    else:
        flash('Usuário não encontrado!')
        return redirect('/login') """
            
@home.route("/")
def index():
    return "Bem vindo ao sistema de dados vitivinícolas!"

@processamento.route("/processamento")
def get_processamento():
    return jsonify(gerar_json_agrupado(urls.urls_processamento))

@producao.route("/producao")
def get_producao():
    return jsonify(gerar_json_agrupado(urls.url_producao))

@comercio.route("/comercio")
def get_comercializacao():
    return jsonify(gerar_json_agrupado(urls.url_comercializacao))