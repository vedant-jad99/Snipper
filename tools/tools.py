import pyautogui as pag
from tkinter import filedialog, Toplevel, Label, Button, RAISED
from PIL import ImageTk
from datetime import datetime as dt
import json
from show_report.scripts.insert_table import show

global label_image
global json_path
json_path = "activity_and_logs/activities.json"

def screenshotimage():
    image = pag.screenshot()
    a, b = image.size
    return image.resize((int(a * 0.9), int(b * 0.9)))

def saveimage(image):
    global json_path

    if image == None:
        window = Toplevel(name="#Error")
        window.title("#Error")
        message = Label(window, width=35, height=7, padx=10, pady=10, text="Error! No image to save!", fg='red')
        button = Button(window, width=10, height=2, padx=10, relief=RAISED, borderwidth=3, text="OK", command=window.destroy)
        
        message.grid(row=0, column=0)
        button.grid(row=1, column=0)
        return None

    path = filedialog.asksaveasfilename(title="Save file", filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    if path != ():
        width, height = image.size
        image = image.resize((int(width*1.11), int(height*1.111)))
        image.save(path)
        with open(json_path, "r") as f:
            activity = json.load(f)
            data = {"timestamp": str(dt.now()), "activity": "Snip saved", "location": path}
            activity.append(data)
            with open(json_path, "w") as file:
                json.dump(activity, file)
                file.close()
            f.close()

def clearimage(func, label, icons):
    func()
    label.configure(image=icons['blank'])

def undoimage(image_stack, redo_stack, label, func):
    global label_image
    if len(image_stack) > 1:
        redo_stack.append(image_stack.pop())
        label_image = ImageTk.PhotoImage(image_stack[-1])
        label.configure(image=label_image)
        func(image_stack[-1])
    if len(image_stack) == 1:
        func()

def redoimage(redo_stack, image_stack, label, func):
    global label_image
    if len(redo_stack) > 0:
        image = redo_stack.pop()
        image_stack.append(image)
        label_image = ImageTk.PhotoImage(image)
        label.configure(image=label_image)
        func(image)
    else:
        func()

def closewindow(root):
    root.destroy()

def activity_report():
    global json_path
    with open(json_path, "r") as f:
        activity = json.load(f)
        data = {"timestamp": str(dt.now()), "activity": "Viewed report", "location": " "}
        activity.append(data)
        with open(json_path, "w") as file:
            json.dump(activity, file)
            file.close()
        f.close()
        show()

def clear_activity():
    def clear():
        activity = []
        with open(json_path, "w") as file:
            json.dump(activity, file)
            file.close()
        window.destroy()

    window = Toplevel()
    message = Label(window, width=35, height=7, padx=10, pady=10, text="Are you sure you want to clear?", fg='red')
    space = Label(window, width=10)
    button = Button(window, width=10, height=2, padx=10, relief=RAISED, borderwidth=3, text="Yes", command=clear)
    button1 = Button(window, width=10, height=2, padx=10, relief=RAISED, borderwidth=3, text="No", command=window.destroy)
    message.grid(row=0, column=0)
    button.grid(row=1, column=0)
    button1.grid(row=1, column=1)
    space.grid(row=1, column=2)
