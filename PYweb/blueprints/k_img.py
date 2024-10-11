# 导入 Flask 相关模块
from flask import Blueprint, request, jsonify, send_file

# 导入 PIL 模块
from PIL import Image

# 导入内存操作模块
import io

# 导入自定义工具类
from utils.k_means_util import k_means_img

# 导入配置模块
import config

# 创建蓝图
k_img_bp = Blueprint('k_img', __name__)

@k_img_bp.route("/k_means", methods=["POST"])
def k_means():
    # 从请求中获取上传的文件
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "没有文件上传"}), 400

    try:
        # 将文件对象转为 PIL 图像格式
        img = Image.open(file)

        # 获取配置中的相关参数
        resolution = config.resolution
        lower_range_hsv = config.lower_range_hsv
        upper_range_hsv = config.upper_range_hsv

        # 实例化工具类
        img_processor = k_means_img(resolution=resolution)

        # 调用 upload_image 处理图像
        processed_image = img_processor.process_image(img, lower_range_hsv, upper_range_hsv)
        # 将处理后的图像保存到字节流中
        img_io = io.BytesIO()
        processed_image.save(img_io, "PNG")
        img_io.seek(0)

        # 将字节流返回给客户端
        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        # 捕获并返回任何可能的错误信息
        return jsonify({"error": str(e)}), 500
