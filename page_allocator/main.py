# Controls the program
import sys

from tkinter import Tk
# Import the data used in the project.
from data import Data
# Import the main window class from the gui file.
from gui import MainWindow

class Ctl:
    @classmethod
    def RunNextProcess(cls):
        # Get the next "process" to run
        next_process = prog_data.process_list[prog_data.next_line]
        prog_data.next_line += 1
        print(next_process)

    @classmethod
    def GetProcessList(cls):
        try:
            process_list = open(sys.argv[1]).readlines()
            return process_list
        except:
            raise RuntimeError('No input file specified')

# Initialize the main data object
prog_data = Data()
prog_data.process_list = Ctl.GetProcessList()

# Create main root window.
root = Tk()
# Get main window object to use.
my_gui = MainWindow(root)

# Set the input file box text.
my_gui.SetInputText(prog_data.process_list)

# Start the GUI
root.mainloop()

