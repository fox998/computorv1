import pylab
import numpy


class Polynomial:
    
    def __init__(self, *coefficients):
        """ input: coefficients are in the form a_n, ...a_1, a_0 
        """
        # for reasons of efficiency we save the coefficients in reverse order,
        # i.e. a_0, a_1, ... a_n
        self.coefficients = coefficients[::-1] # tuple is also turned into list

    def __call__(self, x):    
        res = 0
        for index, coeff in enumerate(self.coefficients):
            res += coeff * x** index
        return res  

def graph(index_arr):
    x = numpy.linspace(-5,5) # 100 linearly spaced numbers
    p1 = Polynomial(*index_arr)
    F1 = p1(x)
    # compose plot
    pylab.plot(x, F1, label="F1")
    
    pylab.grid()
    pylab.show() # show the plot

if __name__ == "__main__":
    graph([1, 1, 1])
