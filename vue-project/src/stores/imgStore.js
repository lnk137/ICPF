import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useImgStore = defineStore('useStore', () => {
  const grayscaleImage = ref(null);  // 用于存储灰度图像
  const original_img = ref(null);    // 用于存储原始图像
  const gb_kimg = ref(null);         // 用于存储高斯模糊的 K-means 图像
  const no_gb_kimg = ref(null);      // 用于存储未模糊的 K-means 图像

  // 更新灰度图像的方法
  const updateGrayscaleImage = (newImage) => {
    grayscaleImage.value = newImage;
    console.log('grayscaleImage.value已更新:', grayscaleImage.value);
  };

  // 更新原始图像的方法
  const updateOriginalImage = (newImage) => {
    original_img.value = newImage;
    console.log('original_img.value:', original_img.value);
  };

  // 更新高斯模糊的 K-means 图像的方法
  const updateGBImage = (newImage) => {
    gb_kimg.value = newImage;
    console.log('gb_kimg.value:', gb_kimg.value);
  };

  // 更新未模糊的 K-means 图像的方法
  const updateNoGBImage = (newImage) => {
    no_gb_kimg.value = newImage;
    console.log('no_gb_kimg.value:', no_gb_kimg.value);
  };

  return {
    grayscaleImage,
    original_img,
    gb_kimg,
    no_gb_kimg,
    updateGrayscaleImage,
    updateOriginalImage,
    updateGBImage,
    updateNoGBImage,
  };
});
