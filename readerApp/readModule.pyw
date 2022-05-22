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
from pprint import pprint
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
    info(body, 'dictRaces')

def downloadFile():
    searchedFile = id_textBox.get("1.0", END + '-1c') + '.xml'
    searchedFile = searchedFile.replace('\n', '')
    if(searchedFile.replace('.xml', '') != ''):
        headers = {
            'filename':searchedFile
        }
        url = os.getenv('URL_DOWNLOAD')
        r = requests.get(url, headers=headers)
        pprint(r.json)
        file = r.content
        file = file.decode('utf-8')
        if('error404' in file):
            info('Error 404: race not found.')
        else: 
            destinationUrl = 'downloads/' + searchedFile
            f = open(destinationUrl, 'w+')
            f.write(file)
            f.close()
            info('File downloaded succesfully, check downloads folder.', 'downloadFile')

def list_classes():
    url = os.getenv('URL_LISTCLASSES')
    id = id_textBox.get("1.0", END + '-1c')
    if id!='':
        r = requests.get(url, params = {'id' : id})
        body = r.content.decode('utf-8')
        info(body, 'list_classes')

def results():
    url = os.getenv('URL_RESULTS')
    id = id_textBox.get("1.0", END + '-1c')
    cl = class_textBox.get("1.0", END + '-1c')
    r = requests.get(url, params = {'id' : id, 'class' : cl})
    body = r.content.decode('utf-8')
    info(body, 'results')

# root window
root = Tk()
photo = PhotoImage(file="img/icon.png")
root.iconphoto(False, photo)
root.title('Download files')
root.geometry('500x350')
root.resizable(True, True)
frame = Frame(root)
frame.pack(fill = BOTH, expand = True, padx = 10, pady = 20)

# label title
labelFileName = ttk.Label(
    frame,
    text = 'Races in the database:',
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
buttonResults = ttk.Button(
    frame,
    text = 'results',
    command = results
)
buttonResults.pack(
    ipadx = 5,
    ipady = 5,
)
buttonSend = ttk.Button(
    frame,
    text = 'Download xml',
    command = downloadFile
)
buttonSend.pack(
    ipadx = 5,
    ipady = 5,
    side = 'top'
)

root.mainloop()

#except BaseException as error:
#    showinfo(title='Error', message="Sorry, there was an error :/")
#    root.destroy()