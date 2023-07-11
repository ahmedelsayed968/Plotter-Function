
class Parser:
    class Variable:
        def __init__(self,coff:int,power:int)->None:
            self.coff = coff
            self.power = power
        def get_value(self,x:int)->int:
            return  self.coff * x **self.power 

    def __init__(self,function:str)->None:
        self.input_function = function
         
    def get_function(self)->list:
        valid = self._check_function()
        if not valid:
            raise Exception('invalid Input')
        else:
            print('valid!')
            
            
            
        
    
    def _check_function(self)->bool:
        st = []
        for char in self.input_function:
            if len(st) == 0:
                st.append(char)
                continue
            
            if self._is_sign(st[-1]) and self._is_sign(char):
                return False
            if char == 'x' and not self._is_sign(st[-1]):
                return False
            if char.isdigit() and st[-1] == 'x':
                return False
            if char == 'x' and st[-1] == 'x':
                return False
            st.append(char)
        if self._is_sign(st[-1]):
            return False    
        return True        
    
    def _is_sign(self,char)->bool:
        return char=='+' or char=='-' or char =='/' or char=='*' or char == '^'
        
        
        
if __name__ == '__main__':
    p = Parser('5+x*3-x^x^3^3*2/2-1')
    func = p.get_function()