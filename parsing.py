from pyparsing import *

from entities import *

class KnapsackParser():
    
    '''
    Parses a text containing a representation of entity Knapsack
    according to the grammar defined in 'knapsack-grammar.bnf'
    '''

    def parse_items( self, tokens ):
        name, weight, value = tokens[0]
        return Item(name=name, weight=weight, value=value)

    def parse_knapsack( self, tokens ):

        capacity, items = tokens

        knapsack = Knapsack(capacity)
        for item in items:
            knapsack.add_item(item)

        return knapsack

    def __init__(self):
        '''
        Defines grammar rules
        '''

        # define the tokens for each element of the grammar
        name = QuotedString("'")
        
        weight = pyparsing_common.integer()
        value = pyparsing_common.integer()
        
        # define the item elements
        item = Group(Suppress("(") +
                        name + 
                        Suppress(", w=") + 
                        weight + 
                        Suppress(", v=") + 
                        value + 
                        Suppress(")")).setParseAction(self.parse_items)

        # define the item_list element
        item_list = Suppress("items=(") + \
                        Group( OneOrMore(item + Optional(",").suppress() ) ).setResultsName("items")+ \
                        Suppress(")")

        # define the capacity element
        capacity = Suppress("capacity=") + \
                        pyparsing_common.number().setResultsName("capacity")

        # define the expression element
        self.root = Suppress("Knapsack(") + \
                        capacity + Suppress(",") + \
                        item_list + Suppress(")")

        self.root.setParseAction(self.parse_knapsack)

        
    def from_string(self, repr: str) -> Knapsack:
        '''
        Parses the string passed as parameter, returns an instance of 
        entities.Knapsack
        '''
        return self.root.parseString(repr)[0]

    def from_file(self, filename: str):
        '''
        Reads the context of the given filename and parses it with 
        self.parse_string
        '''
        with open(filename, "r") as file:
            repr = file.read().strip()
            return self.root.parseString(repr)[0]
