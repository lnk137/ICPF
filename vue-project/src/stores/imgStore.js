import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useStore = defineStore('useStore', () => {
  const grayscaleImage = ref(null);
  const original_img = ref(null);
  const k_means_img = ref(null);

  // 更新灰度图像的方法
  const updateGrayscaleImage = (newImage) => {
    grayscaleImage.value = newImage;
    console.log('grayscaleImage.value:', grayscaleImage.value);
  };

  // 更新原始图像的方法
  const updateOriginalImage = (newImage) => {
    original_img.value = newImage;
    console.log('original_img.value:', original_img.value);
  };

  // 更新 K-Means 图像的方法
  const updateKMeansImage = (newImage) => {
    k_means_img.value = newImage;
    console.log('k_means_img.value:', k_means_img.value);
  };

  return {
    grayscaleImage,
    original_img,
    k_means_img,
    updateGrayscaleImage,
    updateOriginalImage,
    updateKMeansImage
  };
});
