<template>
    <div class="percentage-group">
      <div class="percentage-item" v-for="(percentage, index) in percentages" :key="index">
        <div class="circle-chart">
          <!-- 这里可以使用 SVG 或 Canvas 来绘制圆形图表 -->
          <div class="percentage-value">{{ percentage.value }}%</div>
        </div>
        <div class="percentage-label">{{ percentage.label }}</div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from "vue";
  
  // 接收父组件传递的百分比数据
  const props = defineProps({
    percentages: {
      type: Array,
      required: true,
      default: () => [
        { value: 0, label: '标签1' },
        { value: 0, label: '标签2' },
        { value: 0, label: '标签3' }
      ]
    }
  });
  </script>
  
  <style scoped>
  .percentage-group {
    display: flex;
    justify-content: space-around;
    align-items: center;
    gap: 20px; /* 调整每个百分比之间的距离 */
  }
  
  .percentage-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .circle-chart {
    width: 100px;
    height: 100px;
    background-color: #f5f5f5;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .percentage-value {
    font-size: 24px;
    font-weight: bold;
  }
  
  .percentage-label {
    margin-top: 10px;
    font-size: 16px;
    text-align: center;
  }
  </style>
  