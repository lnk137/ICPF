<template>
  <div>
    <!-- 开发时 -->
    <div class="test" v-if="flase">
      <CardComponent class="card"></CardComponent>
      <SimpleCard :title="1" subtitle="content" class="card" />
      <CardComponent class="card"></CardComponent>
      <SimpleCard :title="2" subtitle="content" class="card" />
      <CardComponent>class="card"</CardComponent>
      <SimpleCard :title="3" subtitle="content" class="card" />
    </div>
    <!-- 整活时 -->
     <div v-if="true">好奇怪，为什么这里会什么都没有呢，会不会是被藏起来了</div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.test {
  display: flex;
  flex-wrap: wrap;
}
.card {
  max-width: 200px;
}
</style>