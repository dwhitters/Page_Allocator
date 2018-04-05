from tkinter import Tk, Frame, Label, Button, Text, Menu, W, E, N, S, DISABLED, messagebox

# Contains the main window.
class MainWindow:
    # Constructor.
    def __init__(self, master, presenter):
        # Container identifiers
        FILE_CONTAINER   = 0
        RAM_CONTAINER    = 1
        OUTPUT_CONTAINER = 2

        self.master = master
        master.title("Simulated Page Allocation Manager")

        self.presenter = presenter

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
        self.output_frame.grid(row=0, column=OUTPUT_CONTAINER, sticky=E+W)

        self.CreateMenuBar()
        self.presenter.SetGui(self)

    def printMe(self):
        print("Me")

    # Creates the menubar with a "File" dropdown menu.
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

    # Sets the text within a textbox.
    #
    # @param frame
    #   The textbox to be set.
    # @param text
    #   The text that the textbox text will be set to.
    def SetText(self, frame, text):
        # Delete all text in the box from line 1, character 0 to end.
        frame.delete(1.0, "end")
        # Set the text.
        frame.insert("end", text)

    # Appends text to the text within a text box.
    #
    # @param text
    #   The text to be appended.
    def AppendText(self, box, text):
        # Append the text from the end of the previous text.
        box.insert("end", text)

    # Sets up the file frame to a default string.
    def SetupFileFrame(self):
        self.input_box = Text(self.file_frame)
        self.input_box.grid(row=0, column=0)

        self.SetText(self.input_box, "I'm the input")

    # Sets up the RAM frame.
    #
    # @param num_frames
    #   The number of frames that will be created.
    def SetupRamFrame(self, num_frames):
        self.frames = [] # Create list of frames
        for i in range(0, int(num_frames)):
            # Create a list of "frames"
            self.frames.append(Text(self.ram_frame, width=20, height=5))
            # Set text to "Free".
            self.SetText(self.frames[i], "Free")
            # Display the frames in the ram frame container.
            self.frames[i].grid(row=i,column=0, sticky=W+E+N+S, padx=10)

        back_button = Button(self.ram_frame, text="Back", command=self.printMe)
        back_button.grid(row=int(num_frames) + 1, column=0, sticky = W+E+N+S, pady=10)
        next_button = Button(self.ram_frame, text="Next", command=self.presenter.RunNextProcess)
        next_button.grid(row=int(num_frames) + 2, column=0, sticky=W+E+N+S, pady=10)

    # Sets up the output frame.
    def SetupOutputFrame(self):

        # Setup the process log box.
        self.output_box = Text(self.output_frame)
        self.output_box.grid(row=0, column=0)
        self.SetText(self.output_box, "")

        # Setup the page table output box.
        self.page_table_box = Text(self.output_frame)
        self.page_table_box.grid(row=1, column=0)
        self.SetText(self.page_table_box, "")

    # Sets the input text to the text within the list.
    #
    # @param text_list
    #   The list of text which the input text box will be set to.
    def SetInputText(self, text_list):
        self.SetText(self.input_box, "".join(text_list))
        self.input_box.config(state=DISABLED) # Make input box readonly.

    # Adds text to the output box.
    #
    # @param text
    #   The text to be added to the box.
    def AddOutputText(self, text):
        self.AppendText(self.output_box, text)
        self.output_box.see("end") # Scroll to end of box.

    # Sets the page table box text.
    #
    # @param text
    #   The text to set the page table box text to.
    def SetPageTableBoxText(self, text):
        self.SetText(self.page_table_box, text)
        self.page_table_box.see("end") # Scroll to end of box.

    # Popup with the title and text.
    #
    # @param title
    #   The title of the popup box.
    # @param text
    #   The message within the popup.
    def PopupWarning(self, title, text):
        messagebox.showwarning(title, text)

    # Set the object's text in the RAM frame.
    def SetFrameText(self, frame_num, text):
        self.SetText(self.frames[frame_num], text)

    # Setup the GUI.
    def SetupFrames(self, num_frames):
        self.SetupFileFrame()
        self.SetupRamFrame(num_frames)
        self.SetupOutputFrame()

