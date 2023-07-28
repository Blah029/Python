"""A script to calculate a consistent image size based on aspect ratio for reports"""

width_factor = 4
height_factor = 3
aspectratio = height_factor/width_factor


def calculate_left_margin(width, height):
    """Returns the left margin to be set for a centered image in inches"""
    area = width*height
    ratio = (area/(8.75**2*aspectratio))**0.5
    width_normalised = width/ratio
    return round((17.5-width_normalised))/2


def main():
    print(calculate_left_margin(401,192))


if __name__ == "__main__":
    main()