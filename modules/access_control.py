from datetime import datetime

class AccessControl:
    def __init__(self):
        # user_id -> role mapping
        self.users = {}  # e.g. {"user1": "admin", "user2": "buyer"}
        # role permissions mapping
        self.role_permissions = {
            "admin": ["create", "read", "update", "delete", "approve"],
            "buyer": ["create", "read", "update"],
            "finance": ["read", "approve", "pay"],
            "supplier": ["read", "update_status"],
            "warehouse": ["read", "update_stock"],
        }
        self.audit_log = []  # list of tuples (timestamp, user, action, details)

    def add_user(self, user_id, role):
        if user_id in self.users:
            return False
        if role not in self.role_permissions:
            return False
        self.users[user_id] = role
        self.audit_log.append((datetime.now(), user_id, "add_user", f"Role: {role}"))
        return True

    def remove_user(self, user_id):
        if user_id not in self.users:
            return False
        role = self.users.pop(user_id)
        self.audit_log.append((datetime.now(), user_id, "remove_user", f"Role: {role}"))
        return True

    def check_permission(self, user_id, permission):
        role = self.users.get(user_id)
        if not role:
            return False
        allowed = permission in self.role_permissions.get(role, [])
        self.audit_log.append((datetime.now(), user_id, "check_permission", f"Permission: {permission}, Allowed: {allowed}"))
        return allowed

    def log_action(self, user_id, action, details=""):
        self.audit_log.append((datetime.now(), user_id, action, details))

    def get_audit_log(self):
        return self.audit_log

    # Add this method to fix your error
    def get_all_users(self):
        # Return list of dicts with user info for better display in app
        return [{"user_id": user_id, "role": role} for user_id, role in self.users.items()]
