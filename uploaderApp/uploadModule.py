# tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
# requests
import requests
import os

# global
url = 'https://x4d1kgdj83.execute-api.us-east-1.amazonaws.com/default/upload'
files = []

def uploadFiles(identityToken):
    
    def info(massage):
        showinfo(
            title = 'result',
            message = massage
        )
    
    def clearFiles():
        for f in files:
            fileIn = open(f, mode="rt")
            data = fileIn.read()
            data  = data.replace("\nFLAGSEPARATORCODE","")
            fileIn.close()
            fileOut = open(f, mode="wt")
            fileOut.write(data)
            fileOut.close()
        files.clear()
        labelFileName.configure(text="")
    
    def selectFile():
        filepath = filedialog.askopenfilename()
        if(filepath != ''):
            files.append(filepath)
            labelFileName.configure(text=labelFileName.cget("text") + os.path.basename(filepath) + "\n")
            generateFileSeparator(filepath)

    def generateFileSeparator(filePath):
        f = open(filePath, mode="a")
        f.write("\nFLAGSEPARATORCODE")
        f.close()

    def generateFileHeader():
        header = {
            'accept':'application/json', 
            'Authorization':identityToken,
            'fileNumber':str(len(files))
        }
        i = 0
        for f in files:
            tuple = {"filename-"+str(i) : os.path.basename(f)}
            i += 1
            header.update(tuple)
        return header

    def generateFileDict():
        fileDict = {}
        i = 0
        for f in files:
            tuple = {'file'+str(i) : open(f, 'rb')}
            i += 1
            fileDict.update(tuple)
        return fileDict

    # sending 
    def sendPost():
        if(len(files) > 0):
            fileHeaders = generateFileHeader()
            fileDict = generateFileDict()
            r = requests.post(url, files=fileDict, headers=fileHeaders)
            info(r.content)
            clearFiles()

    # root window
    root = Tk()
    photo = PhotoImage(file="img/icon.png")
    root.iconphoto(False, photo)
    root.title('http post request')
    root.geometry('500x300')
    root.resizable(False, False)
    frame= Frame(root)
    frame.pack(fill = BOTH, expand = True, padx = 10, pady = 20)
    
    # button to select file
    buttonAddFile = ttk.Button(
        frame,
        text='select file',
        command=selectFile
    )
    buttonAddFile.pack(
        pady=5,
        ipadx=5,
        ipady=5,
        side='top'
    )
    # label that changes with the file name selected
    labelFileName = ttk.Label(
        frame,
        text=""
    )
    labelFileName.pack(
        pady=5,
        ipadx=5,
        ipady=5,
        side='top'
    )
    # button to send post request
    buttonSend = ttk.Button(
        frame,
        text='Send POST',
        command=sendPost
    )
    buttonSend.pack(
        ipadx=5,
        ipady=5,
        side='top'
    )

    root.mainloop()