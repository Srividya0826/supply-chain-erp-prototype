# test_order_fulfillment.py

from datetime import datetime, timedelta
from modules.order_fulfillment import OrderFulfillment

def run_tests():
    fulfillment = OrderFulfillment()

    # Test create_order
    order_id = "ORD1001"
    po_id = "PO1001"
    items = [{"item_id": "I001", "quantity": 5}]
    ship_to = "123 Main St, New York, NY"
    expected_delivery = datetime.now() + timedelta(days=5)

    assert fulfillment.create_order(order_id, po_id, items, ship_to, expected_delivery) == True
    assert fulfillment.create_order(order_id, po_id, items, ship_to, expected_delivery) == False  # duplicate

    # Test update_shipping_status
    assert fulfillment.update_shipping_status(order_id, "Shipped", "Warehouse A") == True
    assert fulfillment.update_shipping_status(order_id, "Delivered", "Customer Address") == True
    assert fulfillment.update_shipping_status("invalid_id", "Shipped") == False

    # Test request_return
    assert fulfillment.request_return(order_id, "Damaged item") == True
    assert fulfillment.request_return(order_id, "Another reason") == False  # already requested
    assert fulfillment.request_return("invalid_id", "Reason") == False

    # Test process_return
    assert fulfillment.process_return(order_id) == True
    assert fulfillment.process_return(order_id) == True  # can process multiple times but state remains processed
    assert fulfillment.process_return("invalid_id") == False

    # Test get_order_status
    status = fulfillment.get_order_status(order_id)
    assert status is not None
    print("Order Status:", status)

    # Test list_orders
    orders = fulfillment.list_orders()
    assert isinstance(orders, list)
    print("All orders:", orders)

    print("All Order Fulfillment tests passed!")

if __name__ == "__main__":
    run_tests()
