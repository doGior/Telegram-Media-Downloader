class Queue:
    def __init__(self):
        self.q = []
        self.__front = 0
        self.__rear = 0

    def enqueue(self, item):
        self.q.append(item)
        self.__rear = len(self.q)-1

    def dequeue(self):
        item = self.q[self.__front]
        self.q.pop(self.__front)
        self.__rear = len(self.q) - 1
        return item

    def is_empty(self):
        return len(self.q) == 0

    def front(self):
        return self.q[self.__front]

    def rear(self):
        return self.q[self.__rear]
