from datetime import datetime

class Collaboration:
    def __init__(self):
        self.comments = {}  # key: entity_id (like PO id), value: list of comments
        self.tasks = {}     # key: task_id, value: task dict
        self.messages = {}  # key: conversation_id, value: list of messages

    # Comments
    def add_comment(self, entity_id, user_id, comment_text):
        comment = {
            "user_id": user_id,
            "comment": comment_text,
            "timestamp": datetime.now()
        }
        if entity_id not in self.comments:
            self.comments[entity_id] = []
        self.comments[entity_id].append(comment)
        return True

    def get_comments(self, entity_id):
        return self.comments.get(entity_id, [])

    # Tasks
    def create_task(self, task_id, assigned_to, description, status="To Do"):
        if task_id in self.tasks:
            return False
        self.tasks[task_id] = {
            "assigned_to": assigned_to,
            "description": description,
            "status": status,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        return True

    def update_task_status(self, task_id, new_status):
        if task_id not in self.tasks:
            return False
        self.tasks[task_id]["status"] = new_status
        self.tasks[task_id]["updated_at"] = datetime.now()
        return True

    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def list_tasks_for_user(self, user_id):
        return [task for task in self.tasks.values() if task["assigned_to"] == user_id]

    # Messaging
    def send_message(self, conversation_id, sender_id, message_text):
        message = {
            "sender_id": sender_id,
            "message": message_text,
            "timestamp": datetime.now()
        }
        if conversation_id not in self.messages:
            self.messages[conversation_id] = []
        self.messages[conversation_id].append(message)
        return True

    def get_messages(self, conversation_id):
        return self.messages.get(conversation_id, [])
