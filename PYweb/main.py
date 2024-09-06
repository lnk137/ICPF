import io
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageOps, ImageDraw
import webview
import threading
import numpy as np
import cv2
from flask_cors import CORS
#pyinstaller main.spec
app = Flask(__name__)
CORS(app)

# 全局变量存储颜色范围和其他参数
lower_range_hsv =[35, 35, 35]
upper_range_hsv = [255, 255, 255]
resolution = "500x500"
soil_width = 50
start_height = 0


# 获得前端的参数
@app.route("/color-ranges", methods=["POST"])
def get_data():
    global lower_range_hsv, upper_range_hsv, resolution, soil_width, start_height
    data = request.json

    # 解析颜色范围和其他参数
    lower_range_hsv = data.get("lower_range", None)
    upper_range_hsv = data.get("upper_range", None)
    resolution = data.get("resolution", None)
    soil_width = data.get("soil_width", None)
    start_height = data.get("start_height", None)

    # 调试输出，检查接收到的数据
    print(f"Lower HSV range: {lower_range_hsv}")
    print(f"Upper HSV range: {upper_range_hsv}")
    print(f"Resolution: {resolution}")
    print(f"Soil width: {soil_width}")
    print(f"Start height: {start_height}")

    return jsonify({
        "lower_hsv": lower_range_hsv,
        "upper_hsv": upper_range_hsv,
        "resolution": resolution,
        "soil_width": soil_width,
        "start_height": start_height,
    })


# 获取分辨率
def parse_resolution(resolution_str):
    # 解析分辨率字符串并返回宽度和高度
    if resolution_str:
        try:
            width, height = map(int, resolution_str.lower().split('x'))
            return width, height
        except ValueError:
            print("解析分辨率失败，使用默认500x500")
    return 500, 500  # 默认分辨率

# 调整图像分辨率
def resize_image(img_pil, resolution):
   
    width, height = parse_resolution(resolution)
    return img_pil.resize((width, height), Image.LANCZOS)  # 使用 LANCZOS 替换 ANTIALIAS


# 判断图像是否是灰度图
def is_grayscale_image(img_pil):
    # 将图像转换为灰度图像数组
    img_array = np.array(img_pil.convert("L"))
    
    # 获取图像的总像素数
    total_pixels = img_array.size
    
    # 定义黑色和白色的阈值范围
    black_threshold = 20  # 黑色像素的最大值
    white_threshold = 200  # 白色像素的最小值
    
    # 统计黑色和白色像素的数量
    black_pixels = np.sum(img_array <= black_threshold)
    white_pixels = np.sum(img_array >= white_threshold)
    
    # 计算黑色和白色像素的比例
    black_ratio = black_pixels / total_pixels
    white_ratio = white_pixels / total_pixels
    
    # 如果黑色或白色像素比例超过 20%，则认为是需要跳过颜色处理的图像
    if black_ratio > 0.3 or white_ratio > 0.3:
        print(f"黑色比例: {black_ratio:.2f}, 白色比例: {white_ratio:.2f} - 跳过颜色处理")
        return True
    
    return False

# 在图像上绘制红线
def draw_red_line(display_img, matrix_flow_depth):
    draw = ImageDraw.Draw(display_img)
    width, height = display_img.size
    line_thickness = int(height * 0.005)  # 计算线条厚度
    draw.line([(0, matrix_flow_depth), (width, matrix_flow_depth)], fill="#a60d0d", width=line_thickness)  # 绘制红线
    return display_img

# 在图像上绘制蓝线
def draw_blue_line(img_pil, start_height):
    draw = ImageDraw.Draw(img_pil)
    width, height = img_pil.size
    line_thickness = int(height * 0.003)  # 计算线条厚度
    draw.line([(0, start_height), (width, start_height)], fill="#00acd6", width=line_thickness)  # 绘制蓝线
    return img_pil

# 在图像上绘制绿线
def draw_green_line(img_pil, maximum_staining_depth):
    draw = ImageDraw.Draw(img_pil)
    width, height = img_pil.size
    line_thickness = int(height * 0.003)  # 计算线条厚度
    draw.line([(0, maximum_staining_depth), (width, maximum_staining_depth)], fill="#12822a", width=line_thickness)  # 绘制绿线
    return img_pil

# 计算染色区域面积和染色比例
def calculate_black_area_ratio(img_pil):
    img = np.array(img_pil.convert("L"))  # 转换为灰度图像数组
    total_pixels = img.size
    black_pixels = np.sum(img <= 150)  # 计算黑色像素数量
    black_ratio = black_pixels / total_pixels  # 计算黑色像素比例
    height, width = img.shape
    black_area = black_ratio * height * width * 0.01  # 计算黑色区域面积
    black_area= f"{black_area:.2f}"
    black_ratio= f"{black_ratio*100:.2f}"
    print(f"@@@来自calculate_black_area_ratio@@@")
    print(f"黑色区域面积: {black_area}, 黑色像素比例: {black_ratio}%")
    black_area, black_ratio=float(black_area),float(black_ratio)
    return black_area, black_ratio


# 计算基质流深度
def find_y_coordinate(img_pil, target_ratio=0.8):
    img = np.array(img_pil.convert("L"))  # 转换为灰度图像数组
    height, width = img.shape
    for y in range(int(start_height), height):
        row = img[y, :]  # 获取当前行像素值
        black_pixels = np.sum(row <= 120)  # 计算当前行黑色像素数量
        black_ratio = black_pixels / width  # 计算当前行黑色像素比例
        if black_ratio <= target_ratio:
            matrix_flow_depth=y/10
            print(f"@@@来自find_y_coordinate@@@")
            print(f"基质流深度为{matrix_flow_depth}")
            return matrix_flow_depth  # 返回符合条件的y坐标
    matrix_flow_depth=None # 如果没有找到符合条件的y坐标
    
# 计算优先流百分数
def calculate_priority_flow_percentage(soil_width, matrix_flow_depth, black_area):
    a = float(soil_width) * float(matrix_flow_depth)  # 计算a值
    b = float(black_area)  # 获取染色面积并转换为浮点数
    print(f"a值: {a}, b值: {b}")
    result = f"{(1 - a / b) * 100:.2f}"  # 计算优先流百分数
    print("@@@来自calculate_priority_flow_percentage@@@")
    result=float(result)
    print(f"优先流百分数{result}%")
    return result

# 计算优先流区染色面积比
def calculate_area_ratio_of_preferred_flow_zone(soil_width, matrix_flow_depth, black_area):
    a=float(black_area)-matrix_flow_depth*soil_width
    soil_area = soil_width * soil_width 
    result = (a/soil_area)*100
    result=f"{result:.2f}"
    print("@@@来自calculate_area_ratio_of_preferred_flow_zone@@@")
    print(f"优先流区染色面积比: {result} %")
    result=float(result)
    return result

#计算最大染色深度
def calculate_maximum_staining_depth (img_pil, target_ratio=0.005):
    img = np.array(img_pil.convert("L"))  # 转换为灰度图像数组
    height, width = img.shape
    empty_count = 0
    for y in range(height - 1, -1, -1):
        row = img[y, :]  # 获取当前行像素值
        black_pixels = np.sum(row <= 200)  # 计算当前行黑色像素数量
        black_ratio_temp = black_pixels / width  # 计算当前行黑色像素比例
        if black_ratio_temp >= 0.1:
            break
        elif black_ratio_temp >= target_ratio:
            empty_count += 1  # 计算空白行数
            print(f"空白行数{empty_count}")
            if empty_count >= 2:
                y/=10
                print(f"@@@来自calculate_maximum_staining_depth@@@")
                print(f"最大染色深度为{y}cm")
                y=f"{y:.2f}"
                y=float(y)
                return y # 返回最大染色深度
    return round(y*0.1)# 如果没有找到符合条件的y坐标

# 计算长度指数
def calculate_length_index(img_pil):
    img = np.array(img_pil.convert("L"))  # 转换为灰度图像数组
    height, width = img.shape
    ratio_list = []
    difference_proportion_list = []
    
    for y in range(height):
        row = img[y, :]  # 获取当前行像素值
        black_pixels = np.sum(row <= 120)  # 计算当前行黑色像素数量
        black_ratio_temp = black_pixels / width  # 计算当前行黑色像素比例
        ratio_list.append(black_ratio_temp)  # 保存当前行黑色像素比例
        
        # 如果列表中有至少两个元素，计算当前行与上一行的差值比例
        if len(ratio_list) >= 2:
            difference_proportion = abs(ratio_list[-1] - ratio_list[-2])
            difference_proportion_list.append(difference_proportion)
    
    total_difference_proportion = sum(difference_proportion_list)
    total_difference_proportion = round(total_difference_proportion, 3)  # 保留三位小数
    total_difference_proportion *= 100  # 乘以100
    total_difference_proportion= f"{total_difference_proportion:.2f}"
    print(f"@@@来自calculate_length_index@@@")
    print(f"长度指数: {total_difference_proportion}")
    total_difference_proportion=float(total_difference_proportion)
    return total_difference_proportion
# 黑白颜色处理函数
def black_white_processing(img_pil,resolution):
    # 处理图像，先调整分辨率再进行颜色操作
    img_resized = resize_image(img_pil, resolution)  # 调整分辨率

    img_cv = np.array(img_resized)  # 将PIL图像转换为NumPy数组
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)  # 将RGB格式转换为BGR格式
    hsv_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)  # 将图像转换为HSV色彩空间

    if len(lower_range_hsv) != 3 and len(upper_range_hsv) != 3:
        raise ValueError("lower_range和upper_range必须是长度为3的列表或数组")
    # 创建颜色掩码
    mask = cv2.inRange(hsv_img, np.array(lower_range_hsv), np.array(upper_range_hsv)) 
    # 反转掩码的黑白颜色
    inverted_mask = cv2.bitwise_not(mask)
    # 将处理后的掩码转换为三通道的图像以便返回和显示
    mask_rgb = cv2.cvtColor(inverted_mask , cv2.COLOR_GRAY2RGB)
    # 将掩码图像转换为PIL图像
    img_pil=Image.fromarray(mask_rgb)  
    return img_pil

# 计算各种参数
def calculate_parameters(img_pil):
    global black_area, black_ratio, matrix_flow_depth, priority_flow_percentage, priority_staining_area, maximum_staining_depth, length_index
    black_area, black_ratio = calculate_black_area_ratio(img_pil)
    matrix_flow_depth = find_y_coordinate(img_pil)
    priority_flow_percentage = calculate_priority_flow_percentage(soil_width, matrix_flow_depth, black_area)
    priority_staining_area = calculate_area_ratio_of_preferred_flow_zone(soil_width, matrix_flow_depth, black_area)
    maximum_staining_depth = calculate_maximum_staining_depth(img_pil)
    length_index = calculate_length_index(img_pil)
#图像处理主函数
def process_image(img_pil, lower_range, upper_range, resolution):
    # 如果图像不是灰度图，则进入颜色处理
    if not is_grayscale_image(img_pil):
        print("是原图，进入颜色处理")
        img_pil=black_white_processing(img_pil,resolution)
    else:
        img_pil = resize_image(img_pil, resolution)  # 调整分辨率
        print("是黑白图，取消颜色处理")
    # 计算各种参数
    calculate_parameters(img_pil)
    
    return img_pil

@app.route("/upload", methods=["POST"])
def upload_image():
    global lower_range_hsv, upper_range_hsv

    if lower_range_hsv is None or upper_range_hsv is None:
        return jsonify({"error": "Color ranges not set"}), 400

    # 获取上传的文件
    file = request.files["file"]
    img = Image.open(file)

    # 调用处理函数处理图像
    processed_img = process_image(img, lower_range_hsv, upper_range_hsv, resolution)
    display_img = processed_img.copy()
    display_img=draw_red_line(display_img, matrix_flow_depth*10)  # 绘制基质流深度的红线
    display_img=draw_blue_line(display_img, start_height)  # 绘制基质流深度的红线
    display_img=draw_green_line(display_img, maximum_staining_depth*10)  # 绘制基质流深度的红线
    # 将处理后的图像保存到字节流中
    img_io = io.BytesIO()
    display_img.save(img_io, "PNG")
    img_io.seek(0)

    # 将图像作为响应返回
    return send_file(img_io, mimetype="image/png")

@app.route("/show-data", methods=["GET"])
def show_data():
    # 返回已经处理好的参数
    print("@@@来自show_data@@@")
    print(f"----{black_area}-----")
    return jsonify({
        "black_area": black_area,  # 已处理好的黑色区域面积
        "black_ratio": black_ratio,  # 已处理好的黑色像素比例
        "matrix_flow_depth":matrix_flow_depth,
        "priority_flow_percentage":priority_flow_percentage,
        "priority_staining_area":priority_staining_area,
        "maximum_staining_depth":maximum_staining_depth,
        "length_index":length_index,
    })

def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # 创建并启动一个线程来运行Flask应用
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 创建Webview窗口，设置自定义大小
    #http://localhost:5173/
    # web/index.html
    webview.create_window("智算优先流", "web/index.html", width=1000, height=800, resizable=False)
    webview.start()
