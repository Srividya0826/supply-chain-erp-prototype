from modules.supplier import SupplierManager

def test_supplier_module():
    sm = SupplierManager()
    print("Adding supplier S001:", sm.add_supplier('S001', 'Supplier One', 'contact1@example.com'))
    print("Adding supplier S002:", sm.add_supplier('S002', 'Supplier Two', 'contact2@example.com'))
    print("Adding duplicate supplier S001:", sm.add_supplier('S001', 'Supplier One Duplicate', 'dup@example.com'))

    sm.update_supplier_performance('S001', delivery_time=3, quality_rating=4.5, reliability_score=90)
    sm.log_communication('S001', "Contacted about delivery delay.")
    sm.log_communication('S001', "Confirmed new delivery schedule.")

    supplier = sm.get_supplier('S001')
    print("Supplier S001 details:", supplier)

    print("All suppliers:", sm.list_suppliers())

if __name__ == "__main__":
    test_supplier_module()
