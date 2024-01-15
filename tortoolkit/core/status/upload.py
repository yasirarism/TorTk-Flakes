from .status import Status, QBTask
from ..getVars import get_val
import os

class TGUploadTask(Status):
    
    def __init__(self, task):
        super().__init__()
        self.Tasks.append(self)
        self._dl_task = task
        self._files = 0
        self._dirs = 0
        self._uploaded_files = 0
        self._active = True
        self._current_file = ""

    async def set_inactive(self):
        self._active = False

    async def is_active(self):
        return self._active

    async def add_a_dir(self, path):
        await self.dl_files(path)

    async def dl_files(self, path = None):
        if path is None:
            path = await self._dl_task.get_path()
        
        files = self._files
        dirs = self._dirs
        for _, d, f in os.walk(path, topdown=False):
            for _ in f:
                files += 1
            for _ in d:
                dirs += 1
        
        # maybe will add blacklisting of Extensions
        self._files = files
        self._dirs = dirs

    async def uploaded_file(self, name=None):
        self._uploaded_files += 1
        print(f"\n----updates files to {self._uploaded_files}\n")
        self._current_file = str(name)

    async def create_message(self):
        msg = f"<b>Uploading:- </b> <code>{self._current_file}</code>\n"
        prg = 0
        try:
            prg = self._uploaded_files/self._files

        except ZeroDivisionError:pass
        msg += f"<b>Progress:- </b> {self.progress_bar(prg)} - {prg * 100}\n"
        msg += f"<b>Files:- </b> {self._uploaded_files} of {self._files} done.\n"
        msg += "<b>Type:- </b> <code>TG Upload</code>\n"
        return msg

    def progress_bar(self, percentage):
        """Returns a progress bar for download
        """
        #percentage is on the scale of 0-1
        comp = get_val("COMPLETED_STR")
        ncomp = get_val("REMAINING_STR")
        return "".join(comp if i <= int(percentage*10) else ncomp for i in range(1,11))