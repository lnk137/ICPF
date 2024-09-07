<template>
    <div class="atom-icon">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 100 100"
        class="atom"
      >
        <!-- 核 -->
        <circle cx="50" cy="50" r="10" fill="black" /> <!-- 核稍微变大 -->
        
        <!-- 轨道 1 -->
        <ellipse cx="50" cy="50" rx="35" ry="25" fill="none" stroke="#a940c9" stroke-width="3" />
        
        <!-- 轨道 2 -->
        <ellipse cx="50" cy="50" rx="35" ry="25" fill="none" stroke="#328eea" stroke-width="3" transform="rotate(60 50 50)" />
        
        <!-- 轨道 3 -->
        <ellipse cx="50" cy="50" rx="35" ry="25" fill="none" stroke="#6dc532" stroke-width="3" transform="rotate(120 50 50)" />
      </svg>
    </div>
  </template>
  
  <script setup>
  // 这里不需要额外的逻辑
  </script>
  
  <style scoped>
  .atom-icon {
    color:#a940c9;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 300px; /* 整体增大 */
    height: 300px; /* 整体增大 */
  }
  
  .atom {
    width: 200px; /* 增加图标的宽度 */
    height: 200px; /* 增加图标的高度 */
  }
  </style>
  