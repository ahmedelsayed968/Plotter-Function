import sys
import pytest
import math
sys.path.append('utils')
from Parser2 import Parser,Tokenizer

def test_tokenizer_invalid_inputs() :
    tk = Tokenizer()
    with pytest.raises(ValueError) as e_info:
        tk.tokenize('%+1+1+ctan')
    with pytest.raises(ValueError) as e_info:
        tk.tokenize('%+1+1+ccos')
    with pytest.raises(ValueError) as e_info:
        tk.tokenize('%+1+1+csin')
    with pytest.raises(ValueError) as e_info:
        tk.tokenize('%+1+1+wsin')
        
        
def test_tokenizer_valid_inputs():
    tk = Tokenizer()
    tk.tokenize('1+1+sin(x)+tan(x)+1')
    assert True
    tk.tokenize('1+1+sin(x)+tan(x)+cos(x)+tan(x)')
    assert True
    tk.tokenize('1+1+sin(x)+e+cos(x)*tan(x)')
    assert True

def test_sign_checker():
    p = Parser()

    assert p._Parser__sign_is_bigger('^','^')==True
    assert p._Parser__sign_is_bigger('^','*')==True
    assert p._Parser__sign_is_bigger('^','/')==True
    assert p._Parser__sign_is_bigger('^','+')==True
    assert p._Parser__sign_is_bigger('^','-')==True
    
    assert p._Parser__sign_is_bigger('*','*')==True
    assert p._Parser__sign_is_bigger('*','/')==True
    assert p._Parser__sign_is_bigger('*','+')==True
    assert p._Parser__sign_is_bigger('*','-')==True
    
    assert p._Parser__sign_is_bigger('/','*')==True
    assert p._Parser__sign_is_bigger('/','/')==True
    assert p._Parser__sign_is_bigger('/','+')==True
    assert p._Parser__sign_is_bigger('/','-')==True

    assert p._Parser__sign_is_bigger('+','+')==True
    assert p._Parser__sign_is_bigger('+','-')==True
    

    assert p._Parser__sign_is_bigger('*','^')==False
    assert p._Parser__sign_is_bigger('/','^')==False
    assert p._Parser__sign_is_bigger('+','^')==False
    assert p._Parser__sign_is_bigger('-','^')==False
    

    assert p._Parser__sign_is_bigger('+','*')==False
    assert p._Parser__sign_is_bigger('-','*')==False

    
def test_create_tree_invalid_expression():
    p = Parser()
    with pytest.raises(ValueError) as e:
        p.create_tree('%%+1+1+ctan')

def test_create_tres_invalid_methametical_expression():
    p = Parser()
    with pytest.raises(ValueError) as e:
        p.create_tree('x+')
    with pytest.raises(ValueError) as e:
        p.create_tree('x+x**x')
        
    with pytest.raises(ValueError) as e:
        p.create_tree('x+x++/*-1x')
        
    with pytest.raises(ValueError) as e:
        p.create_tree('x/*x')
    
    with pytest.raises(ValueError) as e:
        p.create_tree('x/*xsin2')
        
    with pytest.raises(ValueError) as e:
        p.create_tree('x/*xcos3')
    
    with pytest.raises(ValueError) as e:
        p.create_tree('1/x+sin')

def test_create_tree_valid_inputs():
    p = Parser()
    assert p.create_tree('1+1') == None
    assert p.create_tree('1+1+x') == None
    assert p.create_tree('1+1+sin(x)') == None
    assert p.create_tree('1+1+tan(x)+cos(x)*e') == None
    assert p.create_tree('1+1+e^3+x') == None

def test_evaluation():
    p = Parser()
    p.create_tree('1+1')
    assert p.evaluate(x=1) == float(2)
    
    p.create_tree('1+x+x*x')
    assert p.evaluate(x=1) == float(1+1+1*1)
    
    p.create_tree('1+x+x*x+e^x')
    assert p.evaluate(x=5) == float(1+5+5*5+math.e**5)
    
    
    p.create_tree('1/(x+e^x)')
    assert p.evaluate(x=5) == float(1/(5+math.e**5))
    
    
    p.create_tree('1/(x+e^x)+sin(x^3)')
    assert p.evaluate(x=5) == float(1/(5+math.e**5)+math.sin(5**3))
    
    p.create_tree('1/x')
    with pytest.raises(ZeroDivisionError) as e:
        p.evaluate(x=0)
    