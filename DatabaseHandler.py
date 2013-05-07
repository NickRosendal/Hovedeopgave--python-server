'''
Created on Apr 19, 2013

@author: xxx
'''
import sqlite3
import os
class DatabaseHandler:
    
    def __init__(self, hoursBetweenlastVisit=12):
        self.hoursBetweenlastVisit = hoursBetweenlastVisit
    def openConnection(self, dataBase="guestDB.sqlite"):
        self.myConnection = sqlite3.connect(dataBase)
        self.myCursor = self.myConnection.cursor()
    def closeConnection(self):
        self.myCursor.close()
        self.myConnection.close()
        pass
    def addGuest(self, name, birthday, sex):
        self.openConnection()
        self.myCursor.execute("INSERT INTO Guest VALUES (NULL,'" + name + "','" + birthday + "','" + sex + "',NULL, NULL);"),
        self.myCursor.execute("INSERT INTO Event VALUES (datetime(), last_insert_rowid(), 'Guest Created');");
        self.myConnection.commit()
        self.myConnection.close()
    def enterGuest(self, guestId):
        self.openConnection()
        self.myCursor.execute("SELECT * FROM Event WHERE Id = '" + str(guestId) + "' AND DateTime >= datetime('now','-" +  str(self.hoursBetweenlastVisit) + " hours')")
        if len(self.myCursor.fetchall()) == 0:
            self.myCursor.execute("INSERT INTO Event VALUES (datetime(), " + str(guestId) + ", 'Entered');");
        self.myConnection.commit()
        print "DONE"    
        self.myConnection.close()    
    def addEventToGuest(self, guestId, event):
        self.openConnection()
        self.myCursor.execute("INSERT INTO Event VALUES (datetime(), " + str(guestId) + ", '" + event + "');");
        self.myConnection.commit()
        self.myConnection.close()
    def addImageToGuest(self, guestId, ImagePath):
        self.openConnection()
        self.myCursor.execute("SELECT ImagePath FROM Guest WHERE id='" + str(guestId) + "'")
        result = self.myCursor.fetchall()
        if result[0][0] != None:
            os.remove(str(result[0][0]))
        self.myCursor.execute("UPDATE Guest SET ImagePath='" + ImagePath + "' WHERE ID='" + guestId + "'")
        self.myConnection.commit()
        self.closeConnection()
    def getSingleGuest(self, name, birthday):
        self.openConnection()
        self.myCursor.execute("SELECT * FROM Guest WHERE Name = '" + name + "' AND Birthday = '" + birthday + "'")
        foundGuests = self.myCursor.fetchall()
        if len(foundGuests) == 0:
            self.closeConnection()
            return None
        elif len(foundGuests) == 1:
            returnEntry = list(foundGuests[0])
            self.myCursor.execute("SELECT DateTime, Description FROM Event WHERE Id ='" + str(returnEntry[0]) + "' ORDER BY DateTime DESC")  # New code
            returnEntry.append(self.myCursor.fetchall())
            self.closeConnection()
            return returnEntry
        self.closeConnection()
    def getGuestsForNight(self):
        self.openConnection()
        self.myCursor.execute("SELECT Guest.*  FROM Guest INNER JOIN Event ON Guest.Id = Event.Id WHERE Event.DateTime >= datetime('now','-" + str(self.hoursBetweenlastVisit) + " hours') GROUP BY Guest.Id ORDER BY  Event.DateTime DESC") 
        foundGuests = self.myCursor.fetchall()
        if len(foundGuests) == 0:
            self.closeConnection()
            return None
        else:
            returnList = []
            for guestEntry in foundGuests:
                self.myCursor.execute("SELECT DateTime, Description FROM Event WHERE Id ='" + str(guestEntry[0]) + "' ORDER BY DateTime DESC")  # New code
                returnEntry = list(guestEntry)
                returnEntry.append(self.myCursor.fetchall())
                returnList.append(returnEntry)
            self.closeConnection()
            return returnList
    def searchForGuests(self, name, sex):
        self.openConnection()
        name = name.replace(" ", "%")
        self.myCursor.execute("SELECT * FROM Guest WHERE Name LIKE '%" + name + "%' AND Sex  LIKE '%" + sex + "%'")
        foundGuests = self.myCursor.fetchall()
        if len(foundGuests) == 0:
            self.closeConnection()
            return None
        else:
            returnList = []
            for guestEntry in foundGuests:
                self.myCursor.execute("SELECT DateTime, Description FROM Event WHERE Id ='" + str(guestEntry[0]) + "' ORDER BY DateTime DESC")  # New code
                returnEntry = list(guestEntry)
                returnEntry.append(self.myCursor.fetchall())
                returnList.append(returnEntry)
            self.closeConnection()
            return returnList
    def deleteGuest(self, firstAndMiddleName, lastName, birthday):
        self.openConnection()
        self.myCursor.execute("SELECT Id, ImagePath, DocumentationImagePath FROM Guest WHERE Name LIKE '%" + firstAndMiddleName + "%" + lastName + "%' AND Birthday  LIKE '%" + birthday + "%'")
        for currentItem in self.myCursor.fetchall():
            try:
                if currentItem[1] != None:
                    os.remove(str(currentItem[1]))
                if currentItem[2] != None:
                    os.remove(str(currentItem[2]))
            except OSError as e:
                print('File error' + str(e))
            self.myCursor.execute("DELETE FROM Event WHERE Id = '" + str(currentItem[0]) + "'")
            self.myCursor.execute("DELETE FROM Guest WHERE Id = '" + str(currentItem[0]) + "'")
        self.myConnection.commit()
        self.closeConnection()
        
if __name__ == '__main__':
    myDatabaseHandler = DatabaseHandler()
    # myDatabaseHandler.openConnection()
    # myDatabaseHandler.addGuest("firstAndMiddleName", "lastName", "birthday", "F", "imagePath", None)
    print "getSingleGuest", myDatabaseHandler.getSingleGuest("KIM GRAVE LINDHARD", "1982-07-21")
    # tmpTuple = myDatabaseHandler.getSingleGuest("Anders", "Lindhard", "1982-07-21")
    # print tmpTuple
    # myDatabaseHandler.addEventToGuest(tmpTuple[0][0], "Entered")
    # for currentItem in  myDatabaseHandler.searchForGuests("i", "", ""):
    #    print currentItem
    # myDatabaseHandler.deleteGuest("kim","","")
    # myDatabaseHandler.closeConnection()
    print "searchForGuests", myDatabaseHandler.searchForGuests("kim", "M")
