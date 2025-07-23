from modules.alerts_notifications import AlertsNotifications

an = AlertsNotifications()

# Setup user alert preferences
an.set_user_prefs("user1", email=True, sms=True, in_app=False)
an.set_user_prefs("user2", email=False, sms=False, in_app=True)

# Send alerts
an.send_alert("user1", "Order Status", "Your order PO1001 has been shipped.")
an.send_alert("user2", "Stock Alert", "Inventory for item I001 is below reorder point.")

# View alert log
for alert in an.get_alert_log():
    print(alert)
