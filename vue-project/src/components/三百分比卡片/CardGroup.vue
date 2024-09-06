<template>
    <div class="card-group">
      <!-- 使用 v-for 循环遍历传入的数据，并传递给 Temp 组件 -->
      <Temp v-for="(card, index) in cards" 
            :key="index"
            :percentage="card.percentage" 
            :title="card.title" 
            :label="card.label" />
    </div>
  </template>
  
  <script setup>
  
  // 定义 props 用于接收参数
  const props = defineProps({
    cards: {
      type: Array,
      required: true, // 数组是必需的
      default: () => [],
    }
  });
  </script>
  
  <style scoped>
  .card-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0;
    padding: 0;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(37, 114, 85, 0.352);
    overflow: hidden;
  }
  </style>
  