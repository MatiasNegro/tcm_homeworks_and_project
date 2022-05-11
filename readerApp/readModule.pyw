# tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
# requests
import requests
import json
# local env
import os
from dotenv import load_dotenv

# global
load_dotenv()

def info(message, title='Result'):
    showinfo(
        title,
        message
    )

#try:

def dictRaces():
    url = os.getenv('URL_LISTRACES')
    r = requests.get(url)
    body = r.content.decode('utf-8')
    info(body, 'JSON')
    '''bodyDict = json.loads(body)
    for j in bodyDict:
        raceName = 'race name: ' + bodyDict[j]['race_name'] + '\n'
        raceDate = 'race date: ' + bodyDict[j]['race_date'] + '\n'
        raceId = 'race id: ' + bodyDict[j]['race_id']
        message = raceName + raceDate + raceId
        info(message, "event " + str(j))'''

def downloadFile():
    searchedFile = fileSearched_textbox.get("1.0", END + '-1c')
    searchedFile = searchedFile.replace('\n', '')
    if(searchedFile != ''):
        headers = {
            'filename':searchedFile
        }
        url = os.getenv('URL_DOWNLOAD')
        r = requests.get(url, headers=headers)
        file = r.content
        file = file.decode('utf-8')
        if('404' in file):
            info('Error 404: file not found.')
        else: 
            destinationUrl = 'downloads/' + fileSearched_textbox.get("1.0", END + '-1c')
            f = open(destinationUrl, 'w+')
            f.write(file)
            f.close()
            info('File downloaded succesfully, check downloads folder.')
        fileSearched_textbox.delete('1.0', END)

def list_classes():
    url = os.getenv('URL_LISTCLASSES')
    id = id_textBox.get("1.0", END + '-1c')
    r = requests.get(url, params = {'id' : id})
    body = r.content.decode('utf-8')
    info(body, 'JSON')

def results(id, cl):
    url = os.getenv('URL_RESULTS')
    id = id_textBox.get("1.0", END + '-1c')
    cl = class_textBox.get("1.0", END + '-1c')
    r = requests.get(url, params = {'id' : id, 'class' : cl})
    body = r.content.decode('utf-8')
    info(body, 'JSON')

# root window
root = Tk()
photo = PhotoImage(file="img/icon.png")
root.iconphoto(False, photo)
root.title('Download files')
root.geometry('500x500')
root.resizable(True, True)
frame = Frame(root)
frame.pack(fill = BOTH, expand = True, padx = 10, pady = 20)

# label title
labelFileName = ttk.Label(
    frame,
    text = 'Files in the database:',
    font = ('calibri', 13)
)
labelFileName.pack(
    pady = 5,
    ipadx = 5,
    side = 'top'
)
# get all the files in the bucket
buttonListRaces = ttk.Button(
    frame,
    text = 'list_races',
    command = dictRaces
)
buttonListRaces.pack(
    ipadx = 5,
    ipady = 5,
)
# get all clases of a race
canvas = Canvas(frame, width=750, height=15)
canvas.create_text(50, 7, text="Race Id:", font=("calibri", 11), justify="center")
canvas.pack(
    side='top'
)
id_textBox = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
)
id_textBox.pack(
    pady = 5,
    fill = 'x'
)
canvas = Canvas(frame, width=750, height=15)
canvas.create_text(50, 7, text="Race Class:", font=("calibri", 11), justify="center")
canvas.pack(
    side='top'
)
class_textBox = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
)
class_textBox.pack(
    pady = 5,
    fill = 'x'
)
buttonListClasses = ttk.Button(
    frame,
    text = 'list_classes',
    command = list_classes
)
buttonListClasses.pack(
    ipadx = 5,
    ipady = 5,
)
# get ranking of a class in an event
buttonResults = ttk.Button(
    frame,
    text = 'results',
    command = results
)
buttonResults.pack(
    ipadx = 5,
    ipady = 5,
)
downloadFrame = Frame(frame)
downloadFrame.pack(fill = BOTH, expand = True)

# button that downloads file
buttonSend = ttk.Button(
    frame,
    text = 'Download',
    command = downloadFile
)
buttonSend.pack(
    ipadx = 5,
    ipady = 5,
    side = 'left'
)
# file name textbox
fileSearched_textbox = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
)
fileSearched_textbox.pack(
    pady = 5,
    fill = 'x',
    side = 'right'
)

root.mainloop()

#except BaseException as error:
#    showinfo(title='Error', message="Sorry, there was an error :/")
#    root.destroy()