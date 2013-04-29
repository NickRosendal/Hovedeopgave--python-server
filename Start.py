import threading

from CommandServer import CommandServer
from CameraStreamHttpServer import CameraCaptureServer
from MagtekUsbCardReader import MagtekUsbCardReader
from DatabaseHandler import DatabaseHandler
import HealthInsuranceCardInterpreter
from FileServer import FileServer
class MainServer():
    FILEPATH = "/home/xxx/Eclipse Workspace/PyBarEntrySystemServer/GuestImages/"
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
        elif message == "take picture":
            filePath = self.myCameraCaptureServer.takePicture("Images")
            # tell the db about the file and maybe delete a old file
            #self.myFileServer.serveFile(filePath)
            print "good show"
        elif message[0:23] == "send picture from disk:":
            self.myFileServer.serveFile(MainServer.FILEPATH + message[23:len(message) - 1])
   
    
    def handleSwipe(self, cardList):
        guestFromDataBase = self.myDatabaseHandler.getSingleGuest(str(cardList[0]), str(cardList[1]), str(cardList[3]))
        if guestFromDataBase:
            print guestFromDataBase
            commandString  = "guestInfo:name:" + str(guestFromDataBase[0][1]) + " " + str(guestFromDataBase[0][2]) +"#"
            commandString += " birthday:" + str(guestFromDataBase[0][3]) + "#"
            commandString += " sex:" + str(guestFromDataBase[0][4]) + "#"
            commandString += " zipcode:" + str(guestFromDataBase[0][5]) + "#"
            commandString += " id:" + str(guestFromDataBase[0][0]) + "#"
            commandString += "Image:" + str(guestFromDataBase[0][6]) + "#DocumentationImage:" + str(guestFromDataBase[0][6]) + "#"
            commandString += " Events:"
            for eventItem in guestFromDataBase[1]:
                commandString += "Event:dateTime:" + eventItem[0] + "#Description:" + eventItem[1] + "#"
            commandString += "##"
        else:
            commandString  = "guestInfo:name:" + str(cardList[0]) + " " + str(cardList[1]) + "#"
            commandString += " birthday:" + str(cardList[3]) + "#"
            commandString += " sex:" + str(cardList[4]) + "#"
            commandString += " zipcode:" + str(cardList[2]) + "#"
            commandString += " Events:##"
        
        print commandString
        self.myCommandServer.sendMessage(commandString)
            
    def createCommandString(self, cardInfo):
        if cardInfo == None:
            return
        returnString  = "guestInfo:name:" + str(cardInfo[0]) + " " + str(cardInfo[1]) + "#"
        returnString += " birthday:" + str(cardInfo[3]) + "#"
        returnString += " sex:" + str(cardInfo[4]) + "#"
        returnString += " zipcode:" + str(cardInfo[2]) + "#"
        returnString += "#"
        print returnString
        return returnString 
if __name__ == '__main__':

    myMainServer = MainServer()  # starts the class 
    while True:
        command = raw_input('Write stop to exit\n')
        if command == "stop":
            myMainServer.myCameraCaptureServer.stopCamera()
            myMainServer.myCommandServer.stop()
            myMainServer.myFileServer.stop()
            print "stopped"
            break;
        print command