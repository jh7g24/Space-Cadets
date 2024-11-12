from PIL import Image
import numpy as np

FILENAME = "red_circle.png"

def load_image(filename):
    global im
    try:
        im = Image.open(filename)
    except IOError:
        return None

def get_pixel_data():
    pixels = list(im.getdata())
    print(pixels)
    #width, height = im.size
    #pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return pixels

def get_image_dimensions():
    return im.size

def rgb_to_grey(pixels, mode=1):
    # 1: average method
    # 2: weighted average method
    # 3: luminoisty method
    grey_pixels = []
    for row in pixels:
        grey_row = []
        for pixel in row:
            match mode:
                case 1:
                    grey_pixel = average_method(pixel)
                case 2:
                    grey_pixel = weighted_average_method(pixel)
                case 3:
                    grey_pixel = luminosity_method(pixel)
                case _:
                    raise ValueError("Invalid mode for greyscale conversion")
            grey_row.append(grey_pixel)
        grey_pixels.append(grey_row)
    return grey_pixels


def average_method(pixel):
    avg = (pixel[0] + pixel[1] + pixel[2]) / 3
    return (avg, avg, avg, pixel[3])


def weighted_average_method(pixel):
    # Y = 0.299×R + 0.587×G + 0.114×B
    Y = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.144 * pixel[2]
    return (Y, Y, Y, pixel[3])


def luminosity_method(pixel):
    # Z=0.2126R+0.7152G+0.0722B
    Z = 0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2]
    return (Z, Z, Z, pixel[3])

def save_image(name, pixels):
    new_img = Image.fromarray(np.asarray(pixels, dtype=np.uint8), "RGB")
    new_img.save(name + ".png", "PNG")



def main():
    load_image(FILENAME)
    pixels = get_pixel_data()
    grey_pixels = rgb_to_grey(pixels)
    save_image("output", pixels)

if __name__ == "__main__":
    main()
