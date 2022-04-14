"""This file is useful to handle some slow tasks in parallel."""

import multiprocessing


class MultiProcessingTasks:
    """This is a class to manage tasks in parallel."""

    def __init__(self):
        """Create the MultiProcessingTasks object."""
        self.process_list = []

    def startNewProcess(self, function):
        """Start new tasks."""
        process = multiprocessing.Process(target=function)
        process.start()
        self.process_list.append(process)

    def endAllProcesses(self):
        """End all tasks."""
        for process in self.process_list:
            process.join()
            process.close()
        self.process_list.clear()
