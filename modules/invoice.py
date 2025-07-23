from datetime import datetime

class InvoicePaymentManager:
    def __init__(self):
        # Store invoices by invoice_id
        self.invoices = {}

    def create_invoice(self, invoice_id, po_id, amount, invoice_date=None):
        if invoice_id in self.invoices:
            return False  # Invoice already exists

        if invoice_date is None:
            invoice_date = datetime.now()

        self.invoices[invoice_id] = {
            'invoice_id': invoice_id,
            'po_id': po_id,
            'amount': amount,
            'invoice_date': invoice_date,
            'payment_status': 'Pending',  # Pending, Paid, Overdue
            'payment_history': []  # List of dicts: {'date':..., 'amount':...}
        }
        return True

    def record_payment(self, invoice_id, amount, payment_date=None):
        if invoice_id not in self.invoices:
            return False  # Invoice doesn't exist

        if payment_date is None:
            payment_date = datetime.now()

        invoice = self.invoices[invoice_id]
        total_paid = sum(p['amount'] for p in invoice['payment_history']) + amount

        invoice['payment_history'].append({
            'date': payment_date,
            'amount': amount
        })

        # Update payment status
        if total_paid >= invoice['amount']:
            invoice['payment_status'] = 'Paid'
        elif datetime.now() > invoice['invoice_date']:
            invoice['payment_status'] = 'Overdue'
        else:
            invoice['payment_status'] = 'Pending'

        return True

    def get_invoice(self, invoice_id):
        return self.invoices.get(invoice_id)

    def get_all_invoices(self):
        return list(self.invoices.values())
