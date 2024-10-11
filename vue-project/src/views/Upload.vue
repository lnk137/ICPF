<template>
  <div class="page2">
    <ImageUploader @file-selected="uploadImage" />

    <div v-if="imageStore.grayscaleImage" class="image-preview">
      <div class="tip">
        <p class="image-preview-title">处理后:</p>
        <div class="icon_area">
          <img src="@/assets/保存.svg" alt="保存" class="icon" @click="saveImage" style="scale: 1.1;" />
          <img src="@/assets/切换.svg" alt="切换" class="icon" @click="switching_state" />
        </div>
      </div>
      <img v-if="!isKImg" :src="imageStore.grayscaleImage" alt="Grayscale Image" @click="openImageModal" />
      <img v-else :src="imageStore.k_means_img" alt="K-means Image" @click="openImageModal" />

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useImgStore } from '@/stores/imgStore';
import { usefileStore } from '@/stores/fileStore';
import { useSettingsStore } from '@/stores/settingsStore';

const imageStore = useImgStore();
const fileStore = usefileStore();
const settingsStore = useSettingsStore();

// 上传原始图像，获得灰度图
const uploadImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);
    imageStore.updateOriginalImage(URL.createObjectURL(file));
    fileStore.updateOriginalFile(file);

    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      imageStore.updateGrayscaleImage(imageUrl);
      showKImg();
    }
  } catch (error) {
    console.error('上传过程中出现错误:', error);
  }
};
// 保存图像
const saveImage = async () => {
  try {
    const response = await fetch("http://localhost:5000/save-image", {
      method: "POST"
    });

    if (!response.ok) {
      console.error('保存失败，请重试');
    }
  } catch (error) {
    console.error('保存图像时出错:', error);
  }
};
//发送原始图像，获取kmeans图像
const showKImg = async () => {
  console.log("showKImg处理中");
  const formData = new FormData();
  formData.append("file", fileStore.originalFile);

  const response = await fetch("http://localhost:5000/k_means", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    console.log("error");
  }
  const blob = await response.blob();
  imageStore.updateKMeansImage(URL.createObjectURL(blob));
}
// 切换显示的图像
const isKImg = ref(false);
const switching_state = () => {
  console.log("switching_state");
  isKImg.value = !isKImg.value;
}
//页面挂载时，更新参数，重新处理原始图像
onMounted(() => {
  if (imageStore.original_img) {
    settingsStore.sendColorRanges()
    uploadImage(fileStore.originalFile);
  }
});
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
  margin-top: 20px;

}

.save-button {
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
  margin-top: 20px;
}

.tip {
  display: flex;

}

.icon_area {
  display: flex;
  margin-left: 280px;
}

.icon {
  width: 30px;
  height: 30px;
  margin-left: 6px;
  cursor: pointer;
}
</style>
