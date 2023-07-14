import re
from enum import Enum
import math
class InvalidOperation(Exception):
    pass
class InvalidFunction(Exception):
    pass
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
    
    def __init__(self):
        self.found_variables:set = None
        self.Tree:self.__Node    = None
    
    
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
                        self.__sign_is_bigger(st_operation[-1],value):
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
        while st_operation and st_nodes and len(st_nodes) >=2:
            right = st_nodes.pop()
            left = st_nodes.pop()
            node_value = st_operation[-1]
            type_ = Type.OPERATOR
            st_nodes.append(Parser.__Node(left,node_value,right,type_))
            st_operation.pop()
            
        if len(st_nodes) == 1 and not st_operation:
            self.Tree = st_nodes[-1]
        else:
            raise ValueError('Invalid Expression')
        
    def evaluate(self,**kargs):
        """"
            :kargs: dict of the variables' values to evaluate 
        """
        if not self.Tree:
            raise Exception('Tree Not Found To Evaluate')
        
        return self.__helper_evaluate(self.Tree,kargs)
    
    def __helper_evaluate(self,root,kargs):        
        if not root:
            return 0
        if root.type == Type.OPERATOR:
            return self.__handle_basic_operation(root,kargs)
        elif root.type == Type.CONSTANT:
            if root.value == 'e':
                return math.e
        elif root.type == Type.NUMBER:
            return root.value
        elif root.type == Type.VARIABLE:
            if root.value not in kargs.keys():
                raise Exception(f'Do Not Have value for {root.value}')
            return kargs[root.value]
        elif root.type == Type.FUNCTION:
            return self.__handle_functions(root,kargs)
        
    def __handle_basic_operation(self,root,kargs):
            if root.value == '+':
                return self.__helper_evaluate(root.left,kargs)+ self.__helper_evaluate(root.right,kargs)
            elif root.value == '-':
                return self.__helper_evaluate(root.left,kargs)- self.__helper_evaluate(root.right,kargs)
            elif root.value == '*':
                return self.__helper_evaluate(root.left,kargs)* self.__helper_evaluate(root.right,kargs)
            elif root.value == '^':
                return self.__helper_evaluate(root.left,kargs)** self.__helper_evaluate(root.right,kargs)
            elif root.value == '/':
                return self.__helper_evaluate(root.left,kargs)/ self.__helper_evaluate(root.right,kargs)
            else:
                raise InvalidOperation('Operation Not Supported')                         
    
    def __handle_functions(self,root,kargs):
            if root.value == 'sin':
                return math.sin(self.__helper_evaluate(root.left,kargs))
            elif root.value == 'tan':
                return math.tan(self.__helper_evaluate(root.left,kargs))
            elif root.value == 'cos':
                return math.cos(self.__helper_evaluate(root.left,kargs))
            else:
                raise InvalidFunction('Function Not Supported')   

    def __sign_is_bigger(self,s1,s2):
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
        (r'x*', Type.VARIABLE),                 # match variables
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
                    if not token:
                        match = None
                    else:
                        tokens.append((token, token_type))
                        if token_type== Type.VARIABLE and token not in self.variables:
                            self.variables.add(token)
                        expression = expression[match.end():].lstrip()
                        break
            if not match:
                raise ValueError(f'Invalid token in expression: {expression}')
        return tokens
    
if __name__ == '__main__':
    p = Parser()
    p.create_tree('11+5+11+10')
    print(p.evaluate(x=1))