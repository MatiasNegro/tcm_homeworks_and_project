# tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
# requests
import requests
import os
# files
import Simulator

# global
files = []
flagClear = True

def uploadFiles(identityToken):
    
    def info(massage):
        showinfo(
            title = 'result',
            message = massage
        )
    
    def clearFiles():
        for f in os.listdir('Result_Of_Simulation/simulation'):
            os.remove(os.path.join(os.curdir + '/Result_Of_Simulation/simulation', f))
        for s in os.listdir('Result_Of_Simulation/start_list_parsed'):
            os.remove(os.path.join(os.curdir + '/Result_Of_Simulation/start_list_parsed', s))
        for h in os.listdir('Result_Of_Simulation/start_list_unparsed'):
            os.remove(os.path.join(os.curdir + '/Result_Of_Simulation/start_list_unparsed', h))
        files.clear()
        labelFileName.configure(text="")
        global flagClear
        flagClear = True
    
    def selectFile():
        if(flagClear):
            nSim = number_generation.get("1.0", END + "-1c")
            nSim = int(nSim)
            Simulator.simulation(nSim)
            for f in os.listdir('Result_Of_Simulation/simulation'):
                path = os.path.join(os.curdir + '/Result_Of_Simulation/simulation', f)
                files.append(path)
                labelFileName.configure(text=labelFileName.cget("text") + f + "\n")
                generateFileSeparator(path)
            sendPost()

    def generateFileSeparator(filePath):
        f = open(filePath, mode="a")
        f.write("\nFLAGSEPARATORCODE")
        f.close()

    def generateFileHeader(registerRace=False):
        if registerRace==False:
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
        else:
            header = {
                'accept':'application/json', 
                'Authorization':identityToken
            }
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
        url = os.getenv('URL_UPLOAD')
        fileHeaders = generateFileHeader()
        fileDict = generateFileDict()
        r = requests.post(url, files=fileDict, headers=fileHeaders)
        info(r.content)
        global flagClear
        flagClear = False

    def registerracePost():
        url = os.getenv('URL_REGISTERRACE')
        headers = generateFileHeader(True)
        raceName = race_name.get("1.0", END + "-1c")
        raceDate = race_date.get("1.0", END + "-1c")
        r = requests.post(url, params={'race_name':raceName, 'race_date':raceDate}, headers=headers)
        info(r.content)

    # root window
    root = Tk()
    photo = PhotoImage(file="img/icon.png")
    root.iconphoto(False, photo)
    root.title('http post request')
    root.geometry('800x500')
    root.resizable(True, True)
    frame= Frame(root)
    frame.pack(fill = BOTH, expand = True, padx = 10, pady = 20)
    
    # text
    canvas = Canvas(frame, width=750, height=15)
    canvas.create_text(300, 7, text="Inserire numero di file da generare, dopo la generazione premere 'Clear files' per ripetere:", font=("calibri", 11), justify="center")
    canvas.pack(
        side='top'
    )
    # text for number of files
    number_generation = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
    )
    number_generation.pack(
        pady=5,
        fill='x'
    )
    # button to select file
    buttonAddFile = ttk.Button(
        frame,
        text='Generate files and send',
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
    buttonDeleteFile = ttk.Button(
        frame,
        text='Clear files',
        command=clearFiles
    )
    buttonDeleteFile.pack(
        pady=5,
        ipadx=5,
        ipady=5,
        side='top'
    )
    canvas = Canvas(frame, width=750, height=15)
    canvas.create_text(50, 7, text="Race Name:", font=("calibri", 11), justify="center")
    canvas.pack(
        side='top'
    )
    # text for race name
    race_name = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
    )
    race_name.pack(
        pady=5,
        fill='x'
    )
    canvas = Canvas(frame, width=750, height=15)
    canvas.create_text(50, 7, text="Race Date:", font=("calibri", 11), justify="center")
    canvas.pack(
        side='top'
    )
    # text for race date
    race_date = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
    )
    race_date.pack(
        pady=5,
        fill='x'
    )
    buttonRegisterRace = ttk.Button(
        frame,
        text='Register race',
        command=registerracePost
    )
    buttonRegisterRace.pack(
        pady=5,
        ipadx=5,
        ipady=5,
        side='top'
    )

    root.mainloop()