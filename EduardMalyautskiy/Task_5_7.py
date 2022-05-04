"""
Run the module modules/mod_a.py. Check its result. Explain why does this happen. Try to change x to a list [1,2,3].
Explain the result. Try to change import to from x import * where x - module names. Explain the result.
"""

# python ../modules/mod_a.py
# >>> 1000
""" 
he result of runing module a will be 1000, because when importing module b, module c and its variable x = 6 are imported.
Then the variable is overwritten with the value 1000. This value is output when print(x) is executed.

Changing the value of x to [1,2,3] and the subsequent execution of print(x) outputs [1, 2, 3], 
because in the current namespace, the variable x will be overwritten with a new value.
"""