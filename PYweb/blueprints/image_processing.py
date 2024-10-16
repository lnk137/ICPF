from flask import Blueprint, request, jsonify, send_file
from PIL import Image
import io
import webview
from utils.image_utils import (
    process_image, draw_red_line, draw_blue_line, draw_green_line
)
import config  # 导入config模块
import traceback

image_processing_bp = Blueprint('image_processing', __name__)

@image_processing_bp.route("/upload", methods=["POST"])
def upload_image():
    try:
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
        config.grayscale_picture = processed_img

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

    except Exception as e:
        
        return jsonify({"error": f"上传图像时出错: {e}"}), 500


@image_processing_bp.route("/save-image", methods=["POST"])
def save_image_route():
    # 检查是否有图像可保存
    if not any([config.original_picture, config.grayscale_picture, config.gb_picture, config.no_gb_picture]):
        return jsonify({"error": "没有图像可保存"}), 400

    try:
        # 打开保存对话框
        save_path = webview.windows[0].create_file_dialog(
            webview.SAVE_DIALOG,
            file_types=('PNG files (*.png)',),
            save_filename='soil'
        )

        if save_path:
            base_path = save_path[0] if isinstance(save_path, list) else save_path
            base_path = base_path if base_path.endswith('.png') else f"{base_path}.png"

            # 定义要保存的图片列表
            pictures = {
                "original": config.original_picture,
                "grayscale": config.grayscale_picture,
                "gb": config.gb_picture,
                "no_gb": config.no_gb_picture
            }

            # 依次保存每张图片
            for key, image in pictures.items():
                if image:
                    image.save(base_path.replace('.png', f'_{key}.png'), 'PNG')

            return jsonify({"message": "图像已成功保存"}), 200
        else:
            return jsonify({"error": "用户取消了保存操作"}), 400

    except Exception as e:
        
        return jsonify({"error": f"保存图像时出错: {e}"}), 500

@image_processing_bp.route("/save_excel", methods=['POST'])
def save_excel():
    try:
        # 打开保存对话框，让用户选择保存路径
        save_path = webview.windows[0].create_file_dialog(
            webview.SAVE_DIALOG,
            file_types=('Excel files (*.xlsx)',),  # 文件类型
            save_filename='像素矩阵.xlsx'  # 默认文件名
        )

        # 如果用户选择了路径，将 Excel 文件保存到该路径
        if save_path:
            file_path = save_path[0] if isinstance(save_path, list) else save_path
            with open(file_path, 'wb') as f:
                f.write(config.excel_file.getvalue())  # 写入内存中的 Excel 文件
            return jsonify({"message": "Excel saved successfully"}), 200
        else:
            return jsonify({"error": "User cancelled the save operation"}), 400

    except Exception as e:
        # 捕获并记录异常
        print(f"保存Excel文件时发生错误: {str(e)}")
        return jsonify({"error": f"保存Excel文件时发生错误: {str(e)}"}), 500
