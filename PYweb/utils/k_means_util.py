import io
from PIL import Image, ImageOps, ImageDraw
import numpy as np
import cv2
from sklearn.cluster import KMeans  # 导入KMeans
import config  # 导入config模块

class k_means_img:
    def __init__(self, resolution=(500, 500), k=4):
        self.resolution = resolution
        self.k = k

    # 调整图像分辨率
    def resize_image(self, img_pil):
        width, height = self.resolution
        return img_pil.resize((width, height), Image.LANCZOS)

    # k-means聚类
    def segment_image(self, image):
        # 转换为numpy数组
        image = np.array(image)

        # 将图像转换为HSV颜色空间
        image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        # 将整个HSV空间的数据转换为二维数组
        hsv_data = image_hsv.reshape(-1, 3)

        # 使用K-means聚类
        kmeans = KMeans(n_clusters=self.k, n_init=10, random_state=42)
        kmeans.fit(hsv_data)

        # 获取聚类结果的标签
        labels = kmeans.labels_

        # 获取聚类中心（色相、饱和度和亮度的均值）
        cluster_centers = kmeans.cluster_centers_

        # 将聚类中心的HSV值转换回RGB
        cluster_centers_rgb = cv2.cvtColor(cluster_centers.reshape(1, -1, 3).astype(np.uint8), cv2.COLOR_HSV2RGB).reshape(-1, 3)

        # 保存聚类中心颜色到全局配置
        config.cluster_colors.clear()
        hex_colors = []
        for i, center in enumerate(cluster_centers_rgb):
            hex_color = "#{:02x}{:02x}{:02x}".format(int(center[0]), int(center[1]), int(center[2]))
            hex_colors.append(hex_color)
            config.cluster_colors.append(hex_color)

        # 映射分类结果到聚类中心对应的RGB颜色
        segmented_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        labels_reshaped = labels.reshape(image.shape[:2])
        for idx in range(self.k):
            segmented_image[labels_reshaped == idx] = cluster_centers_rgb[idx]

        return Image.fromarray(segmented_image), labels_reshaped

    # 统计每种颜色的面积和比例
    def calculate_color_stats(self, labels, img_pil, hex_colors):
        # 获取图像的宽和高
        width, height = img_pil.size
        total_pixels = width * height
        print(f"总像素数: {total_pixels}")
        # 用于存储新的颜色信息
        new_color_ifos = []
        # 遍历每个聚类，计算其面积和比例
        for idx in range(self.k):
            color_pixel_count = np.sum(labels == idx)
            color_ratio = color_pixel_count / total_pixels
            color_pixel_count/=100
            color_ratio*=100
            color_ratio=f"{color_ratio:.2f}"
            color_ratio=float(color_ratio)
            color_ifo = {
                'index': idx,
                'hex_color': hex_colors[idx],
                'area': color_pixel_count,
                'ratio': color_ratio
            }
            print(color_ifo)
            # 将新的颜色信息添加到列表中
            new_color_ifos.append(color_ifo)
            # 直接替换 config.color_ifos 的内容
        config.color_ifos = new_color_ifos

    # 黑白颜色处理函数
    def black_white_processing(self, img_pil, lower_range_hsv, upper_range_hsv):
        # 处理图像，先调整分辨率再进行颜色操作
        img_resized = self.resize_image(img_pil)  # 调整分辨率
        img_cv = np.array(img_resized)  # 将PIL图像转换为NumPy数组
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)  # 将RGB格式转换为BGR格式
        hsv_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)  # 将图像转换为HSV色彩空间

        # 创建颜色掩码
        mask = cv2.inRange(hsv_img, np.array(lower_range_hsv), np.array(upper_range_hsv))
        # 使用掩码过滤原始图像，保留符合HSV范围的部分
        result_img = cv2.bitwise_and(img_cv, img_cv, mask=mask)
        # 在显示之前，将BGR图像转换为RGB
        result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

        # 创建一个新的图像，初始化为白色
        white_background_img = np.full((result_img.shape[0], result_img.shape[1], 3), 255, dtype=np.uint8)

        # 将保留区域（符合掩码的部分）覆盖到白色背景图像上
        white_background_img[mask > 0] = result_img_rgb[mask > 0]

        # 将 NumPy 数组转换为 PIL 图像，最终不包含透明度
        stain_img = Image.fromarray(white_background_img)

        # 生成不带高斯模糊的K-means图像
        print("开始生成不带高斯模糊的K-means聚类图像")
        non_blurred_segmented_image, labels = self.segment_image(stain_img)
        # 调用统计函数
        self.calculate_color_stats(labels, non_blurred_segmented_image, config.cluster_colors)
        config.no_gb_picture = non_blurred_segmented_image
        # non_blurred_segmented_image.save("无模糊聚类图.png")
        # print("已保存不带高斯模糊的K-means聚类图像")

        # 调用高斯模糊处理函数
        stain_img = self.apply_gaussian_blur(stain_img)

        # 调用segment_image生成分割结果
        segmented_image, _ = self.segment_image(stain_img)
        config.gb_picture = segmented_image
        return segmented_image,non_blurred_segmented_image

    # 图像处理主函数
    def process_image(self, img_pil, lower_range_hsv, upper_range_hsv):
        GB_Img,NO_GB_Img = self.black_white_processing(img_pil, lower_range_hsv, upper_range_hsv)
        return GB_Img,NO_GB_Img
    
    # 高斯模糊函数
    def apply_gaussian_blur(self, img_pil, ksize=(15, 15)):
        # 将 PIL 图像转换为 NumPy 数组
        img_cv = np.array(img_pil)
        # 对图像应用高斯模糊
        blurred_img_cv = cv2.GaussianBlur(img_cv, ksize, 0)
        # 将模糊后的图像转换回 PIL 格式
        blurred_img_pil = Image.fromarray(blurred_img_cv)
        return blurred_img_pil

