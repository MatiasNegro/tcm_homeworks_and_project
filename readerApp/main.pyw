# tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from idToken import getIdToken
from readModule import readerFiles
    
def login():
    user = username_textbox.get("1.0", END + '-1c')
    passw = password_textbox.get("1.0", END + '-1c')
    try:
        idToken = getIdToken(user, passw)
        root.destroy()
        readerFiles(idToken)
    except BaseException as error:
        showinfo(title='Error', message="Login failed, username or password incorrect.")

# root window
root = Tk()
photo = PhotoImage(file="img/icon.png")
root.iconphoto(False, photo)
root.title('Download files')
root.geometry('300x200')
root.resizable(False, False)
frame = Frame(root)
frame.pack(fill = BOTH, expand = True, padx = 10, pady = 20)

# text
canvas = Canvas(frame, width=490, height=15)
canvas.create_text(35, 10, text = "Username", font = ("calibri", 11))
canvas.pack(
    side = 'top'
)
# insert url
username_textbox = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
)
username_textbox.insert(
    INSERT,
    'user'
)
username_textbox.pack(
    pady = 5,
    fill = 'x'
)
# text
canvas = Canvas(frame, width=490, height=15)
canvas.create_text(32, 10, text = "Password", font = ("calibri", 11))
canvas.pack(
    side = 'top'
)
# insert file name
password_textbox = Text(
    frame,
    height = 1,
    background = "white",
    foreground = "black",
    font = ('calibri', 11)
)
password_textbox.insert(
    INSERT,
    'Username123!'
)
password_textbox.pack(
    pady = 5,
    fill = 'x'
)
# button to select file
button = ttk.Button(
    frame,
    text = 'Login',
    command = login
)
button.pack(
    pady = 5,
    ipadx = 5,
    ipady = 5,
    side = 'top'
)

# main
root.mainloop()