<template>
  <div class="card">
    <div class="progress-container">
      <svg class="progress-circle" viewBox="0 0 100 100">
        <circle class="background-circle" cx="50" cy="50" r="45" />
        <circle
          class="foreground-circle"
          cx="50"
          cy="50"
          r="45"
          :style="circleStyle"
        />
      </svg>
      <div class="progress-text">
        <p class="percentage">{{ percentage }}%</p>
        <p class="label">{{ label }}</p>
      </div>
    </div>
    <div class="course-title">{{ title }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  percentage: Number,
  title: String,
  label: String,
});

const circleStyle = computed(() => {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (props.percentage / 100) * circumference;
  return {
    strokeDasharray: `${circumference}`,
    strokeDashoffset: `${offset}`,
  };
});
</script>

<style scoped>
.card {
  background-color: #e0ede9;
  padding: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
  height: 150px;
  width: 170px;
  flex: 1; /* 让卡片填充父容器的宽度 */
}

.progress-container {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto;
}

.progress-circle {
  width: 100px;
  height: 100px;
  transform: rotate(-90deg);
}

.background-circle {
  fill: none;
  stroke: #3278522f;
  stroke-width: 10;
}

.foreground-circle {
  fill: none;
  stroke: #b2889b;
  stroke-width: 10;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.percentage {
  font-size: 23px;
  font-weight: bold;
  color: #333;
}

.label {
  font-size: 15px;
  color: #999;
}

.course-title {
  margin-top: 20px;
  font-size: 20px;
  font-weight: bold;
  color: #313440;
}
</style>
