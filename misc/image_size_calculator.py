"""A script to calculate a consistent image size 
based on aspect ratio for reports
"""

width_factor = 4
height_factor = 3
aspectratio = height_factor/width_factor


def calculate_left_margin(width, height):
    """Returns the left margin to be set for a centered image in inches"""
    area = width*height
    ratio = (area/(8.75**2*aspectratio))**0.5
    width_normalised = width/ratio
    return round((17.5-width_normalised))/2


def downscale_resolution(width, height, target_width=1920, target_height=1080):
    """Returns the resolution after downscaling to fill 1920 x 1080 window"""
    scaled_width = target_height/height * width
    scaled_height = target_width/width * height
    # Wider than target
    if scaled_width >= target_width:
        scaled_height = target_height
    # Taller than target
    elif scaled_height >= target_height:
        scaled_width = target_width
    return f"{scaled_width:.0f} {scaled_height:.0f}"


def main():
    # print(calculate_left_margin(401,192))
    print(downscale_resolution(1536,864))


if __name__ == "__main__":
    main()