<template>
  <div class="page2">
    <!-- 使用 ImageUploader 组件 -->
    <ImageUploader @file-selected="uploadImage" />

    <!-- 如果 grayscaleImage 有值，则显示处理后的灰度图 -->
    <div v-if="grayscaleImage" class="image-preview">
      <p class="image-preview-title">处理后:</p>
      <img :src="grayscaleImage" alt="Grayscale Image" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ImageUploader from '../components/ImageUploader.vue';

const grayscaleImage = ref(null);

// 上传图片到后端并处理返回结果
const uploadImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      grayscaleImage.value = imageUrl;
    } else {
      console.error("Upload failed");
    }
  } catch (error) {
    console.error("An error occurred during the upload process:", error);
  }
};
</script>

<style scoped lang="less">
.page2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.image-preview img {
  max-width: 400px;
  max-height: 400px;
  border: 1px solid #ccc;
  margin-top: 20px;
}

.clickable {
  text-decoration: underline; /* 添加下划线 */
  color: rgb(41, 172, 73);
}

.image-preview-title {
  color: rgb(48, 52, 64);
  font-size: 20px;
  font-weight: bold;
}
</style>
