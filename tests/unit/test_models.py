from models import Item
from tests.utils.fixtures import app_context

def test_create_item(app_context):
    item = Item(name="Test Item")
    app_context.add(item)
    app_context.commit()

    retrieved_item = app_context.get(Item, item.id)  

    assert retrieved_item is not None
    assert retrieved_item.id == item.id
    assert retrieved_item.name == "Test Item"