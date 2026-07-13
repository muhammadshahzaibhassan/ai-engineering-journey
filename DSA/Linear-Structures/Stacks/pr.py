# Last in, last out, or STACK
def c():
    print("I am C")
    print("Function C ran")
def b():
    c()
    print("Function B ran")
def a():
    b()
    print("Function A ran")

a()