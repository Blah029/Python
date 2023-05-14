'''A test module containig one fuction to examine the use of doctests'''

import doctest

def maxNum(num1,num2):
    """
    Returns the highest number, if the two are not equal

    >>> maxNum(0,10)
    10
    >>> maxNum(1,0)
    1
    >>> maxNum(55,10)
    55
    >>> maxNum(15,15)
    'both are equal'
    >>>
    """

    if num1==num2:
        return "both are equal"
    else:
        return max(num1,num2)

if __name__=="__main__":
    doctest.testmod(verbose=True)
