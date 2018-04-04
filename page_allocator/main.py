# Controls the program
import sys

from tkinter import Tk
# Import the data used in the project.
from data import Data, PCB
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

    # Adds a process to main memory if it can fit. If so, a PCB is created
    # for it and frames in memory are allocated to it.
    #
    # @param process
    #   The process trace tape input list.
    def StartProcess(self, process):
        process_id = process[PID_IDX] # Get the process id.
        # Calculate number of pages needed for code (round up).
        num_code_pages = int((int(process[CODE_SIZE_IDX]) + self.data.page_size - 1) / self.data.page_size)
        # Calculate number of pages needed for data (round up).
        num_data_pages = int((int(process[DATA_SIZE_IDX]) + self.data.page_size - 1) / self.data.page_size)
        # Check if there's room in RAM.
        if len(self.data.free_frames_list) > (num_code_pages + num_data_pages):
            self.gui.AddOutputText("Loading program "+process_id+" into RAM:"+
                                    "code="+process[CODE_SIZE_IDX]+" ("+
                                    str(num_code_pages)+
                                    " pages), data="+process[DATA_SIZE_IDX]+
                                    " ("+str(num_data_pages)+" pages)\n")
            code_page_table = []
            # Allocate the frames and create page table for code
            for i in range(0, int(num_code_pages)):
               code_page_table.append(self.data.free_frames_list[0])
               self.gui.SetFrameText(self.data.free_frames_list[0], "Code-"+str(i)+" of P"+str(process_id))
               self.gui.AddOutputText("Load Code page "+str(i)+" of process "+
                                      process_id+" to frame "+
                                      str(self.data.free_frames_list[0])+"\n")
               del self.data.free_frames_list[0]

            data_page_table = []
            # Allocate the frames and create page table for data
            for i in range(0, int(num_data_pages)):
               data_page_table.append(self.data.free_frames_list[0])
               self.gui.SetFrameText(self.data.free_frames_list[0], "Data-"+str(i)+" of P"+str(process_id))
               self.gui.AddOutputText("Load Data page "+str(i)+" of process "+
                                      process_id+" to frame "+
                                      str(self.data.free_frames_list[0])+"\n")
               del self.data.free_frames_list[0]

            # Save the data and code page tables in a "process control block".
            pcb = PCB(process_id)

            pcb.code_size = process[CODE_SIZE_IDX]
            pcb.data_size = process[DATA_SIZE_IDX]
            pcb.num_code_pages = num_code_pages
            pcb.num_data_pages = num_data_pages
            pcb.code_page_table = code_page_table
            pcb.data_page_table = data_page_table

            self.data.pcb_table.append(pcb)

        else:
            self.gui.AddOutputText("Not enough space for program "+process_id+"!\n")

        # Set the page table output text with the updated tables.
        self.gui.SetPageTableBoxText(self.CompilePageTableText())

    # Compiles the text to set the Page table output text box to.
    #
    # @return
    #   String that the page table output text box should be set to.
    def CompilePageTableText(self):
        page_table_text = "PAGE TABLES:\n\n"
        # Get table data from each process in memory.
        for pcb in self.data.pcb_table:
            page_table_text += ("P"+pcb.pid+" page table(s)\n")
            page_table_text += "\tPage\tFrame\n"
            # Display the text table.
            for index, page in enumerate(pcb.code_page_table):
                page_table_text += "Text\t"+str(index)+"\t"+str(page)+"\n"
            for index, page in enumerate(pcb.data_page_table):
                page_table_text += "Data\t"+str(index)+"\t"+str(page)+"\n"

            page_table_text += "\n" # Add extra newline for better separation.

        return page_table_text



    def FreePageTable(self, page_table):
        # Free the RAM frames containing pages in the page table.
        for page in page_table:
            self.data.free_frames_list.append(page)
            # Clear the frame text.
            self.gui.SetFrameText(self.data.free_frames_list[-1], "Free")

    def FreeProcess(self, pcb):
        self.FreePageTable(pcb.code_page_table)
        self.FreePageTable(pcb.data_page_table)

        # Remove the freed process' control block from the table.
        self.data.pcb_table.remove(pcb)

    def TerminateProcess(self, process):
        process_id = process[PID_IDX] # Get the process id
        # An error will be raised if a process is terminated that doesn't exist.
        try:
            # Find the process control block if it exists.
            pcb = [block for block in self.data.pcb_table if block.pid == process_id][0]
            # Free the process.
            self.FreeProcess(pcb)
            self.gui.AddOutputText("End of Program "+process_id+"\n")
        except:
            self.gui.AddOutputText("Termination not executed. PID #"+str(process_id)+" not in memory!\n")

        # Set the page table output text with the updated tables.
        self.gui.SetPageTableBoxText(self.CompilePageTableText())

# Start the program
# Create main root window.
root = Tk()
# Get main window object to use and give a presenter object.
my_gui = MainWindow(root, Ctl())

# Start the GUI
root.mainloop()
