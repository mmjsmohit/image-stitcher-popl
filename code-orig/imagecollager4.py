import os
import math
import time
import imageio
import numpy as np
from PIL import Image
from typing import List, Tuple
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()

class ImageShape(Enum):
    Rectangle = "Rectangle"
    Circle = "Circle"

class Size:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class ImagePositionAndSize:
    def __init__(self, sp: Tuple[int, int], size: Size):
        self.sp = sp
        self.size = size

class MyImage:
    def __init__(self, value: np.ndarray):
        self.value = value

    def set(self, x: int, y: int, c: Tuple[int, int, int]):
        self.value[y, x] = c

    def color_model(self):
        return "RGB"

    def bounds(self):
        return (0, 0, self.value.shape[1], self.value.shape[0])

    def at(self, x: int, y: int):
        return tuple(self.value[y, x])

class Circle:
    def __init__(self, p: Tuple[int, int], r: int):
        self.p = p
        self.r = r

    def color_model(self):
        return "L"

    def bounds(self):
        return (self.p[0] - self.r, self.p[1] - self.r, self.p[0] + self.r, self.p[1] + self.r)

    def at(self, x: int, y: int):
        xx, yy, rr = float(x - self.p[0]) + 0.5, float(y - self.p[1]) + 0.5, float(self.r)
        if xx * xx + yy * yy < rr * rr:
            return 255
        return 0

def width(i: Image) -> int:
    return i.size[0]

def height(i: Image) -> int:
    return i.size[1]

def draw_line(img: MyImage, line_width: int, space_from_end_x: int, space_from_end_y: int):
    for i in range(img.bounds()[2] - line_width - space_from_end_x, img.bounds()[2] - space_from_end_x):
        img.set(i, img.bounds()[3] - space_from_end_y, (255, 255, 255))

def draw_raw(bg_img: MyImage, inner_img: Image, sp: Tuple[int, int], width: int, height: int):
    resized_img = inner_img.resize((width, height), Image.LANCZOS)
    w = width
    h = height
    if sp[0] + w > bg_img.bounds()[2]:
        w = bg_img.bounds()[2] - sp[0]
    if sp[1] + h > bg_img.bounds()[3]:
        h = bg_img.bounds()[3] - sp[1]
    if w > 0 and h > 0:
        bg_img.value[sp[1]:sp[1] + h, sp[0]:sp[0] + w] = np.array(resized_img.crop((0, 0, w, h)))



def draw_in_circle(bg_img: MyImage, inner_img: Image, sp: Tuple[int, int], width: int, height: int, diameter: int):
    resized_img = inner_img.resize((width, height), Image.LANCZOS)
    r = diameter
    if r > width:
        r = width
    if r > height:
        r = height
    mask = Circle((width // 2, height // 2), r // 2)
    bg_img.value[sp[1]:sp[1] + height, sp[0]:sp[0] + width] = np.array(resized_img)

def make_image_collage(desired_width: int, desired_height: int, number_of_rows: int, shape: ImageShape, images: List[Image]) -> MyImage:

    # Sort images by height in descending order
    images.sort(key=lambda img: height(img), reverse=True)
    # Calculating num of col required
    number_of_columns = len(images) // number_of_rows

    # Creating a matrix to store images organized in rows
    images_matrix = []
    number_of_columns_added = 0
    max_number_of_columns = 0
    for idx in range(number_of_rows):
        columns_in_row = number_of_columns

        # Adjust columns in the last row if there are extra images
        if len(images) % number_of_rows > 0 and (number_of_rows - idx) * number_of_columns < len(images) - number_of_columns_added:
            columns_in_row += 1
        # Update the maximum number of columns
        if columns_in_row > max_number_of_columns:
            max_number_of_columns = columns_in_row
        # Appending images in the matrix for each row
        images_matrix.append(images[number_of_columns_added:number_of_columns_added + columns_in_row])
        number_of_columns_added += columns_in_row
    max_width = 0
    images_size = []

    # Calculate the width and height for each image in each row
    for row in range(number_of_rows):
        images_size.append([])
        calculated_width = math.floor(float(desired_width) / float(len(images_matrix[row])))
        row_width = 0
        row_height = 0
        for col in range(len(images_matrix[row])):
            original_width = width(images_matrix[row][col])
            original_height = height(images_matrix[row][col])
            resize_factor = calculated_width / original_width
            w = int(original_width * resize_factor)
            h = int(original_height * resize_factor)
            images_size[row].append(Size(w, h))
            if shape == ImageShape.Rectangle:
                row_width += w
            else:
                row_width += int(min(w, h) * 0.8)
            row_height += h
        # Update the maximum width for all rows
        if row_width > max_width:
            max_width = row_width
    max_height = 0

    # Calculate the maximum height for all columns
    for col in range(max_number_of_columns):
        col_height = 0
        for row in range(number_of_rows):
            if len(images_size[row]) > col:
                if shape == ImageShape.Rectangle:
                    col_height += images_size[row][col].height
                else:
                    col_height += int(min(images_size[row][col].height, images_size[row][col].width) * 0.8)
        # Update the maximum height
        if col_height > max_height:
            max_height = col_height

    # Call draw_images_on_background_in_parallel to create the collage
    output = draw_images_on_background_in_parallel(number_of_rows, shape, max_width, max_height, max_number_of_columns, images_matrix, desired_width)
    return output

def calculate_image_starting_point_and_size(img: Image, images_matrix: List[List[Image]], padding: int, desired_width: int, shape: ImageShape) -> Tuple[ImagePositionAndSize, Exception]:
    sp_y = padding
    for row in range(len(images_matrix)):
        sp_x = padding
        calculated_column_width = math.floor(float(desired_width) / float(len(images_matrix[row])))
        row_height = 0
        for col in range(len(images_matrix[row])):
            original_width = width(images_matrix[row][col])
            original_height = height(images_matrix[row][col])
            resize_factor = calculated_column_width / original_width
            w = int(original_width * resize_factor)
            h = int(original_height * resize_factor)
            if shape == ImageShape.Circle:
                w = int(min(w, h) * 0.8)
                h = w
            if images_matrix[row][col] == img:
                return ImagePositionAndSize((sp_x, sp_y), Size(w, h)), None
            else:
                sp_x += w + padding
            if h > row_height:
                row_height = h
        sp_y += row_height + padding
    return ImagePositionAndSize((-1, -1), Size(0, 0)), Exception("Image not found in matrix")

def draw_single_image_on_background(img: Image, images_matrix: List[List[Image]], padding: int, shape: ImageShape, desired_width: int, background: MyImage):
    image_details, _ = calculate_image_starting_point_and_size(img, images_matrix, padding, desired_width, shape)
    sp = image_details.sp
    size = image_details.size
    if shape == ImageShape.Rectangle:
        draw_raw(background, img, sp, size.width, size.height)
    else:
        draw_in_circle(background, img, sp, size.width, size.height, size.width)

def draw_images_on_background_in_parallel(number_of_rows: int, shape: ImageShape, max_width: int, max_height: int, max_number_of_columns: int, images_matrix: List[List[Image]], desired_width: int) -> MyImage:
    padding = 1
    if shape == ImageShape.Circle:
        padding = 20
    rectangle_end = (max_width + (max_number_of_columns - 1) * padding + 2 * padding, max_height + (number_of_rows - 1) * padding + 2 * padding)
    output = MyImage(np.zeros((rectangle_end[1], rectangle_end[0], 3), dtype=np.uint8))
    for r in range(len(images_matrix)):
        for c in range(len(images_matrix[r])):
            draw_single_image_on_background(images_matrix[r][c], images_matrix, padding, shape, desired_width, output)
    return output

def draw_images_on_background(number_of_rows: int, shape: ImageShape, desired_width: int, max_width: int, max_height: int, max_number_of_columns: int, images_matrix: List[List[Image]]) -> MyImage:
    padding = 1
    if shape == ImageShape.Circle:
        padding = 20
    rectangle_end = (max_width + (max_number_of_columns - 1) * padding + 2 * padding, max_height + (number_of_rows - 1) * padding + 2 * padding)
    output = MyImage(np.zeros((rectangle_end[1], rectangle_end[0], 3), dtype=np.uint8))
    sp_x, sp_y = 0, 0
    for row in range(number_of_rows):
        row_height = 0
        calculated_width = math.floor(float(desired_width) / float(len(images_matrix[row])))
        for col in range(len(images_matrix[row])):
            original_width = width(images_matrix[row][col])
            original_height = height(images_matrix[row][col])
            resize_factor = calculated_width / original_width
            w = int(original_width * resize_factor)
            h = int(original_height * resize_factor)
            if col == 0:
                sp_x = padding
            if row == 0:
                sp_y = padding
            sp = (sp_x, sp_y)
            if shape == ImageShape.Rectangle:
                draw_raw(output, images_matrix[row][col], sp, w, h)
            else:
                w = int(min(w, h) * 0.8)
                h = w
                draw_in_circle(output, images_matrix[row][col], sp, w, h, w)
            sp_x += w + padding
            if h > row_height:
                row_height = h
        sp_x = 0
        sp_y += row_height + padding
    return output

def load_image(path: str) -> Image:
    return Image.open(path)

def save_image(img: MyImage, filename: str):
    # Convert MyImage to a Pillow Image
    pillow_img = Image.fromarray(img.value)
    # Save the Pillow Image
    pillow_img.save(filename)


def main():

    exec_start = time.time()

    if len(os.sys.argv) != 6:
        raise Exception("Invalid script call. Should be in format `python imagecollager.py <Rectangle|Circle> <number of rows> <width> <height> <dir path>`")
    else:
        image_shape = ImageShape(os.sys.argv[1])
        number_of_rows = int(os.sys.argv[2])
        desired_width = int(os.sys.argv[3])
        desired_height = int(os.sys.argv[4])
        dir_path = os.sys.argv[5]
        images = []
        reading_images_start = time.time()
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
                images.append(load_image(os.path.join(dir_path, file_name)))
        reading_images_duration = time.time() - reading_images_start
        print(f"{len(images)} Images read in {reading_images_duration} seconds")

        collage_creation_start = time.time()
        output = make_image_collage(desired_width, desired_height, number_of_rows, image_shape, images)
        save_image(output, "output_image_py.jpg")
        collage_creation_duration = time.time() - collage_creation_start

        print(f"Image collage created in {collage_creation_duration} seconds")
        print(f"")
        print(f"")
        exec_duration = time.time() - exec_start
        print(f"Total execution time of the program in Python is {exec_duration} seconds")

if __name__ == "__main__":
    main()

profiler.stop()
profiler.print()