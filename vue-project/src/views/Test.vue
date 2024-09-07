<template>
  <div class="show">
    <div class="title">再见小黑🥹</div>
    <div class="img-container">
      <img :src="imageSrc" alt="你是不是没联网" class="image" @click="handleClick" />
    </div>
    <audio controls>
        <source
          src="@/assets/Evan Call - Time Flows Ever Onward.mp3"
          type="audio/mpeg"
        />
      </audio> <atom />

  </div>
</template>

<script setup>
import imageSrc from "@/assets/机器人.jpg"; // 通过import导入图片

// 跳转的处理函数
const handleClick = () => {
  window.location.href = 'https://freepacman.org/'; // 跳转到指定链接
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
