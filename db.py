import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' (user_id, nickname) VALUES (?,?)", [user_id, nickname])

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM 'users' WHERE user_id = ?", [user_id]).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            # return self.cursor.execute("INSERT INTO 'users' ('nickname') VALUES (?) ", [user_id, nickname])
            return self.cursor.execute("UPDATE 'users' SET nickname = ? WHERE user_id = ?", (nickname, user_id,))

    def get_nickname(self, user_id):
        with self.connection:
            nicknames = (self.cursor.execute(
                "SELECT nickname FROM 'users' WHERE user_id = ? AND is_client = 1 ", [user_id]).fetchall())
            return nicknames

    def get_id(self, nickname):
        with self.connection:
            id_s = (self.cursor.execute(
                "SELECT user_id FROM 'users' WHERE nickname = ?", [nickname]).fetchall())
            return id_s

    def admin_status(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT is_admin FROM 'users' WHERE user_id = ?", [user_id]).fetchall()[0][0]

    def set_admin(self, user_id):
        with self.connection:
            self.cursor.execute(
                "UPDATE 'users' SET is_admin = 1 WHERE user_id = ?", [user_id])

    def moder_status(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT is_client FROM 'users' WHERE user_id = ?", [user_id]).fetchall()[0][0]

    def set_moder(self, user_id):
        with self.connection:
            self.cursor.execute(
                "UPDATE 'users' SET is_client = 1 WHERE user_id = ?", [user_id])

    def del_moder(self, user_id):
        with self.connection:
            self.cursor.execute(
                "UPDATE 'users' SET is_client = 0 WHERE user_id = ?", [user_id])

    def get_moders(self):
        with self.connection:
            moders = (self.cursor.execute(
                "SELECT user_id FROM 'users' WHERE is_client = 1").fetchall())

            return moders

    def get_moder_list(self):
        with self.connection:
            moders = (self.cursor.execute("SELECT user_id, nickname FROM 'users' WHERE is_client = 1").fetchall())

        return moders

    def set_messageuper(self, user_id, upper_message):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET upper_text = ? WHERE user_id = ?", (upper_message, user_id,))

    def set_messagemiddle(self, user_id, middle_message):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET middle_text = ? WHERE user_id = ?",
                                       (middle_message, user_id,))

    def set_messagebottom(self, user_id, bottom_message):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET bottom_text = ? WHERE user_id = ?",
                                       (bottom_message, user_id,))

    def get_messagepost(self, user_id):
        with self.connection:
            temp = self.cursor.execute(
                "SELECT upper_text,  middle_text,  bottom_text FROM 'users' WHERE user_id = ? ", [user_id]).fetchall()[
                0]

            return '\n'.join(temp)

    def get_active_user_id(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users WHERE is_active = 1").fetchall()

    def add_chanel_list(self, chanels_id, user_id):
        with self.connection:
            self.cursor.execute("INSERT OR IGNORE INTO Channels (channel_id, user_id) VALUES (?,?)",
                                [chanels_id, user_id])
            # return self.cursor.execute("INSERT INTO 'users' (chanels, user_id) VALUES (?, ?)", [chanels_id, user_id])

    def add_private_channel(self, channels_id, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET private_chat = ? WHERE user_id = ?", [channels_id, user_id])

    # def del_chanel_list(self):
    #     with self.connection:
    #         print('rabotaet')
    #         return self.cursor.execute("UPDATE 'users' SET chanels = NULL WHERE admin_id = 1")
    #         # return self.cursor.execute("INSERT INTO 'users' (chanels, user_id) VALUES (?, ?)", [chanels_id, user_id])

    def del_user_channels(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM 'Channels' WHERE user_id = ?", [user_id])

    def del_all_channels(self):
        with self.connection:
            self.cursor.execute("DELETE FROM 'Channels'")

    def del_current_channel(self, channel_id):
        with self.connection:
            self.cursor.execute("DELETE FROM 'Channels' WHERE channel_id = ?", [channel_id])

    def set_chanel_nickname(self, chanel_name, chanel_id):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET chanel_name = ? WHERE chanels = ?",
                                       [chanel_name, chanel_id, ])

    def get_chanel_list(self, user_id):
        with self.connection:
            temp = (self.cursor.execute(
                "SELECT channel_id FROM 'Channels' WHERE user_id = ?", [user_id]).fetchall())
            return temp

    def get_all_channels(self):
        with self.connection:
            return self.cursor.execute("SELECT channel_id FROM 'Channels'").fetchall()

    def get_all_user_channels(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT channel_id FROM 'Channels' WHERE user_id = ?", [user_id]).fetchall()

    def get_status_malling(self):
        with self.connection:
            return self.cursor.execute("SELECT is_active FROM 'users' WHERE is_admin = 1").fetchall()[0][0]

    def set_status_malling_1(self):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET is_active = 1 WHERE is_admin = 1")

    def set_status_malling_0(self):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET is_active = 0 WHERE is_admin = 1")

    def set_message_chat_id(self, message_id, chat_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'deleting' (message_id, chat_id) VALUES (?,?)",
                                       [message_id, chat_id])

    def get_message_id(self):
        with self.connection:
            return self.cursor.execute("SELECT message_id FROM 'deleting'").fetchall()

    def get_chat_id(self, message_id):
        with self.connection:
            return self.cursor.execute("SELECT chat_id FROM 'deleting' WHERE message_id = ?", [message_id]).fetchall()

    def clean_db(self, ):
        with self.connection:
            return self.cursor.execute("DELETE FROM deleting")

    def get_msg_and_chat_id(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'deleting'").fetchall()

    def set_url(self, user_id, url):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET url = ? WHERE user_id = ?", [url, user_id])

    def get_url(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT url FROM 'users' WHERE user_id = ?", [user_id]).fetchall()[0][0]

    def set_type_malling_db(self, type_malling, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET type = ? WHERE user_id = ?", [type_malling, user_id])

    def get_type_malling_db(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT type FROM 'users' WHERE user_id = ?", [user_id]).fetchall()[0][0]
