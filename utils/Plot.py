# from Parser import Parser
import matplotlib.pyplot as plt
import numpy as np
import math
from Parser2 import Parser
class Plotter:
    def __init__(self,function:str,min_x:float,max_x:float):
        self.input_function = function
        self.min_x = min_x
        self.max_x = max_x
    def plot_function(self)->tuple:
        if self.min_x > self.max_x:
            raise Exception('x-min should be less than x-max')
        parser = Parser()
       
        try:
            parser.create_tree(self.input_function)
        except Exception as e:
            raise e
            
        y_values = []
        x_values = np.linspace(self.min_x,self.max_x)
        for x in x_values:
            try:
                y = parser.evaluate(x=x)
                y_values.append(y)
            except Exception as e:
                raise e

        return x_values,y_values

if __name__ == '__main__':
    pass       
            
        