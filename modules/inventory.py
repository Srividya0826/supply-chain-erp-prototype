class Inventory:
    def __init__(self):
        # stock_data structure:
        # {product_id: {'total_qty': int,
        #               'batches': {batch_id: {'qty': int, 'expiry_date': str}},
        #               'locations': {location_id: qty}}}
        self.stock_data = {}

    def add_stock(self, product_id, quantity, batch_id=None, expiry_date=None, location_id=None):
        if product_id not in self.stock_data:
            self.stock_data[product_id] = {
                'total_qty': 0,
                'batches': {},
                'locations': {}
            }

        self.stock_data[product_id]['total_qty'] += quantity

        # Handle batch info
        if batch_id:
            if batch_id in self.stock_data[product_id]['batches']:
                self.stock_data[product_id]['batches'][batch_id]['qty'] += quantity
            else:
                self.stock_data[product_id]['batches'][batch_id] = {
                    'qty': quantity,
                    'expiry_date': expiry_date
                }

        # Handle location info
        if location_id:
            if location_id in self.stock_data[product_id]['locations']:
                self.stock_data[product_id]['locations'][location_id] += quantity
            else:
                self.stock_data[product_id]['locations'][location_id] = quantity

    def remove_stock(self, product_id, quantity, batch_id=None, location_id=None):
        if product_id not in self.stock_data or self.stock_data[product_id]['total_qty'] < quantity:
            return False  # Not enough stock

        # Remove from total
        self.stock_data[product_id]['total_qty'] -= quantity

        # Remove from batch if specified
        if batch_id:
            if batch_id in self.stock_data[product_id]['batches']:
                if self.stock_data[product_id]['batches'][batch_id]['qty'] >= quantity:
                    self.stock_data[product_id]['batches'][batch_id]['qty'] -= quantity
                else:
                    return False  # Not enough stock in this batch
            else:
                return False  # Batch not found

        # Remove from location if specified
        if location_id:
            if location_id in self.stock_data[product_id]['locations']:
                if self.stock_data[product_id]['locations'][location_id] >= quantity:
                    self.stock_data[product_id]['locations'][location_id] -= quantity
                else:
                    return False  # Not enough stock in location
            else:
                return False  # Location not found

        return True

    def check_stock(self, product_id):
        return self.stock_data.get(product_id, {}).get('total_qty', 0)

    def get_batches(self, product_id):
        return self.stock_data.get(product_id, {}).get('batches', {})

    def get_locations(self, product_id):
        return self.stock_data.get(product_id, {}).get('locations', {})

    def check_reorder(self, product_id, reorder_point):
        current_qty = self.check_stock(product_id)
        return current_qty <= reorder_point

    # <-- Add this method -->
    def get_all_items(self):
        # Returns a list of dicts summarizing each product_id and total quantity
        return [
            {
                "Product ID": pid,
                "Total Quantity": pdata["total_qty"],
                "Batch Count": len(pdata["batches"]),
                "Location Count": len(pdata["locations"])
            }
            for pid, pdata in self.stock_data.items()
        ]
