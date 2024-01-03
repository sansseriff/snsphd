import inspect
import re

# from: https://stackoverflow.com/questions/32000934/python-print-a-variables-name-and-value
def prinfo(*args):
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search(r"\((.*)\)", s).group(1)
    vnames = r.split(", ")
    for i,(var,val) in enumerate(zip(vnames, args)):
        print(f"{var} = {val}")
        
