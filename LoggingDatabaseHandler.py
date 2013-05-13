import sqlite3
class LoggingDatabaseHandler:
    def openConnection(self, dataBase="logDB.sqlite"):
        self.myConnection = sqlite3.connect(dataBase)
        self.myCursor = self.myConnection.cursor()
    def closeConnection(self):
        self.myCursor.close()
        self.myConnection.close()    
    def validataUsernamePassword(self, username, password):
        return True
    def getUsernames(self):
        self.openConnection()
        self.myCursor.execute("SELECT username FROM users")
        result = self.myCursor.fetchall()
        self.closeConnection()
        return result
if __name__ == '__main__':
    myLoggingDatabaseHandler = LoggingDatabaseHandler()
    print myLoggingDatabaseHandler.getUsernames()
    for currentUsername in myLoggingDatabaseHandler.getUsernames():
        print currentUsername[0]
    print "sendGuestInfo:id:#"[0:17]