from app.tools.inventory import check_inventory
 
 
def test_available_part():
 
    result = check_inventory("CF-PX500-001")
 
    assert result["part_name"] == "Cooling Fan"
    assert result["quantity"] == 3
    assert result["status"] == "AVAILABLE"
 
 
def test_out_of_stock_part():
 
    result = check_inventory("CF-PX700-001")
 
    assert result["quantity"] == 0
    assert result["status"] == "OUT_OF_STOCK"
 
 
def test_unknown_part():
 
    result = check_inventory("UNKNOWN-PART")
 
    assert result["status"] == "NOT_FOUND"