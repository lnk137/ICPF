<template>
  <div class="show">
    <div class="title">这个页面，你只会见到一次</div>
    <div class="title">哈   哈   哈   哈</div>
    <div class="title">因为这只是个欢迎页面</div>
    <div class="title">你不可能在这里停留太久，并且再也回不到这里</div>
    <div>
        <img :src="imageSrc" alt="想" class="image" />
    </div>
  </div>
</template>

<script setup>
import imageSrc from '@/assets/芙莉莲旷工.jpg'; // 通过import导入图片
</script>

<style scoped lang="less">
.show {
display: flex;
flex-direction: column;
}
.title {
    font-size: 45px;
    font-weight: bold;
    color:#303440;
}
.image{
    max-height: 350px;
}
</style>