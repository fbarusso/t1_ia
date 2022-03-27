def get_node_from_list(nodes_list, id_number):
    for node in nodes_list:
        if node.id_number == id_number:
            return node
    print('Error: invalid id')


class Node(object):
    def __init__(self, id_number, lat, long):
        self.id_number = id_number
        self.lat = lat
        self.long = long
        self.adj = []

    def insert_adj(self, data):
        self.adj.append(data)


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0

    def insert(self, data, priority):
        self.queue.append([data, priority])

    def pop(self):
        try:
            max_priority_index = 0
            for i in range(len(self.queue)):
                if self.queue[i][1] < self.queue[max_priority_index][1]:
                    max_priority_index = i
            item = self.queue[max_priority_index][0]
            del self.queue[max_priority_index]
            return item
        except IndexError:
            print('Index error on pop function')
