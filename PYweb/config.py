# config.py

lower_range_hsv = [35, 35, 35]
upper_range_hsv = [255, 255, 255]
resolution = [500,500]
soil_width = 50
start_height = 0
original_picture = None
grayscale_picture = None
gb_picture = None
no_gb_picture = None

# 其他变量
black_area = None
black_ratio = None
matrix_flow_depth = None
priority_flow_percentage = None
priority_staining_area = None
maximum_staining_depth = None
length_index = None

# k-means 颜色数组
cluster_colors = []
color_ifos = []


excel_file = None  # 用于保存内存中的 Excel 文件

