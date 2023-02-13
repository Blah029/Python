import math

def surface_eval(x,y):
    """return the z value corresponding to the given x,y values"""
    return math.sin(x)**2*math.cos(y)

data=open("data.txt") #open the data in read mode

for coordinate in data: #terate through each line
    values=list(map(float,coordinate.split(","))) #create a list of two floats containing x value and y value
    print("x:","%.4f"%values[0],"y:","%.4f"%values[1],"z:","%.4f"%surface_eval(values[0],values[1])) #output
