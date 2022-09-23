import sqlite3

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread = False)
        self.cursor = self.connection.cursor()
    
    def add_queue(self, message.chat.id, gender): # Добавление новой очереди
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`message.chat.id`, `gender`) VALUES (?,?)", (message.chat.id, gender))
    
    def delete_queue(self, message.chat.id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE `message.chat.id` = ?", (message.chat.id,))
    
    def delete_chat(self, id_chat):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE `id` = ?", (id_chat,))

    def set_gender(self, message.chat.id, gender):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM `users` WHERE `message.chat.id` = ?", (message.chat.id,)).fetchmany(1)
            if bool(len(user)) == False:
                self.cursor.execute("INSERT INTO `users` (`message.chat.id`, `gender`) VALUES (?,?)", (message.chat.id, gender))
                return True
            else:
                return False

    def get_gender(self, message.chat.id):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM `users` WHERE `message.chat.id` = ?", (message.chat.id,)).fetchmany(1)
            if bool(len(user)):
                for row in user:
                    return row[2]
            else:
                return False
    
    def get_gender_chat(self, gender):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue` WHERE `gender` = ?", (gender,)).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    user_info = [row[1], row[2]]
                    return user_info
            else:
                return [0]

    def get_chat(self):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue`", ()).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    user_info = [row[1], row[2]]
                    return user_info
            else:
                return [0]

    def create_chat(self, chat_one, chat_two):
        with self.connection:
            if chat_two != 0:
                # Создание чата
                self.cursor.execute("DELETE FROM `queue` WHERE `message.chat.id` = ?", (chat_two,))
                self.cursor.execute("INSERT INTO `chats` (`chat_one`, `chat_two`) VALUES (?,?)", (chat_one, chat_two,))
                return True

            else:
                # Становимся в очередь
                return False
    
    def get_active_chat(self, message.chat.id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_one` = ?", (message.chat.id,))
            id_chat = 0
            for row in chat:
                id_chat = row[0]
                chat_info = [row[0], row[2]]
            
            if id_chat == 0:
                chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_two` = ?", (message.chat.id,))
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0], row[1]]
                if id_chat == 0:
                    return False
                else:
                    return chat_info
            else:
                return chat_info
