<template>
  <div class="body">
    <div class="sidebar">
      <!-- 导入 -->
      <router-link to="/set" class="nav-link">
        <img src="@/assets/参数设置.svg" alt="参数" class="icon" />
        参数调整
      </router-link>
      <!-- 导入 -->
      <router-link to="/upload" class="nav-link">
        <img src="@/assets/上传.svg" alt="导入" class="icon" />
        导入图片
      </router-link>
      <!-- 导入 -->
      <router-link to="/result" class="nav-link">
        <img src="@/assets/结果查看.svg" alt="导入" class="icon" style="scale: 0.8;"/>
        结果查看
      </router-link>

      <!-- <router-link to="/test" class="nav-link">
        <img src="@/assets/训练.svg" alt="导入" class="icon"  />
        模型训练
      </router-link>  -->

    </div>

    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script setup>

</script>


<style scoped lang="less">
@max: 100%;
@sidebar_width: 220px;

.body {
  background-color: #c4d6d0;
  display: flex;
  height: @max;
  width: @max;

  .sidebar {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    width: @sidebar_width;
    height: 100vh;
    background: linear-gradient(#26A484, #26a4a4);
    border-radius: 7px;
    flex: 0 0 auto;
    /* 防止侧边栏被压缩 */
    position: fixed;
    /* 固定在页面左侧 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    /* 添加阴影 */
  }

  .nav-link {
  display: flex;
  height: 15%;
  color: #323440;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none; //去掉下划线
  padding: 10px;
  text-align: center;
  border-radius: 5px;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s, opacity 0.3s, color 0.3s;
}

.nav-link:hover {
  height: 15%;
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.251);
  border-radius: 20px;

  /* 添加hover效果 */
}

.nav-link:focus {
  background-color: rgba(198, 198, 198, 0.201);
  /* 添加按下时的背景色 */
  color: rgb(194, 212, 222);
  /* 改变文字颜色以提高可读性 */
}
.icon {
  margin-top: 5px; /* 控制图标的上边距 */
  width: 35px; /* 控制图标的宽度 */
  height: 35px; /* 控制图标的高度 */
}
  .content {
    flex-grow: 1;

    padding: 20px;
    overflow-y: auto;
    /* 当内容超出时可以滚动 */
    margin-left: @sidebar_width;
    /* 留出侧边栏的空间 */
    // scrollbar-width: thin; /* 针对 Firefox 的滚动条样式 */
  }
}
.icon {
  margin-top: 5px; /* 控制图标的上边距 */
  width: 30px; /* 控制图标的宽度 */
  height: 30px; /* 控制图标的高度 */
}

::-webkit-scrollbar {
    width: 0px; /*对垂直流动条有效*/
    height: 6px; /*对水平流动条有效*/
}

</style>
