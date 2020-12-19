import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk, ImageDraw
import os
import buttonTools.button_tools as t
from buttonTools.toolTip import CreateToolTip
from time import sleep

global icons
global image

class Snipper:
    def __init__(self, root):
        frame1 = tk.Frame(root)
        frame2 = tk.Frame(root, background='black')
        self.__image = None

        global icons

        path = str(__file__).split("main_app")[0]
        icons = self.__load_images(path)
        self.__image_stack = [Image.open(os.path.join(path, 'assets/blank.png')).resize((400, 250))]
        self.__redo_stack = []

        self.__save = tk.Button(frame1, pady=5, relief=tk.GROOVE, borderwidth=2, image=icons['save'], command=lambda: t.saveimage(self.__image))
        self.__snip = tk.Button(frame1, pady=5, relief=tk.GROOVE, borderwidth=2, image=icons['snip'], command=lambda: self.__on_snip_click(root))
        self.__clear = tk.Button(frame1, padx=5, relief=tk.GROOVE, borderwidth=2, image=icons['clear'], command=lambda: t.clearimage(self.set_image, self.__image_container, icons))
        self.__undo = tk.Button(frame1, padx=5, relief=tk.GROOVE, borderwidth=2, image=icons['undo'], command=lambda: t.undoimage(self.__image_stack, self.__redo_stack, self.__image_container, self.set_image))
        self.__redo = tk.Button(frame1, padx=5, relief=tk.GROOVE, borderwidth=2, image=icons['redo'], command=lambda: t.redoimage(self.__redo_stack, self.__image_stack, self.__image_container, self.set_image))
        self.__close = tk.Button(frame1, padx=5, relief=tk.GROOVE, borderwidth=2, image=icons['close'], command=lambda: t.closewindow(root))
        self.__space = tk.Label(frame1, width=7)
        self.__options = tk.Menubutton(frame1, padx=5, relief=tk.GROOVE, borderwidth=2, image=icons['options'])

        self.__options.menu = Menu(self.__options, tearoff=0)
        self.__options["menu"] = self.__options.menu
        self.__options.menu.add_command(label="Activity Report", command=t.activity_report)
        self.__options.menu.add_command(label="Clear Report", command=t.clear_activity)

        self.__image_container = tk.Label(frame2, padx=2, pady=2, image=icons['blank'], cursor='tcross')
        self.__image_container.bind("<Button-1>", self.__snip_start)
        self.__image_container.bind("<B1-Motion>", self.__on__motion)
        self.__image_container.bind("<ButtonRelease-1>", self.__snip_release)
        
        self.__snip.grid(row=0, column=0)
        self.__save.grid(row=0, column=1)
        self.__undo.grid(row=0, column=2)
        self.__redo.grid(row=0, column=3)
        self.__clear.grid(row=0, column=4)
        self.__close.grid(row=0, column=5)
        self.__space.grid(row=0, column=6)
        self.__options.grid(row=0, column=7)
        self.__image_container.grid(row=0, column=0)
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)

        save_ttp = CreateToolTip(self.__save, "Save File")
        snip_ttp = CreateToolTip(self.__snip, "Snip Screen")
        clear_ttp = CreateToolTip(self.__clear, "Clear Board")
        undo_ttp = CreateToolTip(self.__undo, "Undo")
        redo_ttp = CreateToolTip(self.__redo, "Redo")
        options_ttp = CreateToolTip(self.__options, "Options")
        close_ttp = CreateToolTip(self.__close, "Exit")


    def set_image(self, image=None):
        self.__image = image


    def __load_images(self, path):
        images = {}

        path = os.path.join(path, 'assets')
        for i in os.listdir(path):
            name = i.split('.')
            image = Image.open(os.path.join(path, i))
            if name[0] == 'blank':
                image = image.resize((400, 250))
            else:
                image = image.resize((40, 25))
            images[name[0]] = ImageTk.PhotoImage(image)
        
        return images

    
    def __on_snip_click(self, root):
        global image
        root.withdraw()
        sleep(0.5)

        image = t.screenshotimage()
        self.__image = image
        image = ImageTk.PhotoImage(image)

        self.__image_stack.append(self.__image)
        self.__image_container.configure(image=image)
        root.deiconify()


    def __on__motion(self, event):
        if self.__image == None:
            return

        global image
        x, y = event.x, event.y
        image = self.__image.copy()
        draw = ImageDraw.Draw(image, "RGBA")
        draw.rectangle(((self.__x, self.__y), (x, y)), fill= (150, 150, 150, 127))
        image = ImageTk.PhotoImage(image)
        self.__image_container.configure(image=image)

    
    def __snip_start(self, event):
        self.__x, self.__y = event.x, event.y


    def __snip_release(self, event):
        if self.__image == None:
            return

        global image
        x, y = event.x, event.y
        self.__image = self.__image.crop((self.__x, self.__y, x, y))
        image = ImageTk.PhotoImage(self.__image)
        self.__image_container.configure(image=image)
        self.__image_stack.append(self.__image)

