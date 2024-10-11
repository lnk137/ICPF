import { defineStore } from 'pinia';
import { ref } from 'vue';

export const usefileStore = defineStore('fileStore', () => {

  const originalFile = ref(null);  // 用于保存原始文件对象

  // 定义更新原始文件的方法
  const updateOriginalFile = (file) => {
    originalFile.value = file;
    console.log('originalFile.value:', originalFile.value);
  };


  return {
    originalFile,
    updateOriginalFile,
  };
});
