<template>
  <div class="body">
    <div class="argument">
      <!-- HSV范围 -->
      <div class="HSV-container">
        <div class="input-group">
          <label>H值下限</label>
          <input
            v-model="lowerHue"
            type="number"
            min="0"
            max="255"
            class="custom-input"
          />
        </div>
        <div class="input-group">
          <label>S值下限</label>
          <input
            v-model="lowerSaturation"
            type="number"
            min="0"
            max="255"
            class="custom-input"
          />
        </div>
        <div class="input-group">
          <label>V值下限</label>
          <input
            v-model="lowerValue"
            type="number"
            min="0"
            max="255"
            class="custom-input"
          />
        </div>
        <div class="input-group">
          <label>H值上限</label>
          <input
            v-model="upperHue"
            type="number"
            min="0"
            max="255"
            class="custom-input"
          />
        </div>
        <div class="input-group">
          <label>S值上限</label>
          <input
            v-model="upperSaturation"
            type="number"
            min="0"
            max="255"
            class="custom-input"
          />
        </div>
        <div class="input-group">
          <label>V值上限</label>
          <input
            v-model="upperValue"
            type="number"
            min="0"
            max="255"
            class="custom-input"
          />
        </div>
      </div>
      <!-- 分辨率调整 -->
      <div class="other">
        <div class="resolution-container">
          <label>分辨率大小</label>
          <input
            v-model="resolutionWidth"
            type="number"
            min="1"
            max="2000"
            class="custom-input"
          />
          <label>x</label>
          <input
            v-model="resolutionHeight"
            type="number"
            min="1"
            max="2000"
            class="custom-input"
          />
        </div>
        <div class="soli-container">
          <label>土壤剖面宽度</label>
          <input
            v-model="soilWidth"
            type="number"
            min="1"
            max="1000"
            class="custom-input"
          />
        </div>
        <div class="start-height-container">
          <label>起始高度</label>
          <input
            v-model="startHeight"
            type="number"
            min="0"
            max="20000"
            class="custom-input"
          />
        </div>
      </div>
    </div>
    <div>
      <img :src="tree" alt="树木" class="image" />
    </div>
  </div>
</template>

<script setup>
import tree from "@/assets/树木.png"; // 通过import导入图片
import { ref, onMounted, onUnmounted } from "vue";
// @ts-ignore

// 定义数据
const lowerHue = ref(35);
const lowerSaturation = ref(35);
const lowerValue = ref(35);
const upperHue = ref(255);
const upperSaturation = ref(255);
const upperValue = ref(255);

const resolutionWidth = ref(500); // 默认分辨率宽度
const resolutionHeight = ref(500); // 默认分辨率高度
const soilWidth = ref(500); // 土壤剖面宽度
const startHeight = ref(500); // 起始高度

// 构建数据对象
const getColorRanges = () => {
  return {
    lower_range: [lowerHue.value, lowerSaturation.value, lowerValue.value],
    upper_range: [upperHue.value, upperSaturation.value, upperValue.value],
    resolution: `${resolutionWidth.value}x${resolutionHeight.value}`,
    soil_width: soilWidth.value,
    start_height: startHeight.value,
  };
};

// 发送颜色范围数据
const sendColorRanges = async () => {
  const data = getColorRanges();

  try {
    const response = await fetch("http://localhost:5000/color-ranges", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Failed to send color ranges");
    }

    const result = await response.json();
    console.log("Data sent successfully:", result);
  } catch (error) {
    console.error("An error occurred:", error);
  }
};

// 设置定时器
let intervalId;

onMounted(() => {
  intervalId = setInterval(sendColorRanges, 100000); // 每5秒发送一次数据
});

onUnmounted(() => {
  clearInterval(intervalId); // 组件卸载时清除定时器
});

// 手动触发数据发送
const handleClick = async () => {
  try {
    await sendColorRanges();
    alert("Color ranges sent successfully!");
  } catch (error) {
    alert("Failed to send color ranges.");
    console.error(error);
  }
};
</script>



<style scoped lang="less">
.body {
  font-size: 20px;
  color: #303440;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-wrap: wrap;
  .argument{
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-wrap: wrap;
  margin: 40px 0;
  }
}

.HSV-container {
  display: flex;
  flex-wrap: wrap;
  /* 允许换行 */
  justify-content: center;
  /* 居中显示 */
}

.input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  flex-basis: calc(33.333% - 30px);
  /* 每行3列，减去间距 */
}

label {
  margin-bottom: 8px;
  font-size: 14px;
  color: #606f7b;
  font-weight: 600;
  display: flex;
  justify-content: center;
}

.custom-input {
  width: 50px;
  padding: 8px;
  font-size: 16px;
  border: none;
  /* 去掉边框 */
  border-radius: 8px;
  /* 圆角 */
  background-color: #d8ede9;
  /* 背景色 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 阴影 */
  transition: box-shadow 0.3s ease, background-color 0.3s ease;
  &:hover {
    opacity: 1;
    background-color: rgba(255, 255, 255, 0.664);
    /* 添加hover效果 */
  }
  &:focus {
    outline: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    /* 聚焦时阴影加深 */
    background-color: #eef5f4;
    /* 聚焦时背景色变亮 */
  }
}

.resolution-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  label {
    margin: 0 10px;
  }
}

.soli-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  label {
    margin: 0 10px;
  }
}

.start-height-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  label {
    margin: 0 10px;
  }
}
.other {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.image {
  max-width: 700px;
  position: absolute; /* 将图片绝对定位 */
  bottom: 0; /* 固定到页面底部 */
  left: 250px;
  right: 0;
  opacity: 0.9; /* 如果需要，可以添加透明度效果 */
}
</style>
