<template>
    <div
      class="upload-area"
      @dragover.prevent
      @dragenter.prevent
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <p style="color: #626F7B;font-weight: 600;">将图片拖拽到此处或者 <em class="clickable">点击上传</em></p>
      <input
        type="file"
        ref="fileInput"
        @change="handleFileChange"
        accept="image/png, image/jpeg"
        style="display: none"
      />
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const fileInput = ref(null);
  const emit = defineEmits(['file-selected']);
  
  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && (file.type === "image/png" || file.type === "image/jpeg")) {
      emit('file-selected', file);
    }
  };
  
  const triggerFileInput = () => {
    fileInput.value.click();
  };
  
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      emit('file-selected', file);
    }
  };
  </script>
  
  <style scoped lang="less">
  .upload-area {
    width: 500px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-bottom: 20px;
    border-radius: 50px;
    background: #dfede9;
    box-shadow: 2px 2px 10px #9cd1c0;
    transition: background-color 0.3s, opacity 0.3s;
  }
  
  .upload-area:hover {
    opacity: 1;
    background-color: rgba(255, 255, 255, 0.712);
  }
  
  .upload-area p {
    text-align: center;
    color: #666;
  }
  
  .clickable {
    text-decoration: underline;
    color: rgb(41, 172, 73);
  }
  </style>
  