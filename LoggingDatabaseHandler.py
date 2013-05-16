import sqlite3
class LoggingDatabaseHandler:
    def openConnection(self, dataBase="logDB.sqlite"):
        self.myConnection = sqlite3.connect(dataBase)
        self.myCursor = self.myConnection.cursor()
    def closeConnection(self):
        self.myCursor.close()
        self.myConnection.close()    
    def validataUsernamePassword(self, username, password):
        self.openConnection()
        self.myCursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
        if len(self.myCursor.fetchall()) > 0:
            result = True
        else:
            result = False
        self.closeConnection()
        return result
    def getUsernames(self):
        self.openConnection()
        self.myCursor.execute("SELECT username FROM users")
        result = self.myCursor.fetchall()
        self.closeConnection()
        return result
    def addEvent(self, description, username, password):
        print "Dec,user,pass", description, username, password
        self.openConnection()
        self.myCursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
        if len(self.myCursor.fetchall()) > 0:
            result = True
            self.myCursor.execute("INSERT INTO events VALUES (datetime(), '" + username + "', '" + description + "')")
            self.myConnection.commit()
        else:
            result = False
        return result    
        self.closeConnection()
if __name__ == '__main__':
    myLoggingDatabaseHandler = LoggingDatabaseHandler()
    print myLoggingDatabaseHandler.getUsernames()
    for currentUsername in myLoggingDatabaseHandler.getUsernames():
        print currentUsername[0]
    print "sendGuestInfo:id:#"[0:17]