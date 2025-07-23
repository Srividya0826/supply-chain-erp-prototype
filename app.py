import streamlit as st
import pandas as pd
from modules.inventory import Inventory
from modules.supplier import SupplierManager
from modules.purchase_order import PurchaseOrderManager
from modules.invoice import InvoicePaymentManager
from modules.order_fulfillment import OrderFulfillment
from modules.access_control import AccessControl
from modules.predictive_analytics import PredictiveAnalytics
from modules.alerts_notifications import AlertsNotifications
from modules.collaboration import Collaboration

# Initialize modules
inventory = Inventory()
supplier = SupplierManager()
po_manager = PurchaseOrderManager()
invoice = InvoicePaymentManager()
fulfillment = OrderFulfillment()
access = AccessControl()
predictor = PredictiveAnalytics()
alerts = AlertsNotifications()
collab = Collaboration()

st.set_page_config(page_title="Supply Chain & ERP", layout="wide")
st.title("📦 Supply Chain & ERP Prototype")

menu = [
    "Dashboard",  # Dashboard as first menu item
    "Inventory", "Suppliers", "Purchase Orders", "Invoices", "Order Fulfillment",
    "User Access", "Predictive Analytics", "Alerts", "Collaboration"
]

# Get current page from query params
params = st.query_params
if "page" in params and params["page"][0] in menu:
    current_page = params["page"][0]
else:
    current_page = "Dashboard"  # Default to Dashboard

choice = st.sidebar.selectbox("Navigate Modules", menu, index=menu.index(current_page))

# Update query params and rerun if selection changed
if choice != current_page:
    st.experimental_set_query_params(page=choice)
    # No need to call st.experimental_rerun() — Streamlit will rerun automatically


# CSS styles for cards and alerts
st.markdown("""
<style>
.metric-card {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: box-shadow 0.3s ease;
    font-size: 16px;
    font-weight: 500;
    color: #333;
    user-select: none;
    margin-bottom: 20px;
}
.metric-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #0066cc;
}
.alert-box {
    background-color: #fff3cd;
    border: 1px solid #ffeeba;
    border-radius: 6px;
    padding: 10px 15px;
    margin-bottom: 8px;
    font-weight: 600;
    color: #856404;
}
</style>
""", unsafe_allow_html=True)

# ------------------------ Dashboard ------------------------
if choice == "Dashboard":
    st.title("📊 Supply Chain & ERP Dashboard")

    # Fetch data from your modules
    total_suppliers = len(supplier.get_all_suppliers())
    inventory_items = inventory.get_all_items()
    total_inventory = len(inventory_items)
    pending_pos = len([po for po in po_manager.get_all_purchase_orders() if po["Status"] == "Pending"])
    unpaid_invoices = len([inv for inv in invoice.get_all_invoices() if inv["Status"] == "Unpaid"])

    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Suppliers'" tabindex="0" role="button" aria-pressed="false">
            <div>Total Suppliers</div><div class="metric-value">{total_suppliers}</div>
        </div>""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Inventory'" tabindex="0" role="button" aria-pressed="false">
            <div>Inventory Items</div><div class="metric-value">{total_inventory}</div>
        </div>""", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Purchase Orders'" tabindex="0" role="button" aria-pressed="false">
            <div>Pending POs</div><div class="metric-value">{pending_pos}</div>
        </div>""", unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Invoices'" tabindex="0" role="button" aria-pressed="false">
            <div>Unpaid Invoices</div><div class="metric-value">{unpaid_invoices}</div>
        </div>""", unsafe_allow_html=True)

    # Generate alerts (low stock and pending orders)
    alerts_list = []
    for item in inventory_items:
        if item["Quantity"] <= item["Reorder Point"]:
            alerts_list.append(f"⚠️ Low stock alert: {item['Name']} (Qty: {item['Quantity']})")
    for po in po_manager.get_all_purchase_orders():
        if po["Status"] == "Pending":
            alerts_list.append(f"⏳ Pending purchase order: {po['PO ID']}")

    st.markdown("### 🔔 Recent Alerts")
    if alerts_list:
        for alert_msg in alerts_list:
            st.markdown(f"<div class='alert-box'>{alert_msg}</div>", unsafe_allow_html=True)
    else:
        st.info("No new alerts at the moment.")

    # Recent purchase orders table preview
    st.markdown("### 📦 Recent Purchase Orders")
    recent_pos = po_manager.get_all_purchase_orders()
    if recent_pos:
        st.dataframe(pd.DataFrame(recent_pos).head(10))
    else:
        st.info("No purchase orders found.")

# ------------------------ Inventory ------------------------
elif choice == "Inventory":
    st.header("📦 Inventory Management")
    items = inventory.get_all_items()
    st.table(items)

    st.subheader("Add New Item")
    item_id = st.text_input("Item ID")
    name = st.text_input("Name")
    quantity = st.number_input("Quantity", step=1)
    reorder_point = st.number_input("Reorder Point", step=1)
    if st.button("Add Item"):
        success = inventory.add_item(item_id, name, quantity, reorder_point)
        st.success("Item added successfully!" if success else "Item already exists!")

# ------------------------ Suppliers ------------------------
elif choice == "Suppliers":
    st.header("🏭 Supplier Management")

    def load_suppliers():
        supplier.load_suppliers()
        return supplier.get_all_suppliers()

    def generate_supplier_id():
        existing = supplier.get_all_suppliers()
        count = len(existing) + 1
        return f"SUP{count:03d}"

    def add_supplier_and_clear():
        sname_val = st.session_state.sname_input.strip()
        contact_val = st.session_state.contact_input.strip()

        if sname_val == "" or contact_val == "":
            st.error("Please fill all supplier details.")
            return

        sid_val = generate_supplier_id()
        success = supplier.add_supplier(sid_val, sname_val, contact_val)

        if success:
            st.success(f"Supplier '{sname_val}' added with ID: {sid_val}")
            st.session_state.suppliers_data = load_suppliers()
            st.session_state.sname_input = ""
            st.session_state.contact_input = ""
        else:
            st.error("A supplier with this ID already exists.")

    if "sname_input" not in st.session_state:
        st.session_state.sname_input = ""
    if "contact_input" not in st.session_state:
        st.session_state.contact_input = ""
    if "suppliers_data" not in st.session_state:
        st.session_state.suppliers_data = load_suppliers()

    col1, col2 = st.columns([9, 1])
    with col1:
        st.subheader("Current Suppliers")
    with col2:
        if st.button("🔄", help="Refresh supplier list"):
            st.session_state.suppliers_data = load_suppliers()

    if st.session_state.suppliers_data:
        filtered_data = [
            {k: v for k, v in supplier.items() if k not in ['performance', 'communication_log']}
            for supplier in st.session_state.suppliers_data
        ]
        df = pd.DataFrame(filtered_data)
        st.dataframe(df, use_container_width=True, height=350)
    else:
        st.info("No suppliers yet.")

    st.subheader("➕ Add New Supplier")
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        st.text_input("Supplier Name", key="sname_input")
    with input_col2:
        st.text_input("Contact Info", key="contact_input")

    st.button("Add Supplier", on_click=add_supplier_and_clear)

# ------------------------ Purchase Orders ------------------------
elif choice == "Purchase Orders":
    st.header("📑 Purchase Order Management")
    orders = po_manager.get_all_purchase_orders()
    st.table(orders)

    st.subheader("Create Purchase Order")
    po_id = st.text_input("PO ID")
    sup_id = st.text_input("Supplier ID")
    itm_id = st.text_input("Item ID")
    qty = st.number_input("Quantity", step=1)
    status = st.selectbox("Status", ["Pending", "Approved", "Shipped"])
    if st.button("Create PO"):
        success = po_manager.create_purchase_order(po_id, sup_id, itm_id, qty, status)
        st.success("PO created!" if success else "PO already exists!")

# ------------------------ Invoices ------------------------
elif choice == "Invoices":
    st.header("💰 Invoice & Payment Management")
    invoices = invoice.get_all_invoices()
    st.table(invoices)

    st.subheader("Create Invoice")
    inv_id = st.text_input("Invoice ID")
    inv_po = st.text_input("PO ID")
    amount = st.number_input("Amount", step=1)
    inv_status = st.selectbox("Status", ["Unpaid", "Paid"])
    if st.button("Create Invoice"):
        success = invoice.create_invoice(inv_id, inv_po, amount, inv_status)
        st.success("Invoice created!" if success else "Invoice exists!")

# ------------------------ Order Fulfillment ------------------------
elif choice == "Order Fulfillment":
    st.header("🚚 Order Fulfillment & Logistics")
    fulfillments = fulfillment.get_all_fulfillments()
    st.table(fulfillments)

    st.subheader("Create Fulfillment")
    fid = st.text_input("Fulfillment ID")
    f_po = st.text_input("PO ID")
    ship_date = st.date_input("Shipment Date")
    carrier = st.text_input("Carrier")
    if st.button("Add Fulfillment"):
        success = fulfillment.add_fulfillment(fid, f_po, str(ship_date), carrier)
        st.success("Fulfillment added!" if success else "Already exists!")

# ------------------------ Access Control ------------------------
elif choice == "User Access":
    st.header("🔐 User Roles & Access Control")
    users = access.get_all_users()
    st.table(users)

    st.subheader("Add User")
    uid = st.text_input("User ID")
    role = st.selectbox("Role", ["Admin", "Manager", "Viewer"])
    if st.button("Add User"):
        success = access.add_user(uid, role)
        st.success("User added!" if success else "User already exists!")

# ------------------------ Predictive Analytics ------------------------
elif choice == "Predictive Analytics":
    st.header("📈 Predictive Analytics")

    st.subheader("Forecast Demand")
    demand_item = st.text_input("Item ID (for demand)")
    if st.button("Forecast"):
        forecast = predictor.forecast_demand(demand_item)
        st.info(f"Forecasted demand for {demand_item}: {forecast} units")

    st.subheader("Predict Lead Time")
    lt_supplier = st.text_input("Supplier ID (for lead time)")
    if st.button("Predict Lead Time"):
        lead_time = predictor.predict_lead_time(lt_supplier)
        st.info(f"Predicted lead time for {lt_supplier}: {lead_time} days")

# ------------------------ Alerts ------------------------
elif choice == "Alerts":
    st.header("🔔 Alerts & Notifications")

    st.subheader("Send Alert")
    alert_user = st.text_input("User ID")
    alert_type = st.text_input("Alert Type")
    alert_msg = st.text_area("Message")
    methods = st.multiselect("Delivery Methods", ["email", "sms", "in_app"])
    if st.button("Send Alert"):
        alerts.send_alert(alert_user, alert_type, alert_msg, methods)
        st.success("Alert sent!")

    st.subheader("All Alerts")
    st.table(alerts.get_alerts())

# ------------------------ Collaboration ------------------------
elif choice == "Collaboration":
    st.header("💬 Collaboration & Communication")

    st.subheader("Comments")
    cm_po = st.text_input("PO ID (for comments)")
    cm_user = st.text_input("Your User ID")
    comment = st.text_area("Comment")
    if st.button("Add Comment"):
        collab.add_comment(cm_po, cm_user, comment)
        st.success("Comment added!")

    if st.button("Show Comments"):
        st.table(collab.get_comments(cm_po))

    st.subheader("Tasks")
    t_id = st.text_input("Task ID")
    assigned_to = st.text_input("Assigned To")
    desc = st.text_input("Description")
    if st.button("Create Task"):
        collab.create_task(t_id, assigned_to, desc)
        st.success("Task created!")

    if st.button("Show Tasks"):
        st.table(collab.get_tasks(assigned_to))

    st.subheader("Messages")
    convo_id = st.text_input("Conversation ID")
    sender = st.text_input("Sender ID")
    msg = st.text_input("Message")
    if st.button("Send Message"):
        collab.send_message(convo_id, sender, msg)
        st.success("Message sent!")

    if st.button("Show Messages"):
        st.table(collab.get_messages(convo_id))
