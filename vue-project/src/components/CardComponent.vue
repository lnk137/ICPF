<template>
    <div class="card">
      <div class="progress-container">
        <svg class="progress-circle" viewBox="0 0 100 100">
          <!-- 背景圆 -->
          <circle class="background-circle" cx="50" cy="50" r="45" />
          <!-- 前景圆，表示进度 -->
          <circle
            class="foreground-circle"
            cx="50"
            cy="50"
            r="45"
            :style="circleStyle"
          />
        </svg>
        <!-- 中间显示百分比 -->
        <div class="progress-text">
          <p class="percentage">{{ percentage }}%</p>
          <p class="label">{{ label }}</p> <!-- 动态显示传入的标签 -->
        </div>
      </div>
      <!-- 底部的课程描述文字 -->
      <div class="course-title">{{ title }}</div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  
  // 定义接收的 prop
  const props = defineProps({
    percentage: {
      type: Number,
      default: 53.56, // 默认进度百分比
    },
    title: {
      type: String,
      default: '西尔UI设计课程', // 默认课程标题
    },
    label: {
      type: String,
      default: '', // 默认的标签文字
    },
  });
  
  // 计算圆形的样式属性，用于控制进度条的前景圆
  const circleStyle = computed(() => {
    const radius = 45; // 圆的半径
    const circumference = 2 * Math.PI * radius; // 圆的周长
    const offset = circumference - (props.percentage / 100) * circumference; // 计算进度的偏移量
  
    return {
      strokeDasharray: `${circumference}`,
      strokeDashoffset: `${offset}`,
    };
  });
  </script>
  
  <style scoped>
  .card {
    background-color: #E0EDE9;
    width: 200px;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(37, 114, 85, 0.352);
    text-align: center;
    font-family: Arial, sans-serif;
    height: 166px;
  }
  
  .progress-container {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto;
  }
  
  .progress-circle {
    width: 100px;
    height: 100px;
    transform: rotate(-90deg); /* 旋转进度条，使得起点为顶部 */
  }
  
  .background-circle {
    fill: none;
    stroke: #3278522f;
    stroke-width: 10;
  }
  
  .foreground-circle {
    fill: none;
    stroke: #b2889b;
    stroke-width: 10;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.5s ease;
  }
  
  .progress-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .percentage {
    font-size: 23px;
    font-weight: bold;
    color: #333;
  }
  
  .label {
    font-size: 15px;
    color: #999;
  }
  
  .course-title {
    margin-top: 20px;
    font-size: 20px;
    font-weight: bold;
    color: #313440;
  }
  </style>
  