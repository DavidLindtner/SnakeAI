import multiprocessing
import time

from kivy.core.window import Window


class Proc(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        Window.hide()
        generate = 1
        while generate:
            generate = self.task_queue.get()
            print("Process - " + str(generate))
            time.sleep(1)
            self.task_queue.task_done()
            self.result_queue.put([generate, generate, generate])