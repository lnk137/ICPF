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

        # 调用 process_image 处理图像，返回高斯模糊和未模糊的图像
        GB_Img, NO_GB_Img = img_processor.process_image(img, lower_range_hsv, upper_range_hsv)

        # 创建字节流对象来存储图像
        gb_img_io = io.BytesIO()
        no_gb_img_io = io.BytesIO()

        # 将处理后的图像保存到字节流中
        GB_Img.save(gb_img_io, "PNG")
        NO_GB_Img.save(no_gb_img_io, "PNG")

        # 回到字节流的开始位置
        gb_img_io.seek(0)
        no_gb_img_io.seek(0)

        # 返回两个图像为附件形式的响应
        return jsonify({
            "GB_Img": gb_img_io.getvalue().decode('latin1'),  # 将二进制数据转换为可传输的字符串形式
            "NO_GB_Img": no_gb_img_io.getvalue().decode('latin1')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@k_img_bp.route("/get_color_ifos", methods=["POST"])
def get_color_ifos():
    try:
        # 从 config 文件中获取 color_ifos
        color_ifos = config.color_ifos
        # 将 color_ifos 数据通过 jsonify 返回给前端
        return jsonify({"color_ifos": color_ifos}), 200
    except Exception as e:
        # 捕获并返回任何可能的错误信息
        return jsonify({"error": str(e)}), 500
