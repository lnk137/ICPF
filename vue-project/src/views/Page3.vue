<template>
  <div class="page3">
    <!-- 显示黑色区域面积 -->
    <div v-if="loading" class="loading">
      <WifiLoader text="加载中..." />
    </div>
    <div v-else class="result">
      <CardComponent :percentage="blackRatio*100" title="染色面积比" label="" />
      <SimpleCard :title="`${blackArea} cm²`" subtitle="染色面积" />

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import WifiLoader from '@/components/WifiLoader.vue'; // 引入加载动画组件
import axios from 'axios';  // 使用 axios 或其他工具从后端获取数据

// 定义响应式变量
const blackArea = ref(null);  // 黑色区域面积
const blackRatio = ref(null);  // 黑色像素比例
const loading = ref(false);  // 数据加载状态，默认不显示加载

// 获取数据的函数
const fetchBlackAreaData = async () => {
  loading.value = true;  // 开始获取数据，显示加载动画

  try {
    // 模拟从后端获取数据的异步操作
    const response = await axios.get('http://localhost:5000/show-data');
    // 假设后端返回的响应中包含 blackArea 和 blackRatio
    blackArea.value = response.data.black_area;
    blackRatio.value = response.data.black_ratio;
    if (blackArea.value && blackRatio.value) {
      loading.value = false;
    }
  } catch (error) {
    console.error('数据获取失败: ', error);
  } 
};

// 页面加载时触发数据获取
onMounted(() => {
  fetchBlackAreaData();
});
</script>
<style scoped>
.page3 {
  display: flex;
  align-content: center;
  justify-content: center;
}
.result{
  display: flex;
  gap: 20px; /* 可以调整卡片之间的间距 */
}
.loading {
  position: absolute; 
  left: 558px;
  right: 0;
  top:300px;
}

</style>