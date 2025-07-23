from modules.inventory import Inventory

def test_inventory():
    inv = Inventory()

    # Add 100 units of product 'P001' at batch 'B001' and location 'L001'
    inv.add_stock('P001', 100, batch_id='B001', expiry_date='2025-12-31', location_id='L001')
    print(f"After adding stock: {inv.check_stock('P001')} units")  # Expect 100

    # Add 50 more units of product 'P001' at batch 'B002' and location 'L002'
    inv.add_stock('P001', 50, batch_id='B002', expiry_date='2026-06-30', location_id='L002')
    print(f"After adding more stock: {inv.check_stock('P001')} units")  # Expect 150

    # Remove 30 units from batch 'B001' and location 'L001'
    success = inv.remove_stock('P001', 30, batch_id='B001', location_id='L001')
    print(f"Remove 30 units success? {success}")
    print(f"Stock after removal: {inv.check_stock('P001')} units")  # Expect 120

    # Check batches info
    batches = inv.get_batches('P001')
    print(f"Batches: {batches}")

    # Check locations info
    locations = inv.get_locations('P001')
    print(f"Locations: {locations}")

    # Check reorder alert at reorder point 50
    reorder_needed = inv.check_reorder('P001', reorder_point=50)
    print(f"Is reorder needed? {reorder_needed}")  # Expect False

    # Remove 80 units overall (no batch/location specified)
    inv.remove_stock('P001', 80)
    print(f"Stock after removing 80 units: {inv.check_stock('P001')}")  # Expect 40
    reorder_needed = inv.check_reorder('P001', reorder_point=50)
    print(f"Is reorder needed now? {reorder_needed}")  # Expect True

if __name__ == "__main__":
    test_inventory()
