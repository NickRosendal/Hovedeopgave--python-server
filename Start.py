import threading

from CommandServer import CommandServer
from CameraStreamHttpServer import CameraCaptureServer
from MagtekUsbCardReader import MagtekUsbCardReader
from DatabaseHandler import DatabaseHandler
import HealthInsuranceCardInterpreter
from FileServer import FileServer
class ObserverbleTest():
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
            print message
            self.myCommandServer.sendMessage("image is ready")      
        elif subjectName == "CardReader" and eventType =="swipe":
            cardList = HealthInsuranceCardInterpreter.Interpitate(message)
            print cardList
            guestFromDataBase = self.myDatabaseHandler.getSingleGuest(str(cardList[0]), str(cardList[1]), str(cardList[3]))
            if guestFromDataBase:
                print guestFromDataBase
                commandString  = "guestInfo:name:" + str(guestFromDataBase[0][1]) + " " + str(guestFromDataBase[0][2]) +"#"
                commandString += " birthday:" + str(guestFromDataBase[0][3]) + "#"
                commandString += " sex:" + str(guestFromDataBase[0][4]) + "#"
                commandString += " zipcode:" + str(guestFromDataBase[0][5]) + "#"
                commandString += " id:" + str(guestFromDataBase[0][0]) + "#"
                commandString += " Events:"
                for eventItem in guestFromDataBase[1]:
                    commandString += "Event:dateTime:" + eventItem[0] + "#Description:" + eventItem[1] + "#"
                #commandString += "#Image:" + ImageToString.getImage() + "#DocumentationImage"
                #commandString += "#Image:herERDENSA#DocumentationImage"
                commandString += "##"
            else:
                commandString  = "guestInfo:name:" + str(cardList[0]) + " " + str(cardList[1]) + "#"
                commandString += " birthday:" + str(cardList[3]) + "#"
                commandString += " sex:" + str(cardList[4]) + "#"
                commandString += " zipcode:" + str(cardList[2]) + "#"
                commandString += " Events:##"
            
            #print commandString
            self.myCommandServer.sendMessage(commandString)
       
    def handleTcpMessages(self, message):
        print "CommandServer have recived message:", message
        if message == "pending":
            self.myCommandServer.sendMessage("connection accepted")
        elif message == "start video server":
            self.myCameraCaptureServer.showVideo()
            self.myCommandServer.sendMessage("video server is ready")
        elif message == "take picture":
            filePath = self.myCameraCaptureServer.takePicture("path")
        #    thread = threading.Thread(target=self.myFileServer.serveFile, args=(str(filePath)))
        #    thread.start()
        elif message == "pretendToSwipe":
            self.myCommandServer.sendMessage("guestInfo:name:SIGNE JOHANSEN# birthday:1986-12-23# zipcode:3500# sex:Female# status:welcomed# lastVisit:NA##")
            
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

    myObserverbleTest = ObserverbleTest()  # starts the class 
    while True:
        command = raw_input('Write stop to exit\n')
        if command == "stop":
            myObserverbleTest.myCameraCaptureServer.stopCamera()
            myObserverbleTest.myCommandServer.stop()
            print "stopped"
            break;
        print command