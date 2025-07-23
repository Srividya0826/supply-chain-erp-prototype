from modules.access_control import AccessControl

ac = AccessControl()

# Add users
print("Add admin:", ac.add_user("user1", "admin"))
print("Add buyer:", ac.add_user("user2", "buyer"))
print("Add finance:", ac.add_user("user3", "finance"))

# Check permissions
print("user1 can approve?", ac.check_permission("user1", "approve"))
print("user2 can approve?", ac.check_permission("user2", "approve"))

# Log action
ac.log_action("user2", "create_po", "PO1001 created")

# Get audit log
for entry in ac.get_audit_log():
    print(entry)
