import numpy as np
import cv2
from PIL import Image, ImageOps, ImageDraw
from sklearn.cluster import KMeans
from app import (
    lower_range_hsv, upper_range_hsv, resolution, soil_width, start_height,
    black_area, black_ratio, matrix_flow_depth, priority_flow_percentage,
    priority_staining_area, maximum_staining_depth, length_index
)

def parse_resolution(resolution_str):
    if resolution_str:
        try:
            width, height = map(int, resolution_str.lower().split('x'))
            return width, height
        except ValueError:
            print("解析分辨率失败，使用默认500x500")
    return 500, 500  # 默认分辨率

def resize_image(img_pil, resolution):
    width, height = parse_resolution(resolution)
    return img_pil.resize((width, height), Image.LANCZOS)

def is_grayscale_image(img_pil):
    img_array = np.array(img_pil.convert("L"))
    total_pixels = img_array.size
    black_threshold = 20
    white_threshold = 200
    black_pixels = np.sum(img_array <= black_threshold)
    white_pixels = np.sum(img_array >= white_threshold)
    black_ratio = black_pixels / total_pixels
    white_ratio = white_pixels / total_pixels
    if black_ratio > 0.3 or white_ratio > 0.3:
        print(f"黑色比例: {black_ratio:.2f}, 白色比例: {white_ratio:.2f} - 跳过颜色处理")
        return True
    return False

def black_white_processing(img_pil, resolution):
    img_resized = resize_image(img_pil, resolution)
    img_cv = np.array(img_resized)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
    hsv_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    if len(lower_range_hsv) != 3 and len(upper_range_hsv) != 3:
        raise ValueError("lower_range和upper_range必须是长度为3的列表或数组")
    mask = cv2.inRange(hsv_img, np.array(lower_range_hsv), np.array(upper_range_hsv))
    stain_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    inverted_mask = cv2.bitwise_not(mask)
    mask_rgb = cv2.cvtColor(inverted_mask, cv2.COLOR_GRAY2RGB)
    img_pil = Image.fromarray(mask_rgb)
    return img_pil

def calculate_black_area_ratio(img_pil):
    img = np.array(img_pil.convert("L"))
    total_pixels = img.size
    black_pixels = np.sum(img <= 150)
    black_ratio = black_pixels / total_pixels
    height, width = img.shape
    black_area = black_ratio * height * width * 0.01
    black_area = f"{black_area:.2f}"
    black_ratio = f"{black_ratio * 100:.2f}"
    print(f"黑色区域面积: {black_area}, 黑色像素比例: {black_ratio}%")
    black_area, black_ratio = float(black_area), float(black_ratio)
    return black_area, black_ratio

def find_y_coordinate(img_pil, target_ratio=0.8):
    img = np.array(img_pil.convert("L"))
    height, width = img.shape
    print("开始计算基质流")
    for y in range(start_height, height):
        row = img[y, :]
        black_pixels = np.sum(row <= 120)
        black_ratio = black_pixels / width
        if black_ratio <= target_ratio:
            matrix_flow_depth = y / 10
            print(f"基质流深度为{matrix_flow_depth}")
            return matrix_flow_depth
    return 0

def calculate_priority_flow_percentage(soil_width, matrix_flow_depth, black_area):
    a = soil_width * matrix_flow_depth
    b = black_area
    print(f"a值: {a}, b值: {b}")
    result = f"{(1 - a / b) * 100:.2f}"
    print(f"优先流百分数{result}%")
    result = float(result)
    return result

def calculate_area_ratio_of_preferred_flow_zone(soil_width, matrix_flow_depth, black_area):
    a = float(black_area) - matrix_flow_depth * soil_width
    soil_area = soil_width * soil_width
    result = (a / soil_area) * 100
    result = f"{result:.2f}"
    print(f"优先流区染色面积比: {result} %")
    result = float(result)
    return result

def calculate_maximum_staining_depth(img_pil, target_ratio=0.005):
    img = np.array(img_pil.convert("L"))
    height, width = img.shape
    empty_count = 0
    for y in range(height - 1, -1, -1):
        row = img[y, :]
        black_pixels = np.sum(row <= 200)
        black_ratio_temp = black_pixels / width
        if black_ratio_temp >= 0.1:
            break
        elif black_ratio_temp >= target_ratio:
            empty_count += 1
            print(f"空白行数{empty_count}")
            if empty_count >= 2:
                y /= 10
                print(f"最大染色深度为{y}cm")
                y = f"{y:.2f}"
                y = float(y)
                return y
    return round(y * 0.1)

def calculate_length_index(img_pil):
    img = np.array(img_pil.convert("L"))
    height, width = img.shape
    ratio_list = []
    difference_proportion_list = []

    for y in range(height):
        row = img[y, :]
        black_pixels = np.sum(row <= 120)
        black_ratio_temp = black_pixels / width
        ratio_list.append(black_ratio_temp)
        if len(ratio_list) >= 2:
            difference_proportion = abs(ratio_list[-1] - ratio_list[-2])
            difference_proportion_list.append(difference_proportion)

    total_difference_proportion = sum(difference_proportion_list)
    total_difference_proportion = round(total_difference_proportion, 3)
    total_difference_proportion *= 100
    total_difference_proportion = f"{total_difference_proportion:.2f}"
    print(f"长度指数: {total_difference_proportion}")
    total_difference_proportion = float(total_difference_proportion)
    return total_difference_proportion

def draw_red_line(img_pil, matrix_flow_depth):
    draw = ImageDraw.Draw(img_pil)
    width, height = img_pil.size
    line_thickness = int(height * 0.005)
    draw.line([(0, matrix_flow_depth), (width, matrix_flow_depth)], fill="#a60d0d", width=line_thickness)
    return img_pil

def draw_blue_line(img_pil, start_height):
    draw = ImageDraw.Draw(img_pil)
    width, height = img_pil.size
    line_thickness = int(height * 0.003)
    draw.line([(0, start_height), (width, start_height)], fill="#00acd6", width=line_thickness)
    return img_pil

def draw_green_line(img_pil, maximum_staining_depth):
    draw = ImageDraw.Draw(img_pil)
    width, height = img_pil.size
    line_thickness = int(height * 0.003)
    draw.line([(0, maximum_staining_depth), (width, maximum_staining_depth)], fill="#12822a", width=line_thickness)
    return img_pil

def calculate_parameters(img_pil):
    global black_area, black_ratio, matrix_flow_depth, priority_flow_percentage, priority_staining_area, maximum_staining_depth, length_index
    black_area, black_ratio = calculate_black_area_ratio(img_pil)
    matrix_flow_depth = find_y_coordinate(img_pil)
    priority_flow_percentage = calculate_priority_flow_percentage(soil_width, matrix_flow_depth, black_area)
    priority_staining_area = calculate_area_ratio_of_preferred_flow_zone(soil_width, matrix_flow_depth, black_area)
    maximum_staining_depth = calculate_maximum_staining_depth(img_pil)
    length_index = calculate_length_index(img_pil)

def process_image(img_pil, lower_range, upper_range, resolution):
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    img_cv = cv2.GaussianBlur(img_cv, (17, 17), 0)
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    if not is_grayscale_image(img_pil):
        print("是原图，进入颜色处理")
        img_pil = black_white_processing(img_pil, resolution)
    else:
        img_pil = resize_image(img_pil, resolution)
        print("是黑白图，取消颜色处理")
    calculate_parameters(img_pil)
    return img_pil
