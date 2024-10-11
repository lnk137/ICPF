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
        return img_pil.resize((width, height), Image.LANCZOS)  # 使用 LANCZOS 替换 ANTIALIAS

    # k-means聚类
    def segment_image(self, image, blur_ksize=(1, 1)):
        # 转换为numpy数组
        image = np.array(image)
        # 高斯模糊处理，降噪
        image_blur = cv2.GaussianBlur(image, blur_ksize, 0)

        # 将模糊后的图像转换为HSV颜色空间
        image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

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

        # 打印每个聚类中心的颜色的16进制表示
        for i, center in enumerate(cluster_centers_rgb):
            hex_color = "#{:02x}{:02x}{:02x}".format(int(center[0]), int(center[1]), int(center[2]))
            print(f"聚类 {i} 的颜色: {hex_color}")

        # 映射分类结果到聚类中心对应的RGB颜色
        segmented_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        for idx in range(self.k):
            segmented_image[labels.reshape(image.shape[:2]) == idx] = cluster_centers_rgb[idx]

        return Image.fromarray(segmented_image)

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

        # 调用segment_image生成分割结果
        segmented_image = self.segment_image(stain_img)

        return segmented_image

    # 图像处理主函数
    def process_image(self, img_pil, lower_range_hsv, upper_range_hsv):
        processed_img = self.black_white_processing(img_pil, lower_range_hsv, upper_range_hsv)
        return processed_img

    # 上传并处理图像
    def upload_image(self, img, lower_range_hsv, upper_range_hsv):
        processed_img = self.process_image(img, lower_range_hsv, upper_range_hsv)
        return processed_img

# 示例如何使用工具类
if __name__ == "__main__":
    # 示例输入参数，用户需根据实际输入来调整
    img_path = "1.png"  # 替换为实际的图像路径
    lower_range_hsv = config.lower_range_hsv
    upper_range_hsv = config.upper_range_hsv
    resolution =config.resolution

    # 实例化工具类
    img_processor = k_means_img(resolution=resolution)

    # 调用 upload_image 处理图像
    processed_image = img_processor.upload_image(img, lower_range_hsv, upper_range_hsv)
    
    # 保存处理后的图像
    processed_image.save("processed_image.png")
