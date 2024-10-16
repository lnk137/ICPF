<template>
    <div class="body">
      <!-- 启动画面 -->
      <div v-if="showSplashScreen" class="splash-screen" :style="{ background: randomGradient }">
        <div class="splash-content">
          <!-- 使用 Atom 组件作为 Logo -->
          <Atom class="logo" />
          <h1 class="software-name">ICPWF</h1>
          <p class="version">V1.1.0-beta</p>
          <div class="progress-bar">
            <div class="progress"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from "vue";
  import { useRouter } from "vue-router";
  
  // 启动动画状态
  const showSplashScreen = ref(true);
  const randomGradient = ref("");
  
  // 路由实例
  const router = useRouter();
  
  const gradients = [
    "linear-gradient(45deg, #ff6347, #47baff)",  // 番茄红 (#ff6347) 和 天蓝色 (#47baff)
    "linear-gradient(45deg, #ffcc00, #0033ff)",  // 金黄色 (#ffcc00) 和 深蓝色 (#0033ff)
    "linear-gradient(45deg, #ff7f50, #507fff)",  // 珊瑚橙 (#ff7f50) 和 淡蓝色 (#507fff)
    "linear-gradient(45deg, #ff4500, #00ffb4)",  // 橙红色 (#ff4500) 和 青绿色 (#00ffb4)
    "linear-gradient(45deg, #800080, #ffff00)",  // 紫色 (#800080) 和 黄色 (#ffff00)
    "linear-gradient(45deg, #ff0000, #00ffff)",  // 红色 (#ff0000) 和 青色 (#00ffff)
  ];
  
  // 选择随机颜色渐变
  const setRandomGradient = () => {
    const randomIndex = Math.floor(Math.random() * gradients.length);
    randomGradient.value = gradients[randomIndex];
  };
  
  onMounted(() => {
    // 设置随机渐变背景
    setRandomGradient();
  
    // 模拟加载时间，3秒后隐藏启动动画并跳转路由
    setTimeout(() => {
      showSplashScreen.value = false;
      router.push("/set"); // 跳转到目标页面
    }, 3000);
  });
  </script>
  
  <style scoped lang="less">
  /* 启动动画 */
  .splash-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 9999; /* 保证启动动画在最上层 */
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .splash-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
  }
  
  .logo {
    width: 150px;
    height: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 50px;
    animation: rotateScale 3s infinite;
  }
  
  .software-name {
    font-size: 3rem;
  }
  
  .version {
    font-size: 1.5rem;
  }
  
  /* 进度条样式 */
  .progress-bar {
    width: 300px;
    height: 10px;
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 5px;
    margin-top: 20px;
    overflow: hidden;
  }
  
  .progress {
    height: 100%;
    width: 0;
    background-color: white;
    animation: loadProgress 3s linear forwards, pulseEffect 1.5s infinite;
  }
  
  /* 旋转和缩放动画 */
  @keyframes rotateScale {
    0% { transform: rotate(0deg) scale(1); }
    65% { transform: rotate(180deg) scale(1.7); }
    100% { transform: rotate(360deg) scale(1.2); }
  }
  
  /* 进度条加载动画 */
  @keyframes loadProgress {
    0% { width: 0%; }
    100% { width: 100%; }
  }
  
  /* 进度条闪烁效果 */
  @keyframes pulseEffect {
    0% { opacity: 1; }
    30% { opacity: 0.3; }
    50% { opacity: 0.6; }
    80% { opacity: 0.3; }
    100% { opacity: 1; }
  }
  </style>
  