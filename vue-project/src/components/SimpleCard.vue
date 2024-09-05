<template>
    <div class="card">
      <!-- 卡片的标题 -->
      <div class="card-title">{{ title }}</div>
      <!-- 卡片的副标题 -->
      <div class="card-subtitle">{{ subtitle }}</div>
    </div>
  </template>
  
  <script setup>
  // 定义props来接收父组件传入的标题和副标题
  const props = defineProps({
    title: {
      type: String,
      default: 'Illustrator', // 默认标题
    },
    subtitle: {
      type: String,
      default: 'Arial', // 默认副标题
    },
  });
  </script>
  
  <style scoped>
  /* 卡片样式 */
  .card {
    background-color: #E0EDE9;
    width: 200px;
    height: 166px;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(37, 114, 85, 0.352);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-family: Arial, sans-serif;
  }
  
  /* 标题样式 */
  .card-title {
    font-size: 24px;
    font-weight: bold;
    color: #303440;
    margin-bottom: 20px;
  }
  
  /* 副标题样式 */
  .card-subtitle {
    font-size: 17px;
    color: #54575f;
  }
  </style>
  