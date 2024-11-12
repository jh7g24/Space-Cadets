from PIL import Image
import numpy as np
import math

FILENAME = "red_circle.png"
GREY_NAME = "grey_output"
SOBEL_NAME = "sobel_output"
OUTPUT_NAME = "output"
RGBA = True
if RGBA:
    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 255)
    BLUE = (0, 255, 0, 255)
else:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 255, 0)


def load_image(filename):
    global im
    try:
        im = Image.open(filename)
    except IOError:
        return None


def get_pixel_data():
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
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
    if RGBA:
        return (avg, avg, avg, pixel[3])
    else:
        return (avg, avg, avg)


def weighted_average_method(pixel):
    # Y = 0.299×R + 0.587×G + 0.114×B
    Y = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.144 * pixel[2]
    return (Y, Y, Y, pixel[3])


def luminosity_method(pixel):
    # Z=0.2126R+0.7152G+0.0722B
    Z = 0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2]
    return (Z, Z, Z, pixel[3])


def sobel(grey_pixels):
    sobel_pixels = []
    kernels = [
        [
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ],
        [
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ]
    ]
    for row in range(len(grey_pixels)):
        sobel_row = []
        for col in range(len(grey_pixels[0])):
            Gxy = []
            for i in range(2):
                total = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= row + dx <= (len(grey_pixels) - 1):
                            if 0 <= col + dy <= (len(grey_pixels[0]) - 1):
                                total += grey_pixels[row + dx][col + dy][0] * kernels[i][1 + dx][1 + dy]
                Gxy.append(total)
            G = math.sqrt((Gxy[0] ** 2) + (Gxy[1] ** 2))
            if RGBA:
                sobel_pixel = (G, G, G, grey_pixels[row][col][3])
            else:
                sobel_pixel = (G, G, G)
            sobel_row.append(sobel_pixel)
        sobel_pixels.append(sobel_row)

    return sobel_pixels


def hough(sobel_pixels):
    threshold = 300
    edge_pixels_coords = []
    for row in range(len(sobel_pixels)):
        for col in range(len(sobel_pixels[0])):
            if sobel_pixels[row][col][0] > threshold:
                edge_pixels_coords.append((row, col))


    #best_fits = []
    #for radius in range(len(sobel_pixels) // 4, len(sobel_pixels) // 2):
    radius = 2600 // 12
    votes = np.zeros((len(sobel_pixels[0]), len(sobel_pixels)))
    for coord in edge_pixels_coords:
        for x in range(coord[0] - radius, coord[0] + radius):
            y1, y2 = calculate_circle_ys(coord, radius, x)
            if 0 <= x < len(sobel_pixels[0]):
                if 0 <= y1 < len(sobel_pixels):
                    votes[x][y1] += 1
                if 0 <= y2 < len(sobel_pixels):
                    votes[x][y2] += 1

    row_maxes = []
    for row in votes:
        max = 0
        max_index = 0
        for col in range(len(row)):
            if row[col] > max:
                max = row[col]
                max_index = col
        row_maxes.append((max, max_index))

    max = 0
    max_index = 0
    for i in range(len(row_maxes)):
        if row_maxes[i][0] > max:
            max = row_maxes[i][0]
            max_index = i
    """
    best_fits.append((max, (max_index, row_maxes[max_index][1]), radius))

    best_score = -99999999999
    best_fit = None
    for element in best_fits:
        if element[0] > best_score:
            best_score = element[0]
            best_fit = element

    return best_fit[1], best_fit[2]"""
    return (max_index, row_maxes[max_index][1]), radius


def calculate_circle_ys(center, radius, x):
    y1 = int(math.sqrt((radius ** 2) - ((x - center[0]) ** 2)) + center[1])
    y2 = center[0] - abs(y1 - center[0])
    return y1, y2


def draw_circle(pixels, center, radius, thickness, color=GREEN):
    if thickness != 0:
        pixels = draw_circle(pixels, center,thickness, 0)
    for x in range(center[0] - radius, center[0] + radius):
        if 0 <= x < len(pixels):
            y1, y2 = calculate_circle_ys(center, radius, x)
            if 0<= y1 < len(pixels[0]):
                if thickness != 0:
                    pixels = draw_circle(pixels, (x, y1), thickness, 0)
                else:
                    pixels[x][y1] = color
            if 0 <= y2 < len(pixels[0]):
                if thickness != 0:
                    pixels = draw_circle(pixels, (x, y2), thickness, 0)
                else:
                    pixels[x][y2] = color
    return pixels


def save_image(name, pixels):
    if RGBA:
        new_img = Image.fromarray(np.asarray(pixels, dtype=np.uint8), "RGBA")
    else:
        new_img = Image.fromarray(np.asarray(pixels, dtype=np.uint8), "RGB")
    new_img.save(name + ".png", "PNG")


def main():
    load_image(FILENAME)
    print("Image loaded")
    pixels = get_pixel_data()
    print("Pixel data extracted")
    grey_pixels = rgb_to_grey(pixels)
    save_image(GREY_NAME, grey_pixels)
    print("Greyscale conversion complete")
    sobel_pixels = sobel(grey_pixels)
    save_image(SOBEL_NAME, sobel_pixels)
    print("Sobel operator applied")
    center, radius = hough(sobel_pixels)
    print("Hough Transform complete, center of 'best' circle =", center)
    output_pixels = draw_circle(pixels, center, radius, 5)
    print("Circle drawn")
    save_image(OUTPUT_NAME, output_pixels)
    print("Output image saved")


if __name__ == "__main__":
    main()
