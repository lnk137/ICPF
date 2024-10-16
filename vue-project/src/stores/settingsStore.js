import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSettingsStore = defineStore('settingsStore', () => {
  const lowerHue = ref(35);
  const lowerSaturation = ref(35);
  const lowerValue = ref(35);
  const upperHue = ref(255);
  const upperSaturation = ref(255);
  const upperValue = ref(255);
  const resolutionWidth = ref(500);
  const resolutionHeight = ref(500);
  const soilWidth = ref(50);
  const startHeight = ref(0);

  const isSetUpdate = ref(false);
  // 定义更新方法
  const updateLowerHue = (value) => (lowerHue.value = value);
  const updateLowerSaturation = (value) => (lowerSaturation.value = value);
  const updateLowerValue = (value) => (lowerValue.value = value);
  const updateUpperHue = (value) => (upperHue.value = value);
  const updateUpperSaturation = (value) => (upperSaturation.value = value);
  const updateUpperValue = (value) => (upperValue.value = value);
  const updateResolutionWidth = (value) => (resolutionWidth.value = value);
  const updateResolutionHeight = (value) => (resolutionHeight.value = value);
  const updateSoilWidth = (value) => (soilWidth.value = value);
  const updateStartHeight = (value) => (startHeight.value = value);
  const updateIsSetUpdate = (value) => (isSetUpdate.value = value);
  // 获取颜色范围数据对象
  const getColorRanges = () => {
    return {
      lower_range: [lowerHue.value, lowerSaturation.value, lowerValue.value],
      upper_range: [upperHue.value, upperSaturation.value, upperValue.value],
      resolution: [resolutionWidth.value, resolutionHeight.value], // 将分辨率改为数组形式
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
      console.log("参数发送成功:", result);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return {
    lowerHue,
    lowerSaturation,
    lowerValue,
    upperHue,
    upperSaturation,
    upperValue,
    resolutionWidth,
    resolutionHeight,
    soilWidth,
    startHeight,
    updateLowerHue,
    updateLowerSaturation,
    updateLowerValue,
    updateUpperHue,
    updateUpperSaturation,
    updateUpperValue,
    updateResolutionWidth,
    updateResolutionHeight,
    updateSoilWidth,
    updateStartHeight,
    getColorRanges,  // 将 getColorRanges 函数暴露出来（可选）
    sendColorRanges, // 暴露 sendColorRanges 函数用于发送数据
    isSetUpdate,
    updateIsSetUpdate,
  };
});
