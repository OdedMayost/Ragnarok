import sqlite3


class DataBase:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def get_by_value(self, table, column, value):
        try:
            data = self.cursor.execute("""
                    SELECT * FROM %s
                    WHERE %s = %s;""" % (table, column, value))
            return data.fetchall()
        except:
            return 0

    def update(self, table, column_set, value_set, column, value):
        try:
            self.cursor.execute("""
                    UPDATE %s
                    SET %s = %s
                    WHERE %s = %s
                    ;""" % (table, column_set, value_set, column, value))
            self.conn.commit()
        except:
            return 0

    def add_computer(self, ip):
        try:
            computer = self.get_by_value("Computers", "IP", "'%s'" % ip)
            if not computer:
                computer_id = self.cursor.execute("SELECT MAX(ComputerID) FROM Computers;").fetchone()[0]
                computer_id = 1 if computer_id is None else computer_id + 1
                self.cursor.execute("""INSERT INTO Computers (ComputerID, IP) VALUES (%s, '%s');"""
                                    % (computer_id, ip))
                self.conn.commit()
                return computer_id
            else:
                return computer[0][0]
        except:
            return 0

    def add_user(self, ip, username, password, name, phone_number):
        try:
            user = self.get_by_value("Users", "Username", "'%s'" % username)
            if not user:
                user_id = self.cursor.execute("SELECT MAX(UserID) FROM Users;").fetchone()[0]
                user_id = 1 if user_id is None else user_id + 1
                self.cursor.execute("""INSERT INTO Users (UserID, IP, Username, Password, Name, Phone, AmountGames,
                                AmountWins, AmountLosses) VALUES (%s, '%s', '%s', '%s', '%s', '%s', %s, %s, %s);"""
                                    % (user_id, ip, username, password, name, phone_number, 0, 0, 0))
                self.conn.commit()
                return user_id
            else:
                return user[0][0]
        except:
            return 0

    def user_login(self, username, password, ip):
        try:
            data = self.cursor.execute("""
                            SELECT * FROM Users
                            WHERE Username = '%s' and Password = '%s';""" % (username, password)).fetchall()
            if data:
                user_id = data[0][0]
                self.update("Users", "IP", "'%s'" % ip, "UserID", user_id)
                return user_id
            else:
                return 0
        except:
            return 0

    def update_number_games(self, user_id):
        try:
            data = self.get_by_value("Users", "UserID", str(user_id))
            if data:
                amount_games = int(data[0][6]) + 1
                self.update("Users", "AmountGames", "'%s'" % str(amount_games), "UserID", user_id)
                return amount_games
            else:
                return 0
        except:
            return 0

    def update_number_wins(self, user_id):
        try:
            data = self.get_by_value("Users", "UserID", str(user_id))
            if data:
                amount_wins = int(data[0][7]) + 1
                self.update("Users", "AmountWins", "'%s'" % str(amount_wins), "UserID", user_id)
                return amount_wins
            else:
                return 0
        except:
            return 0

    def update_number_losses(self, user_id):
        try:
            data = self.get_by_value("Users", "UserID", str(user_id))
            if data:
                amount_losses = int(data[0][8]) + 1
                self.update("Users", "AmountLosses", "'%s'" % str(amount_losses), "UserID", user_id)
                return amount_losses
            else:
                return 0
        except:
            return 0

