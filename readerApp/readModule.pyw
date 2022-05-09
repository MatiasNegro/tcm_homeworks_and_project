# tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
# requests
import requests

# global
url = 'https://x4d1kgdj83.execute-api.us-east-1.amazonaws.com/default/download'

def info(massage):
    showinfo(
        title = 'Result',
        message = massage
    )

#try:

def showFiles():
    headers = {
        'mod':'read'
    }
    r = requests.get(url, headers=headers)
    content = r.content
    body = content.decode('utf-8')
    nameList = body.replace('partite/','')
    return nameList

def downloadFile():
    searchedFile = fileSearched_textbox.get("1.0", END + '-1c')
    searchedFile = searchedFile.replace('\n', '')
    if(searchedFile != ''):
        headers = {
            'filename':searchedFile,
            'mod':'download'
        }
        r = requests.get(url, headers=headers)
        file = r.content
        file = file.decode('utf-8')
        if('ResponseMetadata' in file):
            info('Error 404: file not found.')
        else: 
            destinationUrl = 'downloads/' + fileSearched_textbox.get("1.0", END + '-1c') + '.json'
            f = open(destinationUrl, 'w+')
            f.write(file)
            f.close()
            info('File downloaded succesfully, check downloads folder.')
        fileSearched_textbox.delete('1.0', END)

# root window
root = Tk()
photo = PhotoImage(file="img/icon.png")
root.iconphoto(False, photo)
root.title('Download files')
root.geometry('500x500')
root.resizable(True, True)
frame = Frame(root)
frame.pack(fill = BOTH, expand = True, padx = 10, pady = 20)

fileNames = showFiles()

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
# label with all the files in the bucket
labelFileName = ttk.Label(
    frame,
    text = fileNames,
    font = ('calibri', 11)
)
labelFileName.pack(
    ipadx = 5,
    side = 'top'
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