# coding=utf-8
#设置编码，utf-8可支持中英文

def add_and_multiply(x, y):
    addition = x + y
    multiple = multiply(x, y)
    return (addition, multiple)


def multiply(x, y):
    return x * y+3