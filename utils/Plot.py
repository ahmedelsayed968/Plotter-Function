from Parser import Parser
import matplotlib.pyplot as plt
import numpy as np
class Plotter:
    def __init__(self,function,min_x,max_x):
        self.input_function = function
        self.min_x = min_x
        self.max_x = max_x
    def plot_function(self)->tuple:
        if self.min_x > self.max_x:
            raise Exception('x-min should be less than x-max')
        
        tree = Parser(self.input_function).get_function()
        y_values = []
        x_values = np.linspace(self.min_x,self.max_x)
        for x in x_values:
            try:
                y = eval(tree)
                y_values.append(y)
            except Exception as e:
                raise e

                    
        
        # plt.plot(x_values,y_values,'-o')
        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.title(f'Graph of {self.input_function}')
        # plt.show()
        return x_values,y_values

if __name__ == '__main__':
    # P = Plotter('5+x^4+5*3*x',0,6)
    # P.plot_function() 
    pass       
            
        