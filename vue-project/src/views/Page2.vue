<template>
  <div class="page2">
    <ImageUploader @file-selected="uploadImage" />

    <div v-if="grayscaleImage" class="image-preview">
      <p class="image-preview-title">处理后:</p>
      <img :src="grayscaleImage" alt="Grayscale Image" @click="openImageModal" />
      <!-- 保存图片的图标按钮 -->
      <button class="save-button" @click="saveImage" title="保存图片">
        💾
      </button>
    </div>

    <div v-if="showModal" class="modal" @click="closeImageModal">
      <div class="modal-content">
        <img :src="grayscaleImage" alt="Grayscale Image" />
      </div>
    </div>

    <!-- 引入 Notification 组件 -->
    <Notification :message="notification.message" :type="notification.type" v-if="notification.show" />
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
const notification = ref({ show: false, message: '', type: 'success' });

const openImageModal = () => {
  showModal.value = true;
};

const closeImageModal = () => {
  showModal.value = false;
};

// 显示气泡提示框
const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type };
  setTimeout(() => {
    notification.value.show = false;
  }, 3000); // 3秒后自动隐藏
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
      showNotification('图片上传成功🆗', 'success');
    } else {
      showNotification('上传失败，请重试', 'error');
    }
  } catch (error) {
    showNotification('上传过程中出现错误', 'error');
  }
};

// 发送保存指令到后端
const saveImage = async () => {
  try {
    const response = await fetch("http://localhost:5000/save-image", {
      method: "POST"
    });

    if (response.ok) {
      showNotification('图像已成功保存', 'success');
    } else {
      showNotification('保存失败，请重试', 'error');
    }
  } catch (error) {
    showNotification('保存图像时出错', 'error');
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

.image-preview {
  position: relative;
}

.image-preview img {
  max-width: 400px;
  max-height: 400px;
  border: 1px solid #ccc;
  margin-top: 20px;
  cursor: pointer;
}

.save-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #fff;
}

.image-preview-title {
  color: #626F7B;
  font-size: 20px;
  font-weight: bold;
}

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
