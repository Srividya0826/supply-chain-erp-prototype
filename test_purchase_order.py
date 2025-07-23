# test_purchase_order.py

from modules.purchase_order import PurchaseOrderManager

def test_po_module():
    manager = PurchaseOrderManager()

    # Create PO
    created = manager.create_po(
        po_id="PO1001",
        supplier_id="S001",
        items=[{'item_id': 'I001', 'quantity': 10, 'price_per_unit': 15.0}],
        created_by='buyer1'
    )
    print("PO Created:", created)  # Expect True

    # Try duplicate create
    duplicate = manager.create_po(
        po_id="PO1001",
        supplier_id="S001",
        items=[{'item_id': 'I002', 'quantity': 5, 'price_per_unit': 20.0}],
        created_by='buyer1'
    )
    print("Duplicate PO create attempt:", duplicate)  # Expect False

    # Approve PO
    approved = manager.approve_po("PO1001", user='manager1')
    print("PO Approved:", approved)  # Expect True

    # Try reject after approval (should fail)
    rejected = manager.reject_po("PO1001", user='manager2')
    print("Reject after approval attempt:", rejected)  # Expect False

    # Check PO status
    status = manager.get_po_status("PO1001")
    print("PO Status:", status)  # Expect 'Approved'

    # Attach document
    attached = manager.attach_document("PO1001", "contract_PO1001.pdf")
    print("Document attached:", attached)  # Expect True

    # Get PO details
    po_details = manager.get_po("PO1001")
    print("PO Details:", po_details)

if __name__ == "__main__":
    test_po_module()
