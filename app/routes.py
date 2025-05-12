from flask import Blueprint
from service.producao import producao_service
from service.processamento import processamento_service
from util import response 

producao = Blueprint('producao', __name__)
processamento = Blueprint('processamento', __name__)

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