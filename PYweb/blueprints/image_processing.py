from flask import Blueprint, request, jsonify, send_file
from PIL import Image
import io
import webview
from utils.image_utils import (
    process_image, draw_red_line, draw_blue_line, draw_green_line
)
import config  # 导入config模块

image_processing_bp = Blueprint('image_processing', __name__)

@image_processing_bp.route("/upload", methods=["POST"])
def upload_image():
    # 获取全局变量
    lower_range_hsv = config.lower_range_hsv
    upper_range_hsv = config.upper_range_hsv
    resolution = config.resolution
    start_height = config.start_height

    # 获取上传的文件
    file = request.files["file"]
    img = Image.open(file)

    # 调用处理函数处理图像
    processed_img = process_image(img, lower_range_hsv, upper_range_hsv, resolution)
    config.original_picture = processed_img

    # 绘制红线、蓝线和绿线
    display_img = processed_img.copy()
    display_img = draw_red_line(display_img, config.matrix_flow_depth * 10)
    display_img = draw_blue_line(display_img, start_height)
    display_img = draw_green_line(display_img, config.maximum_staining_depth * 10)

    # 将处理后的图像保存到字节流中
    img_io = io.BytesIO()
    display_img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

@image_processing_bp.route("/save-image", methods=["POST"])
def save_image_route():
    if config.original_picture is None:
        return jsonify({"error": "没有图像可保存"}), 400

    try:
        # 使用 pywebview 打开文件保存对话框
        save_path = webview.windows[0].create_file_dialog(
            webview.SAVE_DIALOG,
            file_types=('PNG files (*.png)',),
            save_filename='processed_image.png'
        )

        if save_path:
            file_path = save_path[0] if isinstance(save_path, list) else save_path

            if not file_path.lower().endswith('.png'):
                file_path = f"{file_path}.png"

            config.original_picture.save(file_path, 'PNG')
            print(f"图像已保存到 {file_path}")
            return jsonify({"message": "图像已成功保存"}), 200
        else:
            return jsonify({"error": "用户取消了保存操作"}), 400

    except Exception as e:
        print(f"保存图像时出错: {e}")
        return jsonify({"error": f"保存图像时出错: {e}"}), 500
