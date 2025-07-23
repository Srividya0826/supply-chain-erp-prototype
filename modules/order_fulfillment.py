from datetime import datetime

class OrderFulfillment:
    def __init__(self):
        self.orders = {}  # key: order_id, value: order info dict

    def create_order(self, order_id, po_id, items, ship_to, expected_delivery):
        if order_id in self.orders:
            return False  # Duplicate order
        self.orders[order_id] = {
            "po_id": po_id,
            "items": items,  # list of dicts {item_id, quantity}
            "ship_to": ship_to,
            "status": "Created",
            "created_at": datetime.now(),
            "shipping_updates": [],
            "expected_delivery": expected_delivery,
            "actual_delivery": None,
            "return_requested": False,
            "return_processed": False,
        }
        return True

    def update_shipping_status(self, order_id, status, location=None):
        if order_id not in self.orders:
            return False
        update = {
            "timestamp": datetime.now(),
            "status": status,
            "location": location,
        }
        self.orders[order_id]["shipping_updates"].append(update)
        self.orders[order_id]["status"] = status
        if status.lower() == "delivered":
            self.orders[order_id]["actual_delivery"] = datetime.now()
        return True

    def request_return(self, order_id, reason):
        if order_id not in self.orders or self.orders[order_id]["return_requested"]:
            return False
        self.orders[order_id]["return_requested"] = True
        self.orders[order_id]["return_reason"] = reason
        self.orders[order_id]["status"] = "Return Requested"
        return True

    def process_return(self, order_id):
        if order_id not in self.orders or not self.orders[order_id]["return_requested"]:
            return False
        self.orders[order_id]["return_processed"] = True
        self.orders[order_id]["status"] = "Return Processed"
        return True

    def get_order_status(self, order_id):
        return self.orders.get(order_id)

    def list_orders(self):
        return list(self.orders.values())
    
    # Add this alias method to match app.py call
    def get_all_fulfillments(self):
        return self.list_orders()
