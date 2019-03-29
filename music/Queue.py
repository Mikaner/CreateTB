

class Queue:
    def __init__(self):
        self.queue = list()

    def add_queue(self, job):
        self.queue.append(job)

    def interrupt_queue(self, job, position: int):
        try:
            if position > 0:
                self.queue.insert(position-1, job)
            elif position < 0:
                self.queue.insert(position, job)
            else:
                return 0
        except IndexError as e:
            return e

    def remove_queue(self, position: int):
        try:
            if position > 0:
                return self.queue.pop(position-1)
            elif position < 0:
                return self.queue.pop(position)
            else:
                # remove music of playing now
                return 0
        except IndexError as e:
            return e

    def move_queue(self, job, position: int):
        if position==0:
            return
        # cannot move with IndexError
        self.interrupt_queue(self.remove_queue(position), position)

    def next_job(self):
        if self.queue == []:
            return
        return self.queue.pop(0)

    def get_queue(self):
        return self.queue

    def queue_clear(self):
        self.queue.clear()