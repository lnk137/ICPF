<template>
  <div class="page2">
    <ImageUploader @file-selected="uploadImage" />

    <div v-if="grayscaleImage" class="image-preview">
      <p class="image-preview-title">处理后:</p>
      <!-- 点击图片时，显示在弹出窗口中 -->
      <img :src="grayscaleImage" alt="Grayscale Image" @click="openImageModal" />
    </div>

    <!-- 弹出窗口 -->
    <div v-if="showModal" class="modal" @click="closeImageModal">
      <div class="modal-content">
        <img :src="grayscaleImage" alt="Grayscale Image" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ImageUploader from '../components/ImageUploader.vue';

const props = defineProps({
  grayscaleImage: String,
  updateImage: Function,
});

const grayscaleImage = ref(props.grayscaleImage);
const showModal = ref(false);

const openImageModal = () => {
  showModal.value = true;
};

const closeImageModal = () => {
  showModal.value = false;
};

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
      props.updateImage(imageUrl);
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
  cursor: pointer;
}

.image-preview-title {

  color: #626F7B;
  font-size: 20px;
  font-weight: bold;
}

/* Modal 样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  max-width: 80%;
  max-height: 80%;
}

.modal-content img {
  width: 100%;
  height: auto;
  border: 5px solid #fff;
}
</style>
