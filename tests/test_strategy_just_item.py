from app.util.scrapping.strategy_just_item import JustItems


def test_scrape_empty():
    html = "<html></html>"
    result = JustItems().scrape(html)
    assert result == {}


def test_scrape_with_valid_items():
    html = '''
    <table class="tb_base tb_dados">
      <tr><td>Pais1</td><td>10</td><td>100</td></tr>
      <tr><td>Pais2</td><td>20</td><td>200</td></tr>
    </table>
    '''
    result = JustItems().scrape(html)
    assert result == {
        "Pais1": {"Quantidade": "10", "Valor": "100"},
        "Pais2": {"Quantidade": "20", "Valor": "200"}
    }


def test_scrape_table_no_rows():
    html = '''
    <table class="tb_base tb_dados"></table>
    '''
    result = JustItems().scrape(html)
    assert result == {}


def test_scrape_incomplete_rows():
    html = '''
    <table class="tb_base tb_dados">
      <tr><td>Pais1</td><td>10</td></tr>
    </table>
    '''
    result = JustItems().scrape(html)
    assert result == {}
