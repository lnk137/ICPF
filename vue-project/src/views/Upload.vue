<template>
  <div class="page2">
    <ImageUploader @file-selected="uploadImage" />

    <div v-if="imageStore.grayscaleImage" class="image-preview">
      <div class="tip">
        <p class="image-preview-title">处理后:</p>
        <div class="icon_area">
          <img src="@/assets/保存.svg" alt="保存" class="icon" @click="saveImage" style="scale: 1.1;" title="保存图像" />
          <img src="@/assets/切换.svg" alt="切换" class="icon" @click="switching_state" title="切换k-means图" />
        </div>
      </div>
      <div class="showGrayscaleImage" v-if="!isKImg">
        <img :src="imageStore.grayscaleImage"  @click="openImageModal" />
        <div class="eye">
          <img src="@/assets/表格.svg" alt="模糊" class="icon" @click="save_excel" tabindex="0" title="导出像素矩阵" />
        </div>
      </div>
      <div v-if="isKImg" class="k_area">
        <img :src="k_img" alt="K-means Image" @click="openImageModal" />
        <div class="eye">
          <img src="@/assets/眼睛.svg" alt="模糊" class="icon" style="scale: 1.2;" @click="applyGB" tabindex="0"
            title="切换高斯模糊效果" />
        </div>
        <div v-for="(color_ifo, index) in color_ifos" :key="index" class="color_ifos">
          <div class="ifo"
            :style="{ backgroundColor: color_ifo.hex_color, height: '25px', width: '25px', border: '3px solid #f1f1f1' }">
          </div>
          <div class="ifo-text">
            <span>染色面积为: {{ color_ifo.area }}cm²</span><br />
            <span>染色比例为: {{ color_ifo.ratio }}%</span>
          </div>
        </div>
      </div>
    </div>
    <div v-if="isWait" class="wait" style="scale: 2;">
        <Loader />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useImgStore } from '@/stores/imgStore';
import { usefileStore } from '@/stores/fileStore';
import { useSettingsStore } from '@/stores/settingsStore';

const imageStore = useImgStore();
const fileStore = usefileStore();
const settingsStore = useSettingsStore();
const isWait = ref(false);

const line_img=ref(null);
const uploadImage = async (file) => {
  try {
    isWait.value = true;
    const formData = new FormData();
    formData.append("file", file);
    imageStore.updateOriginalImage(URL.createObjectURL(file));
    //更新原始文件
    fileStore.updateOriginalFile(file);

    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    if(!response.ok){
      console.log("上传失败，请重试");
    }
    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);
    line_img.value = imageUrl;
    imageStore.updateGrayscaleImage(imageUrl);
    showKImg();
    isWait.value = false;
  } catch (error) {
    console.error('上传过程中出现错误:', error);
  }
};
// 保存图像
const saveImage = async () => {
  try {
    const response = await fetch("http://localhost:5000/save-image", {
      method: "POST"
    });

    if (!response.ok) {
      console.error('保存失败，请重试');
    }
  } catch (error) {
    console.error('保存图像时出错:', error);
  }
};

// 保存excel
const save_excel = async () => {
  const response = await fetch("http://localhost:5000/save_excel", {
    method: "POST"
  });
  if (!response.ok) {
    console.error('保存失败，请重试');
  }
};
// kmeans处理
const showKImg = async () => {
  console.log("showKImg处理中");
  const formData = new FormData();
  formData.append("file", fileStore.originalFile);

  const response = await fetch("http://localhost:5000/k_means", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    console.log("error");
  }
  // const blob = await response.blob();
  // imageStore.updateKMeansImage(URL.createObjectURL(blob));
  const data = await response.json();
  const gbImgBlob = new Blob([new Uint8Array(data.GB_Img.split('').map(c => c.charCodeAt(0)))], { type: 'image/png' });
  const noGbImgBlob = new Blob([new Uint8Array(data.NO_GB_Img.split('').map(c => c.charCodeAt(0)))], { type: 'image/png' });

  const gbImgUrl = URL.createObjectURL(gbImgBlob);
  const noGbImgUrl = URL.createObjectURL(noGbImgBlob);
  imageStore.updateGBImage(gbImgUrl);
  imageStore.updateNoGBImage(noGbImgUrl);
  k_img.value = noGbImgUrl;
}

// 获取kmeans参数
const color_ifos = ref([]);
const getKMeansParams = async () => {
  const response = await fetch("http://localhost:5000/get_color_ifos", {
    method: "POST",
  });
  if (!response.ok) {
    console.log("error");
  }
  const data = await response.json();
  color_ifos.value = data.color_ifos;
  console.log(color_ifos.value);
}

// 切换显示
const isKImg = ref(false);
const switching_state = () => {
  console.log("switching_state");
  if (imageStore.no_gb_kimg) {
    isKImg.value = !isKImg.value;
  }
  getKMeansParams();
}

// 启用模糊效果
const k_img = ref(imageStore.no_gb_kimg);
const isGB_Img = ref(false);
const applyGB = () => {
  console.log("applyGB");
  if (!isGB_Img.value) {
    k_img.value = imageStore.gb_kimg;
    isGB_Img.value = !isGB_Img.value;
  } else {
    k_img.value = imageStore.no_gb_kimg;
    isGB_Img.value = !isGB_Img.value;
  }
}
onMounted(() => {
  if (settingsStore.isSetUpdate) {
    settingsStore.sendColorRanges()
    uploadImage(fileStore.originalFile);
    settingsStore.updateIsSetUpdate(false);
  }
});
</script>

<style scoped lang="less">
.page2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.image-preview img {
  max-width: 400px;
  max-height: 400px;
  margin-top: 20px;
}

.image-preview-title {
  color: #626F7B;
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
}

.tip {
  display: flex;
}

.icon_area {
  display: flex;
  margin-left: 280px;
}

.icon {
  width: 30px;
  height: 30px;
  margin-left: 6px;
  cursor: pointer;
  transition: transform 0.3s;

  /* 添加过渡效果 */
  &:hover {
    transform: scale(1.1);
    /* 使用 transform 实现缩放 */
  }
}

.color_ifos {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.ifo {
  margin-right: 10px;
}

.ifo-text {
  font-size: 14px;
  font-weight: bold;
  color: #333440;
  line-height: 1.5;
}

.eye {
  position: relative;
  bottom: 400px;
  right: 50px;

}
.wait{
  position: absolute;
  right: 390px;
  top: 460px;
}
</style>
