from datetime import datetime

class AlertsNotifications:
    def __init__(self):
        # Store user alert preferences (email, sms, in-app)
        self.user_alert_prefs = {}  # user_id -> {'email': True, 'sms': False, 'in_app': True}
        self.alert_log = []  # Store alerts sent

    def set_user_prefs(self, user_id, email=True, sms=False, in_app=True):
        self.user_alert_prefs[user_id] = {
            "email": email,
            "sms": sms,
            "in_app": in_app
        }

    def send_alert(self, user_id, alert_type, message):
        prefs = self.user_alert_prefs.get(user_id, {"email": True, "sms": False, "in_app": True})
        timestamp = datetime.now()
        alerts_sent = []

        if prefs.get("email"):
            alerts_sent.append("email")
            # Simulate email sending with print
            print(f"[EMAIL] To: {user_id} | Type: {alert_type} | Message: {message}")

        if prefs.get("sms"):
            alerts_sent.append("sms")
            # Simulate SMS sending
            print(f"[SMS] To: {user_id} | Type: {alert_type} | Message: {message}")

        if prefs.get("in_app"):
            alerts_sent.append("in_app")
            # Simulate in-app alert logging
            print(f"[IN-APP] To: {user_id} | Type: {alert_type} | Message: {message}")

        self.alert_log.append({
            "timestamp": timestamp,
            "user_id": user_id,
            "alert_type": alert_type,
            "message": message,
            "methods": alerts_sent
        })

    def get_alert_log(self):
        return self.alert_log
