<template>
  <div class="body">
    <div class="sidebar">
      <router-link to="/page1" class="nav-link">参数调整</router-link>
      <router-link to="/page2" class="nav-link">导入图片</router-link>
      <router-link to="/page3" class="nav-link">结果查看</router-link>
      <router-link to="/test" class="nav-link">测试页面</router-link>
    </div>

    <div class="content">
      <keep-alive>
        <router-view :grayscaleImage="grayscaleImage" :updateImage="updateImage" />
      </keep-alive>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
// import { RouterView } from "vue-router";

// 定义一个全局状态，用于保存图片
const grayscaleImage = ref<string | null>(null);

// 更新图片的全局状态
const updateImage = (newImage: string) => {
  grayscaleImage.value = newImage;
};
</script>

<style scoped lang="less">
@max: 100%;
@sidebar_width: 220px;

.body {
  background-color: #c4d6d0;
  display: flex;
  height: @max;
  width: @max;
  .sidebar {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    width: @sidebar_width;
    height: 100vh;
    background: linear-gradient(#26A484, #26a4a4);
    border-radius: 7px;
    flex: 0 0 auto; /* 防止侧边栏被压缩 */
    position: fixed; /* 固定在页面左侧 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* 添加阴影 */
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
    transition: background-color 0.3s, opacity 0.3s, color 0.3s;
  }

  .nav-link:hover {
    opacity: 1;
    background-color: rgba(255, 255, 255, 0.251);
    border-radius: 20px;
    /* 添加hover效果 */
  }

  .nav-link:focus {
    background-color: rgba(198, 198, 198, 0.201);
    /* 添加按下时的背景色 */
    color: rgb(194, 212, 222);
    /* 改变文字颜色以提高可读性 */
  }

  .content {
    flex-grow: 1;

    padding: 20px;
    overflow-y: auto; /* 当内容超出时可以滚动 */
    margin-left: @sidebar_width; /* 留出侧边栏的空间 */
  }
}
</style>
