import threading

from CommandServer import CommandServer
from CameraStreamHttpServer import CameraCaptureServer
from MagtekUsbCardReader import MagtekUsbCardReader
from DatabaseHandler import DatabaseHandler
import HealthInsuranceCardInterpreter
import re
from FileServer import FileServer
class MainServer():
    def __init__(self):
        self.myCommandServer = CommandServer()
        self.myCommandServer.registerObserver(self)
        self.myCommandServer.start()
        
        self.myMagtekUsbCardReader = MagtekUsbCardReader()
        self.myMagtekUsbCardReader.registerObserver(self)
        self.myMagtekUsbCardReader.start()
        
        self.myCameraCaptureServer = CameraCaptureServer()
        self.myCameraCaptureServer.start()
        
        self.myDatabaseHandler = DatabaseHandler()
        
        self.myFileServer = FileServer()
        self.myFileServer.registerObserver(self)
        
        print "All modules have been asked to start"

    def notify(self, subjectName,eventType, message):
        if eventType =="status":
            print subjectName, "status", message
        if subjectName == "CommandServer" and eventType =="status" and message == "Closing connection":
            self.myFileServer.closeConnection()
        if subjectName == "CommandServer" and eventType =="message":
            self.handleTcpMessages(message)
        elif subjectName == "FileServer" and eventType =="status":
            if message[0:20] == "Ready to serve file:":
                self.myCommandServer.sendMessage("Image from disk is ready:" + message[20:])   
        elif subjectName == "CardReader" and eventType =="swipe":
            self.handleSwipe(HealthInsuranceCardInterpreter.Interpitate(message))
       
    def handleTcpMessages(self, message):
        print "CommandServer have recived message:", message
        if message == "pending":
            self.myCommandServer.sendMessage("connection accepted")
            
        elif message == "start video server":
            self.myCameraCaptureServer.showVideo()
            self.myCommandServer.sendMessage("video server is ready")
            
        elif message[0:17] == "take picture for ":
            filePath = self.myCameraCaptureServer.takePicture("Images")
            self.myDatabaseHandler.addImageToGuest(message[17:], filePath)
            self.myFileServer.serveFile(filePath)
        elif message[0:7] == "search:":
            name = re.search(r"name:(.*?)#", message[7:]).group(1)
            sex = re.search(r"sex:(.*?)#", message[7:]).group(1)
            searchResult = self.myDatabaseHandler.searchForGuests(name, sex)
            commandString = "searchResult:"
            if searchResult:
                for guestEntry in searchResult:
                    commandString += self.createGuestInfoCommandString(guestEntry)
            commandString += "#"
            self.myCommandServer.sendMessage(commandString)
    
        elif message[0:23] == "send picture from disk:":
            self.myFileServer.serveFile(message[23:len(message) - 1])
        elif message == "give me the night list":
            guestsForNight = self.myDatabaseHandler.getGuestsForNight()
            commandString = "guestsForNight:"
            if guestsForNight:
                for guestEntry in guestsForNight:
                    commandString += self.createGuestInfoCommandString(guestEntry)
            commandString += "#"
            print commandString
            self.myCommandServer.sendMessage(commandString)
    def handleSwipe(self, cardInfo):
        guestFromDataBase = self.myDatabaseHandler.getSingleGuest(str(cardInfo[0]), str(cardInfo[1]))
        if not guestFromDataBase:
            self.myDatabaseHandler.addGuest(str(cardInfo[0]), str(cardInfo[1]), str(cardInfo[2]))
            guestFromDataBase = self.myDatabaseHandler.getSingleGuest(str(cardInfo[0]), str(cardInfo[1]))
        else:
            self.myDatabaseHandler.enterGuest(guestFromDataBase[0])
        commandString = self.createGuestInfoCommandString(guestFromDataBase)
        print commandString
        self.myCommandServer.sendMessage(commandString)
            
    def createGuestInfoCommandString(self, informationList):
        if informationList == None:
            return
        returnString  = "guestInfo:name:" + str(informationList[1]) +"#"
        returnString += " birthday:" + str(informationList[2]) + "#"
        returnString += " sex:" + str(informationList[3]) + "#"
        returnString += " guestId:" + str(informationList[0]) + "#"
        returnString += " Image:" + str(informationList[4]) + "# DocumentationImage:" + str(informationList[5]) + "#"
        returnString += " Events:"
        for eventItem in informationList[6]:
            returnString += "Event:dateTime:" + eventItem[0] + "#Description:" + eventItem[1] + "##"
        returnString += "##"
        return returnString 
if __name__ == '__main__':
    
    myMainServer = MainServer()  # starts the class 
    #print "test", myMainServer.handleTcpMessages("giveMeNIght")
    while True:
        command = raw_input('Write stop to exit\n')
        print command
        if command == "stop":
            myMainServer.myCameraCaptureServer.stopCamera()
            myMainServer.myCommandServer.stop()
            myMainServer.myFileServer.stop()
            print "stopped"
            break;
        elif command[0:4] == "del ":
            print "Will delete '"+ command[4:]+ "' from Database"
            myMainServer.myDatabaseHandler.deleteGuest(command[4:], "", "")
        else:
            print "Error unknown command"
        