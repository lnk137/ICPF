<template>
    <div v-if="show" class="notification" :class="type">
      {{ message }}
    </div>
  </template>
  
  <script setup>
  import { ref, watchEffect } from 'vue';
  
  const props = defineProps({
    message: String,
    type: {
      type: String,
      default: 'success'
    },
    duration: {
      type: Number,
      default: 3000 // 默认3秒自动消失
    }
  });
  
  const show = ref(false);
  
  watchEffect(() => {
    if (props.message) {
      show.value = true;
      setTimeout(() => {
        show.value = false;
      }, props.duration);
    }
  });
  </script>
  
  <style scoped lang="less">
  .notification {
  position: fixed;
  top: 10px;
  left: 56%;
  width: 170px;
  height: 40px;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 20px;
  text-align: center;
  font-weight: bold;
  z-index: 1000;
  transition: opacity 0.5s ease-in-out;
  /* 使用flexbox布局使文字上下居中 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification.success {
  background-color: #307b6baf;
  color: white;
}

.notification.error {
  background-color: #ff5e00b3;
  color: white;
}

  </style>
  