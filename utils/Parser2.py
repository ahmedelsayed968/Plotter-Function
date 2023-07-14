import re
from enum import Enum
import math

class Type(Enum):
    NUMBER = 1
    CONSTANT = 2
    FUNCTION = 3
    OPERATOR = 4
    VARIABLE = 5


class Parser:
    SIGN_LEVEL1 = '^'
    SIGN_LEVEL2 = ['/','*']
    SIGN_LEVEL3 = ['+','-']
    
    def __init__(self,in_num_variables):
        self.in_num_variables:int = in_num_variables
        self.found_variables:set = None
        self.Tree:self.__Node            = None
    
    
    class __Node:
        def __init__(self,left,value,right,type_):
            self.value = value
            self.right = right
            self.left = left
            self.type = type_
            
    def create_tree(self,expression:str):
        # convert the string into tokens and create the tree
        try:
            TK = Tokenizer()
            tokens = TK.tokenize(expression=expression)
        except Exception as e:
            raise e
        
        self.found_variables = TK.variables
        if self.in_num_variables != len(self.found_variables):
            raise ValueError('number of variables is not valid')
        
        st_nodes = []
        st_operation = []
        for token in tokens:
            value,class_ = token
            if class_ == Type.VARIABLE or class_ == Type.CONSTANT or class_ ==Type.NUMBER or class_ == Type.FUNCTION:
                if class_ == Type.NUMBER:
                    st_nodes.append(self.__Node(None,float(value),None,class_))
                else:
                    st_nodes.append(self.__Node(None,value,None,class_))
                        
            elif class_ == Type.OPERATOR and value != ')':
                while   len(st_nodes) >= 2 and \
                        st_operation and \
                        value != '(' and\
                        st_operation[-1] != '(' and\
                        self._sign_is_bigger(st_operation[-1],value):
                    right = st_nodes.pop()
                    left = st_nodes.pop()
                    node_value = st_operation[-1]
                    type_ = Type.OPERATOR
                    calNode = self.__Node(left,node_value,right,type_)
                    st_operation.pop()
                    st_nodes.append(calNode)
                    
                st_operation.append(value)
                    
            elif class_==Type.OPERATOR and value== ')':
                while len(st_nodes)>=2 and st_operation and st_operation[-1] != '(':
                    right = st_nodes.pop()
                    left = st_nodes.pop()
                    node_value = st_operation[-1]
                    type_ = Type.OPERATOR
                    calNode = self.__Node(left,node_value,right,type_)
                    st_nodes.append(calNode)
                    st_operation.pop()
                if st_operation:
                    st_operation.pop()

                # handle functions while building the tree
                # if the 2nd last element in the stack is function [sin,cos,tan]
                # then we have to make left branch of that node contain the value inside the () which is the last element in the stack
                if len(st_nodes)>=2 and st_nodes[-2].type == Type.FUNCTION and not st_nodes[-2].left:
                    st_nodes[-2].left = st_nodes[-1]
                    st_nodes.pop()
        while st_operation and st_nodes:
            right = st_nodes.pop()
            left = st_nodes.pop()
            node_value = st_operation[-1]
            type_ = Type.OPERATOR
            st_nodes.append(Parser.__Node(left,node_value,right,type_))
            st_operation.pop()
            
        
        if len(st_nodes) == 1:
            self.Tree = st_nodes[-1]
        else:
            raise ValueError('Invalid Expression')
        
    def evaluate(self,**kargs):
        """"
            :kargs: dict of the variables' values to evaluate 
        """
        if (self.found_variables and len(kargs) != len(self.found_variables)) or not self.Tree:
            return False
        
        return self._helper_evaluate(self.Tree,kargs)
            
    def _helper_evaluate(self,root,kargs):        
        if not root:
            return 0
        if root.type == Type.OPERATOR:
            if root.value == '+':
                return self._helper_evaluate(root.left,kargs)+ self._helper_evaluate(root.right,kargs)
            elif root.value == '-':
                return self._helper_evaluate(root.left,kargs)- self._helper_evaluate(root.right,kargs)
            elif root.value == '*':
                return self._helper_evaluate(root.left,kargs)* self._helper_evaluate(root.right,kargs)
            elif root.value == '^':
                return self._helper_evaluate(root.left,kargs)** self._helper_evaluate(root.right,kargs)
            elif root.value == '/':
                return self._helper_evaluate(root.left,kargs)/ self._helper_evaluate(root.right,kargs)
        elif root.type == Type.CONSTANT:
            if root.value == 'e':
                return math.e
        elif root.type == Type.NUMBER:
            return root.value
        elif root.type == Type.VARIABLE:
            return kargs[root.value]
        elif root.type == Type.FUNCTION:
            if root.value == 'sin':
                return math.sin(self._helper_evaluate(root.left,kargs))
            elif root.value == 'tan':
                return math.tan(self._helper_evaluate(root.left,kargs))
            elif root.value == 'cos':
                return math.cos(self._helper_evaluate(root.left,kargs))            
        
                        

    
    def _sign_is_bigger(self,s1,s2):
        if s2 == Parser.SIGN_LEVEL1 and s1 != Parser.SIGN_LEVEL1:
            return False
        if s1 == Parser.SIGN_LEVEL1:
            return True
        elif s1 in Parser.SIGN_LEVEL2 and  s2 in Parser.SIGN_LEVEL3:
            return True
        elif s1 in Parser.SIGN_LEVEL3 and s2 not in Parser.SIGN_LEVEL3:
            return False
        return True
    


    
class Tokenizer:
    token_patterns = [
        (r'\d+(\.\d*)?|\.\d+', Type.NUMBER),    # match decimal numbers
        (r'sin|cos|tan', Type.FUNCTION),        # match function names
        (r'e',Type.CONSTANT),
        (r'[a-zA-Z]+', Type.VARIABLE),          # match variables
        (r'[+\-*/^(),]',Type.OPERATOR)          # match operators and parentheses
        
    ]
    def __init__(self) -> None:
        self.variables = set()
        
    def tokenize(self,expression):
        tokens = []
        while len(expression) > 0:
            match = None
            for pattern, token_type in Tokenizer.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(expression)
                if match:
                    token = match.group(0)
                    tokens.append((token, token_type))
                    if token_type== Type.VARIABLE and token not in self.variables:
                        self.variables.add(token)
                    expression = expression[match.end():].lstrip()
                    break
            if not match:
                raise ValueError(f'Invalid token in expression: {expression}')
        return tokens
    
if __name__ == '__main__':
    # Tk = Tokenizer()
    # tokens = Tk.tokenize('3*x + sin(y) / (4 - z)+cos(x)+tan(x)*e^t')
    # print(tokens)
    # print(Tk.variables)
    # print(Parser(4)._sign_is_bigger('*','+'))
    # tree = Parser(4).create_tree('3*x + sin(y) / (4 - z)+cos(x)+tan(x)*e^t')
    
    tree = Parser(4)
    tree.create_tree('3*x + sin(y) / (4 - z)+cos(x)+tan(x)*e^t')
    print(tree.evaluate(x=1,y=0,z=1,t=0))
    # print(Parser()._sign_is_bigger('^','/'))