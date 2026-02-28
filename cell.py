
class Cell():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
    def __eq__(self, other):
        return (self.row == other.row) and (self.col == other.col)
    
    def __ne__(self, other):
        return (self.row != other.row) or (self.col != other.col)
    
    def __str__(self):
        return f"({self.row},{self.col})"
    
    def __hash__(self):
        return hash(str(self))