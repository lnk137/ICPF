<template>
  <div>
    <!-- 开发时 -->
    <div class="test" v-if="true">
      <div class="title">休息一下，听会儿歌吧</div>
      <audio controls>
        <source
          src="https://api.liumingye.cn/m/api/link?id=d3f636iePH3nJMVUD1wXmSGHhLLowuO8zTtj3D5jYckALink&quality=128&_t=1725619294109&token=20240531.00ca1f7f6c6b649a7ed8f7c6c16d7383"
          type="audio/mpeg"
        />
      </audio>
    </div>
    <!-- 整活时 -->
    <div v-if="false">好奇怪，为什么这里会什么都没有呢，会不会是被藏起来了</div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.title{
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 30px;
}
</style>