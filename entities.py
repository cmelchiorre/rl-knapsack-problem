
ITEM_NAMES = [
    'sleeping_bag', 'stove', 'matches', 'flashlight', 'water_bottle', 
    'food', 'first_aid_kit', 'towel', 'extra_clothes', 'hat', 
    'sunglasses', 'sunscreen', 'bug_spray', 'pocket_knife', 'multi_tool', 
    'compass', 'camping_chair', 'camping_light', 'camping_knife', 
    'camping_spoon', 'camping_fork', 'pot', 'pan', 'plate', 'bowl', 'mug', 
    'map', 'whistle', 'mirror'
]


class Item():

    def __init__( self, name:str, weight: int, value: float ):
        self.name = name
        self.weight = weight
        self.value = value

    def to_repr( self):
        return f"('{self.name}', w={self.weight}, v={self.value})"


class Knapsack():
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item( self, item ):
        self.items.append( item )

    def add_item( self, name:str, weight: int, value: float ):
        self.items.append ( Item(name, weight, value ))

    def add_item( self, item: Item ):
        self.items.append ( item )

    def to_repr(self):
        
        repr = "Knapsack( \n" + \
        f"\tcapacity={self.capacity}, \n" + \
        f"\titems=(\n"
        
        for i, item in enumerate(self.items):
            repr += "\t\t" + item.to_repr()
            if i < len(self.items) - 1:
                repr += ","
            repr += "\n"

        repr += "\t)\n)"
        return repr
