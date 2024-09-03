<template>
  <!-- 按钮模板 -->
  <button class="animated-button" @click="handleClick">
    <!-- 插槽：默认显示“你好，世界” -->
    <span class="button-text"><slot>你好，世界</slot></span>
    <!-- 波纹效果的元素，使用 ref 引用 -->
    <span class="ripple" ref="ripple"></span>
  </button>
</template>

<script>
export default {
  methods: {
    handleClick(event) {
      // 获取当前点击的按钮元素
      const button = event.currentTarget;
      // 获取波纹元素
      const ripple = this.$refs.ripple;

      // 获取按钮的尺寸和位置
      const rect = button.getBoundingClientRect();

      // 计算波纹的尺寸：取按钮宽度和高度的最大值，确保波纹覆盖整个按钮
      const size = Math.max(rect.width, rect.height);
      // 计算波纹的起始位置，使波纹从点击的位置开始扩散
      const x = event.clientX - rect.left - size / 2;
      const y = event.clientY - rect.top - size / 2;

      // 设置波纹元素的宽高和位置
      ripple.style.width = `${size}px`;
      ripple.style.height = `${size}px`;
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;

      // 添加动画类名，触发波纹动画
      ripple.classList.add('animate');
      // 设置一个定时器，在600毫秒后移除动画类名，结束波纹动画
      setTimeout(() => {
        ripple.classList.remove('animate');
      },250); // 控制波纹动画持续时间为600毫秒
    }
  }
};
</script>

<style scoped>
.animated-button {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative; /* 使波纹效果能绝对定位 */
  display: inline-block;
  padding: 10px 20px; /* 内边距，定义按钮尺寸 */
  font-size: 16px; /* 按钮文字大小 */
  background-color: #D9EDE9; /* 按钮背景颜色 */
  border: none; /* 去除边框 */
  border-radius: 10px; /* 圆角效果 */
  cursor: pointer; /* 鼠标悬停时显示为指针 */
  outline: none; /* 去除点击时的轮廓 */
  overflow: hidden; /* 隐藏超出按钮范围的内容，确保波纹不会超出按钮 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 添加变形和阴影的过渡效果 */
}

.animated-button:hover {
  transform: scale(1.05); /* 鼠标悬停时放大按钮 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 鼠标悬停时添加阴影效果 */
}

.button-text {
  color: #000000; /* 按钮文字颜色 */
  position: relative; /* 确保文字在波纹效果之上 */
  z-index: 2; /* 设定更高的层级，使其显示在波纹之上 */
}

.ripple {
  position: absolute; /* 绝对定位 */
  border-radius: 50%; /* 圆形波纹 */
  background: rgba(169, 169, 169, 0.397); /* 波纹颜色，使用半透明灰色 */
  transform: scale(0); /* 初始状态下波纹缩放为0 */
  opacity: 0; /* 初始状态下波纹透明度为0 */
  pointer-events: none; /* 波纹不会影响鼠标事件 */
}

.ripple.animate {
  transform: scale(4); /* 波纹放大4倍 */
  opacity: 1; /* 波纹显示 */
  transition: transform 1s ease, opacity 1s ease; /* 控制波纹动画的持续时间为0.3秒 */
}
</style>
