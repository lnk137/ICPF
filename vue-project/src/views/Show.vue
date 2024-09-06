<template>
  <div class="show">
    <div class="title">什么？又有新彩蛋？</div>
    <div>点击后要稍等一会</div>
    <div class="img-container">
      <img :src="imageSrc" alt="你是不是没联网" class="image" @click="handleClick" />
    </div>

  </div>
</template>

<script setup>
import imageSrc from "@/assets/冬天.png"; // 通过import导入图片

// 跳转的处理函数
const handleClick = () => {
  window.location.href = 'https://bruno-simon.com/'; // 跳转到指定链接
};

</script>

<style scoped lang="less">
.show {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.title {
  font-size: 45px;
  font-weight: bold;
  color: #303440;
}
.img-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.image {
  max-height: 350px;
  cursor: pointer;
}

.back-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #45a049;
}
</style>
