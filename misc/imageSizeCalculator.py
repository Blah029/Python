"""A script to calculate a consistent image size based on aspect ratio for reports"""

normalWidth = 4
normalHeight = 3
normalAspectRatio = normalHeight/normalWidth


def calculateLeftMargin(width, height):
    """Returns the left margin to be set for a centered image in inches"""
    area = width*height
    ratio = (area/(8.75**2*normalAspectRatio))**0.5
    normalisedWidth = width/ratio
    return round((17.5-normalisedWidth))/2


def main():
    print(calculateLeftMargin(4,3))


if __name__ == "__main__":
    main()