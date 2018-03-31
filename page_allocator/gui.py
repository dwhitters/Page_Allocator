from tkinter import Tk, Frame, Label, Button, Text, Menu, W, E, N, S

from data import Data

class LeftContainer:
    def __init__(self, master):
        self.master = master

        self.label_text = "ASDF"
        self.label = Label(master, textvariable=self.label_text)

        self.greet_button = Button(master, text="Greet", command=self.greet)

        self.close_button = Button(master, text="Close", command=master.quit)

        self.label.grid(columnspan=1, row=0, sticky=W)
        self.greet_button.grid(row=1)
        self.close_button.grid(row=2)

    def greet(self):
        print("Greetings")

class MainWindow:
    def __init__(self, master):

        # Container identifiers
        FILE_CONTAINER   = 0
        RAM_CONTAINER    = 1
        OUTPUT_CONTAINER = 2

        self.master = master
        master.title("A simple GUI")

        self.data = Data()

        # Allow file and output containers to grow when window is expanded.
        master.grid_columnconfigure(FILE_CONTAINER, weight=1)
        master.grid_columnconfigure(RAM_CONTAINER, weight=0)
        master.grid_columnconfigure(OUTPUT_CONTAINER, weight=1)

        # Allow the layout to expand up and down.
        master.grid_rowconfigure(0, weight=1)

        # Create the main containers
        self.file_frame = Frame(master, bg='cyan', width=450, height=500)
        self.ram_frame = Frame(master, bg="red", width=450, height=500)
        self.output_frame = Frame(master, bg="green", width=450, height=500)

        # Layout the main containers
        self.file_frame.grid(row=0, column=FILE_CONTAINER, sticky=E+W)
        self.ram_frame.grid(row=0, column=RAM_CONTAINER, sticky=N+S+E+W)
        self.output_frame.grid(row=0, column=OUTPUT_CONTAINER, sticky=E+W+N+S)

        self.CreateMenuBar()
        self.SetupFrames()

    def printMe(self):
        print("Me")
    def CreateMenuBar(self):
        # Setup the menu and sub menu
        menubar = Menu(self.master)
        sub_menu = Menu(menubar)
        sub_menu.add_command(label="Set Page Size...", command=self.printMe)
        sub_menu.add_command(label="Set RAM Size...", command=self.printMe)
        sub_menu.add_command(label="Exit", command=self.master.quit)

        # Make file a dropdown menu
        menubar.add_cascade(label="File", menu=sub_menu)

        self.master.config(menu=menubar)

    def SetFrameText(self, frame, text):
            # Delete all text in the box from line 1, character 0 to end.
            frame.delete(1.0, "end")
            # Set the text.
            frame.insert("end", text)

    def SetupFileFrame(self):
        self.input_box = Text(self.file_frame)
        self.input_box.grid(row=0, column=0)

        self.SetFrameText(self.input_box, "I am the input")

    def SetupRamFrame(self):
        self.frames = [] # Create list of frames
        for i in range(0, int(self.data.num_frames)):
            # Create a list of "frames"
            self.frames.append(Text(self.ram_frame, width=20, height=5))
            # Set text to a blank string.
            self.frames[i].insert("end", "breh")
            # Display the frames in the ram frame container.
            self.frames[i].grid(row=i,column=0)

        close_button = Button(self.ram_frame, text="Next", command=self.printMe)

    def SetupOutputFrame(self):
        self.output_box = Text(self.output_frame)
        self.output_box.grid(row=0, column=0)

        self.SetFrameText(self.output_box, "I am the output")

    def SetupFrames(self):
        self.SetupFileFrame()
        self.SetupRamFrame()
        self.SetupOutputFrame()

