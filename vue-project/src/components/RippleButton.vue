<template>
  <!-- 按钮模板，应用自定义样式 -->
  <button 
    class="animated-button" 
    @click="handleClick"
    :style="buttonStyles"
  >
    <!-- 插槽：默认显示“你好，世界” -->
    <span class="button-text" :style="{ color: textColor }">
      <slot>你好，世界</slot>
    </span>
    <!-- 波纹效果的元素，使用 ref 引用 -->
    <span class="ripple" ref="ripple" :style="{ backgroundColor: rippleColor }"></span>
  </button>
</template>

<script setup>
import { ref, computed } from 'vue';

// 定义 ref 引用
const ripple = ref(null);

// 定义 props 以接收样式参数
const props = defineProps({
  backgroundColor: {
    type: String,
    default: '#D9EDE9',
  },
  textColor: {
    type: String,
    default: '#000000',
  },
  borderRadius: {
    type: String,
    default: '10px',
  },
  rippleColor: {
    type: String,
    default: 'rgba(169, 169, 169, 0.397)',
  },
  shadowColor: {
    type: String,
    default: 'rgba(0, 0, 0, 0.1)',
  },
});

// 计算按钮的样式
const buttonStyles = computed(() => ({
  backgroundColor: props.backgroundColor,
  borderRadius: props.borderRadius,
  boxShadow: `0 2px 4px ${props.shadowColor}`,
}));

const handleClick = (event) => {
  const button = event.currentTarget;
  const rect = button.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  const x = event.clientX - rect.left - size / 2;
  const y = event.clientY - rect.top - size / 2;

  if (ripple.value) {
    ripple.value.style.width = `${size}px`;
    ripple.value.style.height = `${size}px`;
    ripple.value.style.left = `${x}px`;
    ripple.value.style.top = `${y}px`;

    ripple.value.classList.add('animate');
    setTimeout(() => {
      ripple.value.classList.remove('animate');
    }, 250);
  }
};
</script>

<style scoped>
.animated-button {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  outline: none;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: none !important; /* 强制移除边框 */
}

.animated-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px;
}

.ripple {
  position: absolute;
  border-radius: 50%;
  transform: scale(0);
  opacity: 0;
  pointer-events: none;
}

.ripple.animate {
  transform: scale(4);
  opacity: 1;
  transition: transform 1s ease, opacity 1s ease;
}
</style>
