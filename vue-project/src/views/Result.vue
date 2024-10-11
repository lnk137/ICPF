<template>
  <div class="page3">
    <!-- 显示黑色区域面积 -->
    <div v-if="loading" class="loading">
      <WifiLoader text="请先导入图片..." />
    </div>
    <div v-else class="result">
      <CardGroup :cards="cardData" />
      <SimpleCard :title="`${blackArea} cm²`" subtitle="染色面积" />
      <SimpleCard :title="`${matrix_flow_depth} cm`" subtitle="基质流深度" />
      <SimpleCard :title="`${maximum_staining_depth} cm`" subtitle="最大染色深度" />
      <SimpleCard :title="`${length_index} `" subtitle="长度指数" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import WifiLoader from '@/components/WifiLoader.vue'; // 引入加载动画组件
import axios from 'axios';  // 使用 axios 或其他工具从后端获取数据

// 定义响应式变量
const blackArea = ref(null);  // 染色面积
const blackRatio = ref(null);  // 染色面积比
const matrix_flow_depth = ref(null); //基质流深度
const priority_flow_percentage = ref(null);  // 优先流百分数
const priority_staining_area = ref(null);  // 优先染色面积比
const maximum_staining_depth = ref(null);  // 最大染色深度
const length_index = ref(null);  // 长度指数

const loading = ref(false);  // 数据加载状态，默认不显示加载

// 定义 cardData 为响应式数组
const cardData = ref([]); 

// 获取数据的函数
const fetchBlackAreaData = async () => {
  loading.value = true;  // 开始获取数据，显示加载动画

  try {
    // 模拟从后端获取数据的异步操作
    const response = await axios.get('http://localhost:5000/show-data');
    const parameters = [
      response.data.black_area,
      response.data.black_ratio,
      response.data.matrix_flow_depth,
      response.data.priority_flow_percentage,
      response.data.priority_staining_area,
      response.data.maximum_staining_depth,
      response.data.length_index
    ];

    // 使用 every() 判断是否所有参数都不为空
    const allParametersExist = parameters.every(param => param !== null && param !== undefined && param !== '');

    if (allParametersExist) {
      blackArea.value = response.data.black_area;
      blackRatio.value = response.data.black_ratio;
      matrix_flow_depth.value = response.data.matrix_flow_depth;
      priority_flow_percentage.value = response.data.priority_flow_percentage;
      priority_staining_area.value = response.data.priority_staining_area;
      maximum_staining_depth.value = response.data.maximum_staining_depth;
      length_index.value = response.data.length_index;

      // 在数据获取成功后，更新 cardData
      cardData.value = [
        { percentage: blackRatio.value, title: "染色面积比" },
        { percentage: priority_flow_percentage.value, title: "优先流百分数" },
        { percentage: priority_staining_area.value, title: "优先染色面积比" }
      ];
      loading.value = false;
    } else {
      console.log("有参数为空");
    }
    if (response.ok) {
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
}
.result{
  display: flex;
  align-content: center;
  justify-content: center;
  flex-wrap:wrap;
  gap: 60px; /* 可以调整卡片之间的间距 */
}
.loading {
  position: absolute; 
  left: 558px;
  right: 0;
  top:300px;
}
</style>
