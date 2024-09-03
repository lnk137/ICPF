import io
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageOps
import webview
import threading
import numpy as np
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 全局变量存储颜色范围和其他参数
lower_range_hsv =[35, 35, 35]
upper_range_hsv = [255, 255, 255]
resolution = "500x500"
soil_width = 500
start_height = 0

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

def parse_resolution(resolution_str):
    # 解析分辨率字符串并返回宽度和高度
    if resolution_str:
        try:
            width, height = map(int, resolution_str.lower().split('x'))
            return width, height
        except ValueError:
            print("解析分辨率失败，使用默认500x500")
    return 500, 500  # 默认分辨率

def resize_image(img_pil, resolution):
    # 调整图像分辨率
    width, height = parse_resolution(resolution)
    return img_pil.resize((width, height), Image.LANCZOS)  # 使用 LANCZOS 替换 ANTIALIAS


import numpy as np

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


def process_image(img_pil, lower_range, upper_range, resolution):
    # 如果图像是灰度图，则跳过颜色处理
    if is_grayscale_image(img_pil):
        print("灰度图检测到，跳过颜色处理")
        img_resized = resize_image(img_pil, resolution)  # 调整分辨率
        return img_resized

    # 处理图像，先调整分辨率再进行颜色操作
    img_resized = resize_image(img_pil, resolution)  # 调整分辨率

    img_cv = np.array(img_resized)  # 将PIL图像转换为NumPy数组
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)  # 将RGB格式转换为BGR格式
    hsv_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)  # 将图像转换为HSV色彩空间

    if len(lower_range) == 3 and len(upper_range) == 3:
        mask = cv2.inRange(hsv_img, np.array(lower_range), np.array(upper_range))  # 创建颜色掩码

        # 反转掩码的黑白颜色
        inverted_mask = cv2.bitwise_not(mask)

        # 将处理后的掩码转换为三通道的图像以便返回和显示
        mask_rgb = cv2.cvtColor(inverted_mask , cv2.COLOR_GRAY2RGB)

        return Image.fromarray(mask_rgb)  # 将掩码图像转换为PIL图像并返回
    else:
        raise ValueError("lower_range和upper_range必须是长度为3的列表或数组")

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

    # 将处理后的图像保存到字节流中
    img_io = io.BytesIO()
    processed_img.save(img_io, "PNG")
    img_io.seek(0)

    # 将图像作为响应返回
    return send_file(img_io, mimetype="image/png")


def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # 创建并启动一个线程来运行Flask应用
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 创建Webview窗口，设置自定义大小
    webview.create_window("Image Uploader", "http://localhost:5173/", width=1000, height=800)
    webview.start()
