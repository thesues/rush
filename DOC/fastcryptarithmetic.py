import re,string,itertools

def fastsolve(formula):
    f,letters = compile_formula(formula)
    for p in itertools.permutations([0,1,2,3,4,5,6,7,8,9],len(letters)):
        try:
            if f(*p) == True:
                table = string.maketrans(letters,"".join(map(str,p)))
                print formula.translate(table)
        except ArithmeticError:
            pass


def compile_formula(formula, verbose = False):
    """
    compile formula into a function, Also return letters found, as a str
    in the same order as params of function. For example 'YOU == ME ** 2' returns
    lamba Y,M,E,U,O : (U*1 + O*10 + Y*100) == (E*1 + M+10) ** 2, 'YMEUO' 
    param  str,bool
    return lambda, str
    """
    letters = set(re.findall(r"[A-Z]",formula))
    params = ",".join(letters)
    tokens = map(compile_word,re.split("([A-Z]+)",formula))
    body = "".join(tokens)
    f = "lambda %s: %s" % (params, body)
    return eval(f), "".join(map(str,letters))

def compile_word(word):
    """
    For example:
    "YOU"
    (U*1 + O*10 + Y*100)
    """
    if word.isupper():
        l = ["%d*%s" %  (10**i,c) for i,c in enumerate(word[::-1])]
        return '(' + "+".join(l) + ')'
    else:
        return word

fastsolve('DONALD+GERALD==ROBERT')
