import StringIO
import Image

def getImage():
    image = Image.open("testImage.jpeg")
    
    output = StringIO.StringIO()
    image.save(output, format="JPEG")
    resultThingy = ""
    for c in output.getvalue():
        if ord(c) < 10:
            resultThingy += "0"
        if ord(c) < 100:
            resultThingy += "0"
        resultThingy += str(ord(c))
         
    #''.join(str(ord(c)) for c in s)
    #contents = ''.join(str(ord(resultThingy)) resultThingy)
    output.close()
    print resultThingy
    return resultThingy

#if __name__ == '__main__':
getImage()