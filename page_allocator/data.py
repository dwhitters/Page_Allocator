# Holds the data used by the program.

# Set the size of kilobyte to 1024 bytes.
KB = 1024

# Frames list
class Data:

    def __init__(self):
        self._page_size = 512   # Set the default page size to 512 bytes
        self._ram_size = 4 * KB # Set the default RAM size to 4KB
        self._num_frames = self._ram_size / self._page_size    # Defaults to 8 frames

        if (self._ram_size % self._page_size) != 0:
            self._num_frames += 1

        self._next_line = 0 # The next line to be processed in the process list.

        self.process_list = self.GetProcessList()

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
        self._page_size = value

    @property
    def ram_size(self):
        return self._ram_size

    @ram_size.setter
    def ram_size(self, value):
        self._ram_size = value


