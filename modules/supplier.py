import json
import os

class Supplier:
    def __init__(self, supplier_id, name, contact_info):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info
        self.performance = {
            'delivery_time_avg_days': None,
            'quality_rating': None,
            'reliability_score': None
        }
        self.communication_log = []

    def update_performance(self, delivery_time=None, quality_rating=None, reliability_score=None):
        if delivery_time is not None:
            self.performance['delivery_time_avg_days'] = delivery_time
        if quality_rating is not None:
            self.performance['quality_rating'] = quality_rating
        if reliability_score is not None:
            self.performance['reliability_score'] = reliability_score

    def add_communication(self, message):
        self.communication_log.append(message)

    def get_summary(self):
        return {
            'supplier_id': self.supplier_id,
            'name': self.name,
            'contact_info': self.contact_info,
            'performance': self.performance,
            'communication_log': self.communication_log
        }

class SupplierManager:
    def __init__(self, filename="suppliers.json"):
        self.suppliers = {}
        self.filename = filename
        self.load_suppliers()

    def add_supplier(self, supplier_id, name, contact_info):
        if supplier_id in self.suppliers:
            return False  # Supplier already exists
        self.suppliers[supplier_id] = Supplier(supplier_id, name, contact_info)
        self.save_suppliers()
        return True

    def update_supplier_performance(self, supplier_id, delivery_time=None, quality_rating=None, reliability_score=None):
        if supplier_id not in self.suppliers:
            return False
        self.suppliers[supplier_id].update_performance(delivery_time, quality_rating, reliability_score)
        self.save_suppliers()
        return True

    def log_communication(self, supplier_id, message):
        if supplier_id not in self.suppliers:
            return False
        self.suppliers[supplier_id].add_communication(message)
        self.save_suppliers()
        return True

    def get_supplier(self, supplier_id):
        if supplier_id in self.suppliers:
            return self.suppliers[supplier_id].get_summary()
        return None

    def get_all_suppliers(self):
        return [s.get_summary() for s in self.suppliers.values()]

    def save_suppliers(self):
        data = {sid: supplier.get_summary() for sid, supplier in self.suppliers.items()}
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4, default=str)

    def load_suppliers(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                for sid, sup_data in data.items():
                    supplier = Supplier(sid, sup_data['name'], sup_data['contact_info'])
                    supplier.performance = sup_data.get('performance', {})
                    supplier.communication_log = sup_data.get('communication_log', [])
                    self.suppliers[sid] = supplier
