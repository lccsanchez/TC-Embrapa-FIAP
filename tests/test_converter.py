from app.util import converter


class FakeRegistro:
    def __init__(self, quantidade):
        self.quantidade = quantidade


class FakeProduto:
    def __init__(self, control, produto, registros):
        self.control = control
        self.produto = produto
        self.registros = registros


def test_detectar_prefixos():
    produtos = [FakeProduto("vinho_tinto", "Vinho Tinto", [FakeRegistro(10)])]
    prefixos = converter.detectar_prefixos(produtos)
    assert "vinho_" in prefixos


def test_model_to_dto():
    produtos = [
        FakeProduto("vinho_tinto", "Vinho Tinto", [FakeRegistro(10)]),
        FakeProduto("vinho_branco", "Vinho Branco", [FakeRegistro(5)]),
    ]
    dto = converter.model_to_dto(produtos)
    assert isinstance(dto, dict)


def test_imp_exp_to_dto():
    class FakeReg:
        def __init__(self, quantidade, valor):
            self.quantidade = quantidade
            self.valor = valor

    class FakeItem:
        def __init__(self, pais, registros_imp_exp):
            self.pais = pais
            self.registros_imp_exp = registros_imp_exp
    items = [FakeItem("Brasil", [FakeReg(10, 100)])]
    dto = converter.imp_exp_to_dto(items)
    assert "Brasil" in dto


def test_detectar_prefixos_empty():
    assert converter.detectar_prefixos([]) == set()


def test_model_to_dto_no_subitems():
    produtos = [
        FakeProduto("vinho", "Vinho", [FakeRegistro(100)]),
        FakeProduto("vinho_tinto", "Vinho Tinto", [FakeRegistro(0)])
    ]
    dto = converter.model_to_dto(produtos)
    assert "vinho" in dto
    assert {"Vinho Tinto": "-"} in dto["vinho"].subitems


def test_model_to_dto_no_registros():
    produtos = [FakeProduto("vinho_tinto", "Vinho Tinto", [])]
    dto = converter.model_to_dto(produtos)
    assert isinstance(dto, dict)
