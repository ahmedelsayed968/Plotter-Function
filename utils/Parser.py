class InvalidInput(Exception):
    pass
class InvalidFunction(Exception):
    pass    
import math
class Parser:
    def __init__(self,function:str)->None:
        self.input_function = function
         
    def get_function(self):
        self.handle_input_function()
        try:
            tree = compile(f'{self.input_function}',filename='./',mode='eval')
        except :
            raise InvalidFunction('Invalid Input Function')
        return tree    
            
        
    def handle_input_function(self):
        self.input_function = self.input_function.lower().\
                                                replace('sin','math.sin').\
                                                replace('cos','math.cos').\
                                                replace('tan','math.tan').\
                                                replace('e','math.e').\
                                                replace('^','**')  
        
        
    def _is_sign(self,char)->bool:
        return char=='+' or char=='-' or char =='/' or char=='*' or char == '^'
if __name__ == '__main__':
    tree = Parser('sin(x)').get_function()
    print(tree)
    x = 2
    print(eval(tree))