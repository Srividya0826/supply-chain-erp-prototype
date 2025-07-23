from modules.invoice import InvoicePaymentManager
from datetime import datetime, timedelta

def test_invoice_module():
    manager = InvoicePaymentManager()

    # Create invoice
    created = manager.create_invoice('INV1001', 'PO1001', 1500)
    print("Invoice Created:", created)

    # Duplicate invoice creation attempt
    duplicate = manager.create_invoice('INV1001', 'PO1001', 1500)
    print("Duplicate Invoice Creation Attempt:", duplicate)

    # Record partial payment
    payment1 = manager.record_payment('INV1001', 500)
    print("First Payment Recorded:", payment1)

    # Record second payment
    payment2 = manager.record_payment('INV1001', 1000)
    print("Second Payment Recorded:", payment2)

    # Get invoice details
    invoice = manager.get_invoice('INV1001')
    print("Invoice Details:", invoice)

    # Create overdue invoice and check status update
    overdue_date = datetime.now() - timedelta(days=30)
    manager.create_invoice('INV1002', 'PO1002', 1000, invoice_date=overdue_date)
    manager.record_payment('INV1002', 200)
    overdue_invoice = manager.get_invoice('INV1002')
    print("Overdue Invoice Details:", overdue_invoice)

if __name__ == "__main__":
    test_invoice_module()
