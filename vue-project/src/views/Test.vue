<template>
  <div class="test">
    <ripple-button @click="show" />
    <div class="img">
      <img :src="img_URL" alt="null" v-if="img_URL">
    </div>
  </div> 
</template>

<script setup>
import { ref } from "vue";
const img_URL = ref(null);
const show =async()=>{
  const response = await fetch("http://localhost:5000/show_k_means", {
    method: "POST",
  });

  if(!response.ok){
    console.log("error");
  }
  const blob = await response.blob();
  img_URL.value = URL.createObjectURL(blob);
}

</script>

<style lang="less" scoped>


</style>