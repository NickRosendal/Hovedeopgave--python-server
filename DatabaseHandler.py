'''
Created on Apr 19, 2013

@author: xxx
'''
import sqlite3

class DatabaseHandler:
    def __init__(self, dataBase="guestDB.sqlite"):
        pass
    def openConnection(self, dataBase="guestDB.sqlite"):
        self.myConnection = sqlite3.connect(dataBase)
        self.myCursor = self.myConnection.cursor()
    def closeConnection(self):
        self.myCursor.close()
        self.myConnection.close()
    def addGuest(self,firstAndMiddleName,lastName,birthday,sex,imagePath,documentationImagePath):
        if documentationImagePath == None: documentationImagePath = "NULL"
        self.myCursor.execute("INSERT INTO Guest VALUES (NULL,'" + firstAndMiddleName + "','" + lastName +"','" +birthday +"','"+ sex +"','"+imagePath+ "', "+ documentationImagePath +");"),
        self.myCursor.execute(" INSERT INTO Event VALUES (datetime(), last_insert_rowid(), 'Guest Created');");
        self.myConnection.commit()
    def addEventToGuest(self, guestId, event):
        self.myCursor.execute(" INSERT INTO Event VALUES (datetime(), " + str(guestId) + ", '"+ event + "');");
        self.myConnection.commit()
    def getSingleGuest(self, firstAndMiddleName, lastName, birthday):
        self.myCursor.execute("SELECT * FROM Guest WHERE FirstAndMiddleName = '" + firstAndMiddleName + "' AND LastName = '" + lastName + "' AND Birthday = '" + birthday +"'")
        foundGuests = self.myCursor.fetchall()
        if len(foundGuests) == 0:
            return None
        elif len(foundGuests) == 1:
            self.myCursor.execute("SELECT * FROM Event WHERE Id ='" + str(foundGuests[0][0]) + "'")
            foundGuests.append(self.myCursor.fetchall())
            return foundGuests
    def searchForGuests(self, firstAndMiddleName, lastName, birthday):
        self.myCursor.execute("SELECT * FROM Guest WHERE FirstAndMiddleName LIKE '%" + firstAndMiddleName + "%' AND LastName  LIKE '%" + lastName + "%' AND Birthday  LIKE '%" + birthday + "%'")
        return self.myCursor.fetchall()
        
if __name__ == '__main__':
    myDatabaseHandler = DatabaseHandler()
    myDatabaseHandler.openConnection()
    #myDatabaseHandler.addGuest("firstAndMiddleName", "lastName", "birthday", "F", "imagePath", None)
    #myDatabaseHandler.getSingleGuest("And1ers", "Lindhard")
    #tmpTuple = myDatabaseHandler.getSingleGuest("Anders", "Lindhard", "1982-07-21")
    #print tmpTuple
    #myDatabaseHandler.addEventToGuest(tmpTuple[0][0], "Entered")
    #for currentItem in  myDatabaseHandler.searchForGuests("i", "", ""):
    #    print currentItem
    myDatabaseHandler.closeConnection()
