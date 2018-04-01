# Controls the program
import sys

from tkinter import Tk
# Import the data used in the project.
from data import Data
# Import the main window class from the gui file.
from gui import MainWindow

# Index of the process ID in a process list
PID_IDX = 0
# Index of the code size in a starting process list
CODE_SIZE_IDX = 1
# Index of the data size in a starting process list
DATA_SIZE_IDX = 2

class Ctl:

    def __init__(self):
        # Initialize the main data object
        self.data = Data()
        self.data.process_list = self.GetProcessList()


    def SetGui(self, gui):
        self.gui = gui
        # Setup gui
        self.gui.SetupFrames(self.data.num_frames)
        # Set the input file box text.
        self.gui.SetInputText(self.data.process_list)

    def RunNextProcess(self):
        if len(self.data.process_list) > self.data.next_line:
            # Get the next "process" to run and convert it into a list of words.
            next_process = self.data.process_list[self.data.next_line].split()
            if len(next_process) == 2:
                self.TerminateProcess(next_process)
            else: # The only alternative is starting a process.
                self.StartProcess(next_process)

            self.data.next_line += 1
        else:
            self.gui.PopupWarning("Warning!", "No more processes!")

    def GetProcessList(self):
        try:
            process_list = open(sys.argv[1]).readlines()
            return process_list
        except:
            raise RuntimeError('No input file specified')

    def StartProcess(self, process):
        process_id = process[PID_IDX] # Get the process id.
        # Calculate number of pages needed for code (round up).
        num_code_pages = (int(process[CODE_SIZE_IDX]) + self.data.page_size - 1) / self.data.page_size
        # Calculate number of pages needed for data (round up).
        num_data_pages = (int(process[DATA_SIZE_IDX]) + self.data.page_size - 1) / self.data.page_size
        # Check if there's room in RAM.
        if len(self.data.free_frames_list) > (num_code_pages + num_data_pages):
            code_page_table = []
            # Allocate the frames and create page table for code
            for i in range(0, int(num_code_pages)):
               code_page_table.append(self.data.free_frames_list[0])
               self.gui.SetFrameText(self.data.free_frames_list[0], "Code-"+str(i)+" of P"+str(process_id))
               del self.data.free_frames_list[0]

            data_page_table = []
            # Allocate the frames and create page table for data
            for i in range(0, int(num_data_pages)):
               data_page_table.append(self.data.free_frames_list[0])
               self.gui.SetFrameText(self.data.free_frames_list[0], "Data-"+str(i)+" of P"+str(process_id))
               del self.data.free_frames_list[0]

            # Save the data and code page tables in data with their process ID.
            self.data.data_page_tables.append((process_id, data_page_table))
            self.data.code_page_tables.append((process_id, code_page_table))

    def FreePageTable(self, process_id, page_table, page_table_list):
        # Free the RAM frames containing pages in the page table.
        for page in page_table:
            self.data.free_frames_list.append(page)
            # Clear the frame text.
            self.gui.SetFrameText(self.data.free_frames_list[-1], "Free")

            # Remove the page table from the page table list.
            for table in page_table_list:
                if process_id in table:
                    page_table_list.remove(table)

    def GetPageTable(self, process_id, page_table_list):
        p = None
        for process in page_table_list:
            if process_id in process:
                p = process

        if p is not None:
            return p[1]
        else:
            # Add output text.

    def TerminateProcess(self, process):
        process_id = process[PID_IDX] # Get the process id
        # Find the process data page table in the data page table list.
        data_page_table = self.GetPageTable(process_id, self.data.data_page_tables)
        # If the process was found...
        if data_page_table is not None:
            # Free the data page table
            self.FreePageTable(process_id, data_page_table, self.data.data_page_tables)

            # Find the process code page table in the code page table list.
            code_page_table = self.GetPageTable(process_id, self.data.code_page_tables)
            # Code page table is a tuple. [PID, page_table]
            self.FreePageTable(process_id, code_page_table, self.data.code_page_tables)

# Start the program
# Create main root window.
root = Tk()
# Get main window object to use and give a presenter object.
my_gui = MainWindow(root, Ctl())

# Start the GUI
root.mainloop()
