from app.util.scrapping.strategy_with_subitems import WithSubItems


def test_scrape_empty():
    html = "<html></html>"
    result = WithSubItems().scrape(html)
    assert result == {}


def test_scrape_with_valid_items_and_subitems():
    html = '''
    <table class="tb_base tb_dados">
      <tr><td class="tb_item">Item1</td><td>100</td></tr>
      <tr><td class="tb_subitem">Sub1</td><td>50</td></tr>
      <tr><td class="tb_subitem">Sub2</td><td>30</td></tr>
    </table>
    '''
    result = WithSubItems().scrape(html)
    assert result["Item1"]["total"] == "100"
    assert {"Sub1": "50"} in result["Item1"]["subitems"]
    assert {"Sub2": "30"} in result["Item1"]["subitems"]


def test_scrape_subitem_without_item():
    html = '''
    <table class="tb_base tb_dados">
      <tr><td class="tb_subitem">Sub1</td><td>50</td></tr>
    </table>
    '''
    result = WithSubItems().scrape(html)
    assert result == []


def test_scrape_incomplete_item_row():
    html = '''
    <table class="tb_base tb_dados">
      <tr><td class="tb_item">Item1</td></tr>
    </table>
    '''
    result = WithSubItems().scrape(html)
    assert result == []


def test_scrape_table_no_rows():
    html = '''
    <table class="tb_base tb_dados"></table>
    '''
    result = WithSubItems().scrape(html)
    assert result == []
