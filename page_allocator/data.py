from math import log, ceil, floor

# Holds the data used by the program.

# Set the size of kilobyte to 1024 bytes.
KB = 1024

# Process control block class. Contains the PID, code size, data size,
# code page table, and data page table.
class PCB:
    def __init__(self, PID):
        self.pid = PID
        self.code_size = 0
        self.data_size = 0
        self.num_code_pages = 0
        self.num_data_pages = 0
        self.code_page_table = []
        self.data_page_table = []

# Holds all information used by the program.
class Data:
    # Constructor.
    def __init__(self):
        self._page_size = 512   # Set the default page size to 512 bytes
        self._ram_size = 4 * KB # Set the default RAM size to 4KB
        self._num_frames = self._ram_size / self._page_size    # Defaults to 8 frames

        self._next_line = 0 # The next line to be processed in the process list.

        self._process_list = [] # Contains the list of process actions.

        # Holds the free frames.
        self._free_frames_list = list(range(int(self._num_frames)))

        # Contains all process control blocks in use.
        self._pcb_table = []

    # Getters and setters.
    @property
    def pcb_table(self):
        return self._pcb_table

    @pcb_table.setter
    def pcb_table(self, value):
        self._pcb_table = value

    @property
    def next_line(self):
        return self._next_line

    @next_line.setter
    def next_line(self, value):
        self._next_line = value

    @property
    def num_frames(self):
        return self._num_frames

    @num_frames.setter
    def num_frames(self, value):
        self._num_frames = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        # Make sure the page size is a power of 2.
        log_base_2 = log(value, 2)
        if ceil(log_base_2) == floor(log_base_2):
            self._page_size = value

    @property
    def ram_size(self):
        return self._ram_size

    @ram_size.setter
    def ram_size(self, value):
        # Make sure the page size is a power of 2.
        log_base_2 = log(value, 2)
        # Ram size must be greater than page size.
        if (value % self._page_size == 0) and (self._ram_size > self._page_size):
            self._ram_size = value

    @property
    def free_frames_list(self):
        return self._free_frames_list

    @free_frames_list.setter
    def free_frames_list(self, value):
        self._free_frames_list = value

