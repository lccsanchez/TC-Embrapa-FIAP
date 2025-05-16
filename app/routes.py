from flask import Blueprint
from service.producao import producao_service
from service.processamento import processamento_service
from service.importacao import importacao_service
from service.exportacao import exportacao_service
from service.comercio import comercio_service
from util import response 

producao = Blueprint('producao', __name__)
processamento = Blueprint('processamento', __name__)
comercializacao = Blueprint("comercializacao", __name__)
importacao = Blueprint("importacao", __name__)
exportacao = Blueprint("exportacao", __name__)

@producao.route("/producao", defaults={'year': None}) 
@producao.route("/producao/<year>") 
def get_producao(year):        
     return response.build_response(producao_service.find_all() if year is None else producao_service.find_by_year(year))


@producao.route("/producao", defaults={'year': None} ,methods=['POST'])
def save_all(year):        
     producao_service.save_all()
     return "OK"

@processamento.route("/processamento") 
def get_processamento_all():  
     return response.build_response(processamento_service.find_all())  

@processamento.route("/processamento/<year>", defaults={'classification':None}) 
@processamento.route("/processamento/<year>/<classification>", defaults={'classification':'ProcessaViniferas'}) 
def get_processamento(year,classification):        
     return response.build_response(processamento_service.find_by_year(year,classification))


@producao.route("/processamento",methods=['POST'])
def processamento_save_all():        
    processamento_service.save_all()
    return "OK"


@comercializacao.route("/comercializacao", defaults={"year": None})
@comercializacao.route("/comercializacao/<year>")
def get_comercializacao(year):
    return response.build_response(
        comercio_service.find_all()
        if year is None
        else comercio_service.find_by_year(year)
    )

@comercializacao.route("/comercializacao", defaults={"year": None}, methods=["POST"])
def save_all(year):
    comercio_service.save_all()
    return "OK"


@importacao.route("/importacao")
def get_importacao_all():
    return response.build_response(importacao_service.find_all())


@importacao.route("/importacao/<year>", defaults={"classification": None})
@importacao.route(
    "/importacao/<year>/<classification>",
    defaults={"classification": "ImpVinhos"},
)
def get_importacao(year, classification):
    return response.build_response(
        importacao_service.find_by_year(year, classification)
    )


@producao.route("/importacao", methods=["POST"])
def importacao_save_all():
    importacao_service.save_all()
    return "OK"


@exportacao.route("/exportacao")
def get_exportacao_all():
    return response.build_response(exportacao_service.find_all())


@exportacao.route("/exportacao/<year>", defaults={"classification": None})
@exportacao.route(
    "/exportacao/<year>/<classification>",
    defaults={"classification": "ExpVinho"},
)
def get_exportacao(year, classification):
    return response.build_response(
        exportacao_service.find_by_year(year, classification)
    )


@producao.route("/exportacao", methods=["POST"])
def exportacao_save_all():
    exportacao_service.save_all()
    return "OK"
