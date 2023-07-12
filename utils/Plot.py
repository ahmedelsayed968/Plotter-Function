from Parser import Parser
import matplotlib.pyplot as plt
import numpy as np
import math
class Plotter:
    def __init__(self,function:str,min_x:float,max_x:float):
        self.input_function = function
        self.min_x = min_x
        self.max_x = max_x
    def plot_function(self)->tuple:
        if self.min_x > self.max_x:
            raise Exception('x-min should be less than x-max')
        tree = Parser(self.input_function).get_function()
        y_values = []
        x_values = np.linspace(round(self.min_x,2),round(self.max_x,2))
        for x in x_values:
            try:
                y = eval(tree)
                y_values.append(round(y,2))
            except Exception as e:
                raise e

        return x_values,y_values

if __name__ == '__main__':
    pass       
            
        