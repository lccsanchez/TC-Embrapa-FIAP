from app.dto.registro_quantidade_valor import RegistroQuantidadeValorDTO
from app.dto.registro_total import RegistroTotalDTO
from app.model.model import ImportacaoExportacao, Produto
from typing import List,Dict,Set

def detectar_prefixos(producoes: List[Produto]) -> Set[str]:
   
    return {
        f"{control.split('_')[0]}_"
        for producao in producoes
        if (control := producao.control) and '_' in control
    }

def model_to_dto(items: List[Produto]) -> Dict[str, RegistroTotalDTO]:

    categorias: Dict[str, RegistroTotalDTO] = {} 

    prefixos = detectar_prefixos(items)
    pai_atual = None
    
    for item in items:
        control = item.control              
        if not any(control.startswith(prefixo) for prefixo in prefixos):
            pai_atual = item
            qt_total = item.registros[0].quantidade
            categorias[pai_atual.control] = RegistroTotalDTO(                
                total= "-" if qt_total==0 else f"{qt_total:,}".replace(",",'.'),
                subitems=[]
            )
        elif pai_atual:
            qt_item=item.registros[0].quantidade   
            categorias[pai_atual.control].subitems.append({ item.produto : "-" if qt_item==0 else f"{qt_item:,}".replace(",",'.')  })
            
    return categorias 

def imp_exp_to_dto(items: List[ImportacaoExportacao]) -> Dict[str, RegistroQuantidadeValorDTO]:
    resultado: Dict[str, RegistroQuantidadeValorDTO] = {}

    for item in items:
        if item.registros_imp_exp:
            reg = item.registros_imp_exp[0]
            quantidade = reg.quantidade
            valor = reg.valor
        else:
            quantidade = 0
            valor = 0

        qtd_formatada = "-" if not quantidade else f"{quantidade:,}".replace(",", ".")
        val_formatado = "-" if not valor else f"{int(valor):,}".replace(",", ".")

        resultado[item.pais] = RegistroQuantidadeValorDTO(
            quantidade=qtd_formatada,
            valor=val_formatado
        )

    return resultado
