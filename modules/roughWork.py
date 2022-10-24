def expand(array):
    """Print items of array line by line"""
    if str(type(array)) == "<class 'list'>" or str(type(array)) == "<class 'tuple'>":
        for item in array:
            print(item)
    elif str(type(array)) == "<class 'dict'>":
        for item in array:
            print(item,": ",array[item], sep="")
    else:
        print("Error: function 'expand' is not defined for",type(array))
