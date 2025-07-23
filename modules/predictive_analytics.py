from datetime import datetime, timedelta
import statistics

class PredictiveAnalytics:
    def __init__(self):
        # Store historical orders and deliveries for predictions
        self.order_history = []  # list of dicts {date, item_id, quantity}
        self.delivery_history = []  # list of dicts {supplier_id, order_id, delivery_days}

    def add_order(self, date, item_id, quantity):
        self.order_history.append({
            "date": date,
            "item_id": item_id,
            "quantity": quantity
        })

    def add_delivery(self, supplier_id, order_id, order_date, delivery_date):
        days_taken = (delivery_date - order_date).days
        self.delivery_history.append({
            "supplier_id": supplier_id,
            "order_id": order_id,
            "delivery_days": days_taken
        })

    def forecast_demand(self, item_id, days_ahead=30):
        # Simple moving average of last 30 days orders for the item
        today = datetime.now()
        relevant_orders = [o for o in self.order_history 
                           if o["item_id"] == item_id and (today - o["date"]).days <= 30]
        total_qty = sum(o["quantity"] for o in relevant_orders)
        avg_daily = total_qty / 30 if total_qty else 0
        return avg_daily * days_ahead

    def predict_lead_time(self, supplier_id):
        # Average delivery days for the supplier
        deliveries = [d["delivery_days"] for d in self.delivery_history if d["supplier_id"] == supplier_id]
        if deliveries:
            return round(statistics.mean(deliveries), 2)
        return None
