# tkinter
from os import access
from textwrap import fill
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
# requests
import requests

# global
url = 'https://x4d1kgdj83.execute-api.us-east-1.amazonaws.com/default/upload'

def uploadFiles(identityToken):
    # message
    def info(massage):
        showinfo(
            title = 'result',
            message = massage
        )

    # sending 
    def sendPost(url, file_url):
        fileName = fileName_textbox.get("1.0", END + '-1c')
        headerComposite = {'accept': 'application/json', 'Authorization' : identityToken, 'file-name' : fileName}
        file = {'file': open(file_url, 'rb')}
        r = requests.post(url, files=file, headers = headerComposite)
        info(r.content)

    def selectFile():
        filepath = filedialog.askopenfilename()
        url = url_textbox.get("1.0", END + '-1c')
        sendPost(url, filepath)

    # root window
    root = Tk()
    root.title('http post request')
    root.geometry('500x200')
    root.resizable(False, False)
    frame= Frame(root)
    frame.pack(fill = BOTH, expand = True, padx = 10, pady = 20)

    # text
    canvas = Canvas(frame, width=490, height=10)
    canvas.create_text(12, 5, text="url", font="calibri")
    canvas.pack(
        side='top'
    )
    # insert url
    url_textbox = Text(
        frame,
        height = 1,
        background = "white",
        foreground = "black",
        font = ('calibri', 11)
    )
    url_textbox.insert(
        INSERT,
        'https://x4d1kgdj83.execute-api.us-east-1.amazonaws.com/default/upload'
    )
    url_textbox.pack(
        pady=5,
        fill='x'
    )
    # text
    canvas = Canvas(frame, width=490, height=10)
    canvas.create_text(8, 5, text="file name", font="calibri")
    canvas.pack(
        side='top'
    )
    # insert file name
    fileName_textbox = Text(
        frame,
        height = 1,
        background = "white",
        foreground = "black",
        font = ('calibri', 11)
    )
    fileName_textbox.insert(
        INSERT,
        'xmlProva.xml'
    )
    fileName_textbox.pack(
        pady=5,
        fill='x'
    )
    # button to select file
    button = ttk.Button(
        frame,
        text='select file and send',
        command=selectFile
    )
    button.pack(
        pady=5,
        ipadx=5,
        ipady=5,
        side='top'
    )

    # main
    root.mainloop()