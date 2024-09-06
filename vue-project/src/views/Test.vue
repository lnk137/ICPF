<template>
  <div>
    <!-- 开发时 -->
    <div class="test" v-if="true">
      <div class="title">休息一下，听会儿歌吧</div>
      <audio controls>
        <source
          src="http://music.163.com/song/media/outer/url?id=285005.mp3"
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