<template>
  <div class="clash-wrapper">
    <div class="sidebar">
      <router-link to="/page1" class="nav-link">参数调整</router-link>
      <router-link to="/page2" class="nav-link">导入图片</router-link>
      <router-link to="/page3" class="nav-link">结果查看</router-link>
    </div>

    <div class="content">
      <!-- 使用 RouterView 传递全局图片状态 -->
      <RouterView :grayscaleImage="grayscaleImage" @update-image="updateImage" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterView } from 'vue-router';

// 定义一个全局状态，用于保存图片
const grayscaleImage = ref<string | null>(null);

// 更新图片的全局状态
const updateImage = (newImage: string) => {
  grayscaleImage.value = newImage;
};
</script>

<style scoped lang="less">
@max: 100%;

.clash-wrapper {
  display: flex;
  height: @max;
  width: @max;

  .sidebar {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    width: 30vh;
    background: linear-gradient(#26A484, #26a4a4);
  }

  .nav-link {
    display: flex;
    height: 20%;
    color: rgb(48, 52, 64);
    font-size: 30px;
    font-weight: bold;
    text-decoration: none; //去掉下划线
    padding: 10px;
    text-align: center;
    border-radius: 5px;
    justify-content: center;
    flex-direction: column;
    transition: background-color 0.3s, opacity 0.3s;
  }

  .nav-link:hover {
    opacity: 1;
    background-color: rgba(255, 255, 255, 0.251);
    /* 添加hover效果 */
  }

  .nav-link:focus {
    background-color: rgba(198, 198, 198, 0.201);
    /* 添加按下时的背景色 */
    color: rgb(216, 220, 231);
    /* 改变文字颜色以提高可读性 */
  }

  .content {
    flex-grow: 1;
    background-color: #c4d6d0;
    padding: 20px;
  }
}
</style>
