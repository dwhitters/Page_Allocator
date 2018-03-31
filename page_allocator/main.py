# Controls the program

from tkinter import Tk
# Import the data used in the project.
from data import Data
# Import the main window class from the gui file.
from gui import MainWindow

class Ctl:
    def RunNextProcess(self):
        # Get the next "process" to run
        next_process = prog_data.process_list[prog_data.next_line]
        print(next_process)

# Initialize the main data object
prog_data = Data()

# Create main root window.
root = Tk()
# Get main window object to use.
my_gui = MainWindow(root)

# Start the GUI
root.mainloop()

