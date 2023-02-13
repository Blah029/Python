import math

refArea = 54.1875 #landscape 4:3, 8.5 inch horizontal


def resize(width,height):
    global refArea
    aspRatio = width/height
    print(round(math.sqrt(refArea*aspRatio)*2,0)/2)
    return round((17.5-math.sqrt(refArea*aspRatio)))/2


def main():
    print(resize(4000,1087))


if __name__ == "__main__":
    main()