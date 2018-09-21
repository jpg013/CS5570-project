import random

class Transaction:
  """ Transaction class """
  
  # Stores the list of (1 - 2 / data item) data operations (read/write) for the transaction
  data_operations = []
  
  # Stores the list of (1 - 4) data items (1, 2, 3, 4) for the transaction
  data_items = []

  # Flag to determine whether or not the transaction commits after completes.
  # If false, this means the transaction will abort after data operations.
  commit_on_complete = True
  
  def __init__(self):
    # Generate random data item count for transaction
    self.data_item_count = random.randint(1,4)  
  
  def generate_rando_data_item_count(self):
    self.data_item_count = random.randint(1,4)  
  
  def make_data_items(self):
    # make "n" number of unique data itmes and add to the data_items list
    
    if (self.data_item_count < 1 or self.data_item_count > 4):
      self.generate_rando_data_item_count()

    while len(self.data_items) < self.data_item_count:
      data = random.randint(1, 100) # Generate random data item number between 1 - 100 
      if data not in self.data_items:
        self.data_items.append(data)
    
    # Sort the data items ascending
    self.data_items.sort()