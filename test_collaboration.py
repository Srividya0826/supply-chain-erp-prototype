from modules.collaboration import Collaboration

col = Collaboration()

# Test Comments
print("Add comment on PO1001:", col.add_comment("PO1001", "user1", "Please expedite this order."))
print("Add another comment:", col.add_comment("PO1001", "user2", "Noted, will check with supplier."))
print("Comments on PO1001:", col.get_comments("PO1001"))

# Test Tasks
print("Create task T001:", col.create_task("T001", "user3", "Review supplier contract"))
print("Create duplicate task T001:", col.create_task("T001", "user3", "Duplicate task"))
print("Update task status T001:", col.update_task_status("T001", "In Progress"))
print("Task details T001:", col.get_task("T001"))
print("Tasks assigned to user3:", col.list_tasks_for_user("user3"))

# Test Messaging
print("Send message in convo C001:", col.send_message("C001", "user1", "Hi, when will the shipment arrive?"))
print("Send message in convo C001:", col.send_message("C001", "user2", "Expected delivery is tomorrow."))
print("Messages in convo C001:", col.get_messages("C001"))
