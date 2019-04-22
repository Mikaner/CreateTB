

class Queue:
    def __init__(self):
        self.queue = list()

    def convert_value(self, position: int):
        return position if position < 1 else position-1

    def add_queue(self, job):
        self.queue.append(job)

    def interrupt_queue(self, job, position: int):
        try:
            if position >= 0:
                self.queue.insert(position, job)
            elif position == -1:
                self.queue.append(job)
            else:
                self.queue.insert(position+1)
        except IndexError:
            raise

    def remove_queue(self, position: int):
        try:
            return self.queue.pop(position)
        except IndexError:
            raise

    def move_queue(self, from_position: int, to_position: int):
        if len(self.queue) < from_position or len(self.queue) < to_position:
            raise IndexError
            return
        self.interrupt_queue(self.remove_queue(from_position), to_position)

    def next_job(self):
        if self.queue == []:
            return None
        return self.queue.pop(0)

    def get_queue(self):
        return self.queue

    def queue_clear(self):
        self.queue.clear()