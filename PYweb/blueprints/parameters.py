from flask import Blueprint, request, jsonify
import config  # 导入config模块

parameters_bp = Blueprint('parameters', __name__)

@parameters_bp.route("/color-ranges", methods=["POST"])
def get_data():
    data = request.json

    # 解析颜色范围和其他参数，并确保数值为整数类型
    config.lower_range_hsv = data.get("lower_range", None)
    config.upper_range_hsv = data.get("upper_range", None)
    config.resolution = data.get("resolution", None)
    config.soil_width = int(data.get("soil_width", 0))
    config.start_height = int(data.get("start_height", 0))

    if config.lower_range_hsv is not None:
        config.lower_range_hsv = [int(value) for value in config.lower_range_hsv]

    if config.upper_range_hsv is not None:
        config.upper_range_hsv = [int(value) for value in config.upper_range_hsv]

    return jsonify({
        "lower_hsv": config.lower_range_hsv,
        "upper_hsv": config.upper_range_hsv,
        "resolution": config.resolution,
        "soil_width": config.soil_width,
        "start_height": config.start_height,
    })

@parameters_bp.route("/show-data", methods=["GET"])
def show_data():
    return jsonify({
        "black_area": config.black_area,
        "black_ratio": config.black_ratio,
        "matrix_flow_depth": config.matrix_flow_depth,
        "priority_flow_percentage": config.priority_flow_percentage,
        "priority_staining_area": config.priority_staining_area,
        "maximum_staining_depth": config.maximum_staining_depth,
        "length_index": config.length_index,
    })