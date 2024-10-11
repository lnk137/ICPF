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
  };
});
