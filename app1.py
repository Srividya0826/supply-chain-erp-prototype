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

menu = [
    "Dashboard",
    "Inventory", "Suppliers", "Purchase Orders", "Invoices", "Order Fulfillment",
    "User Access", "Predictive Analytics", "Alerts", "Collaboration"
]

# Get current page from query params or default
params = st.experimental_get_query_params()
if "page" in params and params["page"][0] in menu:
    current_page = params["page"][0]
else:
    current_page = "Dashboard"

# Sidebar navigation
choice = st.sidebar.selectbox("Navigate Modules", menu, index=menu.index(current_page))

# Sync query params with sidebar choice and rerun if changed
if choice != current_page:
    st.experimental_set_query_params(page=choice)
    st.experimental_rerun()

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

# -------- Dashboard Page --------
if choice == "Dashboard":
    st.title("📊 Supply Chain & ERP Dashboard")

    total_suppliers = len(supplier.get_all_suppliers())
    inventory_items = inventory.get_all_items()
    total_inventory = len(inventory_items)
    pending_pos = len([po for po in po_manager.get_all_purchase_orders() if po["Status"] == "Pending"])
    unpaid_invoices = len([inv for inv in invoice.get_all_invoices() if inv["Status"] == "Unpaid"])

    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Suppliers'" role="button" tabindex="0">
            <div>Total Suppliers</div><div class="metric-value">{total_suppliers}</div>
        </div>""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Inventory'" role="button" tabindex="0">
            <div>Inventory Items</div><div class="metric-value">{total_inventory}</div>
        </div>""", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Purchase Orders'" role="button" tabindex="0">
            <div>Pending POs</div><div class="metric-value">{pending_pos}</div>
        </div>""", unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card" onclick="window.location.href='?page=Invoices'" role="button" tabindex="0">
            <div>Unpaid Invoices</div><div class="metric-value">{unpaid_invoices}</div>
        </div>""", unsafe_allow_html=True)

    # Alerts
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

    # Recent PO Table
    st.markdown("### 📦 Recent Purchase Orders")
    recent_pos = po_manager.get_all_purchase_orders()
    if recent_pos:
        st.dataframe(pd.DataFrame(recent_pos).head(10))
    else:
        st.info("No purchase orders found.")

# -------- Inventory Page --------
elif choice == "Inventory":
    st.header("📦 Inventory Management")
    # TODO: Add inventory module UI here
    st.info("Inventory module content goes here.")

# -------- Suppliers Page --------
elif choice == "Suppliers":
    st.header("🏭 Supplier Management")
    # TODO: Add suppliers module UI here
    st.info("Suppliers module content goes here.")

# -------- Purchase Orders Page --------
elif choice == "Purchase Orders":
    st.header("📑 Purchase Order Management")
    # TODO: Add purchase orders module UI here
    st.info("Purchase Orders module content goes here.")

# -------- Invoices Page --------
elif choice == "Invoices":
    st.header("💰 Invoice & Payment Management")
    # TODO: Add invoices module UI here
    st.info("Invoices module content goes here.")

# -------- Order Fulfillment Page --------
elif choice == "Order Fulfillment":
    st.header("🚚 Order Fulfillment & Logistics")
    # TODO: Add order fulfillment module UI here
    st.info("Order Fulfillment module content goes here.")

# -------- User Access Page --------
elif choice == "User Access":
    st.header("🔐 User Roles & Access Control")
    # TODO: Add user access control module UI here
    st.info("User Access module content goes here.")

# -------- Predictive Analytics Page --------
elif choice == "Predictive Analytics":
    st.header("📈 Predictive Analytics")
    # TODO: Add predictive analytics module UI here
    st.info("Predictive Analytics module content goes here.")

# -------- Alerts Page --------
elif choice == "Alerts":
    st.header("🔔 Alerts & Notifications")
    # TODO: Add alerts module UI here
    st.info("Alerts module content goes here.")

# -------- Collaboration Page --------
elif choice == "Collaboration":
    st.header("💬 Collaboration & Communication")
    # TODO: Add collaboration module UI here
    st.info("Collaboration module content goes here.")
