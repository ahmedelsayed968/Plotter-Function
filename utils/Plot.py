from Parser import Parser
import matplotlib.pyplot as plt
class Plotter:
    def __init__(self,function,min_x,max_x):
        self.input_function = function
        self.min_x = min_x
        self.max_x = max_x
    def plot_function(self):
        tree = Parser(self.input_function).get_function()
        y_values = []
        x_values = list(range(self.min_x,self.max_x+1))
        for x in x_values:
            y = eval(tree)
            y_values.append(y)
        
        plt.plot(x_values,y_values,'-o')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Graph of {self.input_function}')
        plt.show()

if __name__ == '__main__':
    P = Plotter('5+x^4+5*3*x',0,6)
    P.plot_function()        
            
        