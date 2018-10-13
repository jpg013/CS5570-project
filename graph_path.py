
class GraphPathNode: 
    def __init__(self, data): 
        self.data = data 
        self.next = None

class GraphPath:
    def __init__(self): 
        self.head = None
        self.tail = None
        self.length = 0

    def add(self, data): 
        new_node = GraphPathNode(data) 
        
        self.length += 1
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        if self.head.data is self.tail.data and self.tail.data is data:
            raise Exception('cannot create a cycle with only 2 nodes')

        # If the node is same as head, this completes a cycle

        self.tail.next = new_node
        self.tail = new_node        

    def creates_cycle(self, node):
        if self.head is None:
            return False

        if self.length < 2:
            return False
        
        return self.head.data is node

    def clone(self):
        clone_cycle = GraphPath()
        temp = self.head

        while (temp):
            clone_cycle.add(temp.data)
            temp = temp.next
        
        return clone_cycle

    def has_non_root_node(self, node):
        if self.head is None:
            return False

        temp = self.head.next

        while (temp):
            if (node is temp.data):
                return True
            
            temp = temp.next
        
        return False
    
    def has_cycle(self): 
        return self.length > 2 and self.head.data is self.tail.data
    
    def pretty_print(self):
        temp = self.head
        
        while temp:
            next = temp.next
            if next is None:
                print(temp.data.node_id)
            else:
                print(temp.data.node_id, end=" --> ")
            temp = temp.next

    def unwind_data(self):
        temp = self.head

        data = []
        
        while temp:
            data.append(temp.data)
            temp = temp.next

        return data