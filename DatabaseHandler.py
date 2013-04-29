'''
Created on Apr 19, 2013

@author: xxx
'''
import sqlite3
import os
class DatabaseHandler:
    def __init__(self, dataBase="guestDB.sqlite"):
    #    self.openConnection()
        pass
    def openConnection(self, dataBase="guestDB.sqlite"):
        self.myConnection = sqlite3.connect(dataBase)
        self.myCursor = self.myConnection.cursor()
    def closeConnection(self):
        self.myCursor.close()
        self.myConnection.close()
        pass
    def addGuest(self,firstAndMiddleName,lastName,birthday,sex,zipCode):
        self.openConnection()
        self.myCursor.execute("INSERT INTO Guest VALUES (NULL,'" + firstAndMiddleName + "','" + lastName +"','" +birthday +"','"+ sex +"','"+ zipCode + "',NULL, NULL);"),
        self.myCursor.execute("INSERT INTO Event VALUES (datetime(), last_insert_rowid(), 'Guest Created');");
        self.myConnection.commit()
        self.myConnection.close()
    def addEventToGuest(self, guestId, event):
        self.myCursor.execute("INSERT INTO Event VALUES (datetime(), " + str(guestId) + ", '"+ event + "');");
        self.myConnection.commit()
    def addImageToGuest(self,guestId,ImagePath):
        self.openConnection()
        self.myCursor.execute("SELECT ImagePath FROM Guest WHERE id='" +str(guestId) + "'")
        result = self.myCursor.fetchall()
        print result
        if result[0][0] != None:
            os.remove(str(result[0][0]))
        self.myCursor.execute("UPDATE Guest SET ImagePath='" + ImagePath + "' WHERE ID='" + guestId +"'")
        self.myConnection.commit()
        self.closeConnection()
    def getSingleGuest(self, firstAndMiddleName, lastName, birthday):
        self.openConnection()
        self.myCursor.execute("SELECT * FROM Guest WHERE FirstAndMiddleName = '" + firstAndMiddleName + "' AND LastName = '" + lastName + "' AND Birthday = '" + birthday +"'")
        foundGuests = self.myCursor.fetchall()
        if len(foundGuests) == 0:
            self.closeConnection()
            return None
        elif len(foundGuests) == 1:
            self.myCursor.execute("SELECT DateTime, Description FROM Event WHERE Id ='" + str(foundGuests[0][0]) + "'")
            foundGuests.append(self.myCursor.fetchall())
            self.closeConnection()
            return foundGuests
        self.closeConnection()
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
    for currentItem in  myDatabaseHandler.searchForGuests("i", "", ""):
        print currentItem
    myDatabaseHandler.closeConnection()
