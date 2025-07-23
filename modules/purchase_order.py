from datetime import datetime

class PurchaseOrderManager:
    def __init__(self):
        # Store POs in dict keyed by po_id
        self.purchase_orders = {}

    def create_po(self, po_id, supplier_id, items, created_by):
        """
        items: list of dicts with 'item_id', 'quantity', 'price_per_unit'
        """
        if po_id in self.purchase_orders:
            return False  # PO with same ID exists

        po = {
            'po_id': po_id,
            'supplier_id': supplier_id,
            'items': items,
            'status': 'Created',
            'created_by': created_by,
            'created_at': datetime.now(),
            'approved_by': None,
            'approved_at': None,
            'rejected_by': None,
            'rejected_at': None,
            'history': [('Created', datetime.now(), created_by)],
            'attachments': []
        }
        self.purchase_orders[po_id] = po
        return True

    def approve_po(self, po_id, user):
        po = self.purchase_orders.get(po_id)
        if not po or po['status'] != 'Created':
            return False
        po['status'] = 'Approved'
        po['approved_by'] = user
        po['approved_at'] = datetime.now()
        po['history'].append(('Approved', datetime.now(), user))
        return True

    def reject_po(self, po_id, user):
        po = self.purchase_orders.get(po_id)
        if not po or po['status'] != 'Created':
            return False
        po['status'] = 'Rejected'
        po['rejected_by'] = user
        po['rejected_at'] = datetime.now()
        po['history'].append(('Rejected', datetime.now(), user))
        return True

    def get_po_status(self, po_id):
        po = self.purchase_orders.get(po_id)
        if not po:
            return None
        return po['status']

    def get_po_history(self, po_id):
        po = self.purchase_orders.get(po_id)
        if not po:
            return None
        return po['history']

    def attach_document(self, po_id, filename):
        po = self.purchase_orders.get(po_id)
        if not po:
            return False
        po['attachments'].append(filename)
        return True

    def get_po(self, po_id):
        return self.purchase_orders.get(po_id)

    def list_pos(self):
        return list(self.purchase_orders.values())

    def get_all_purchase_orders(self):
        return self.list_pos()
