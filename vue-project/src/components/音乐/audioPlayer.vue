<template>
    <div>
      <audio @timeupdate="updateProgress" controls ref="audioRef" style="display: none">
        <source :src="fileurl" type="audio/mpeg" />
        您的浏览器不支持音频播放
      </audio>
      <div class="audio-right">
        <i :class="audioStatus !== 'pause' ? 'iconfont icon-bofang' : 'iconfont icon-zanting'" @click="playAudio" class="dialogAudioPlay"></i>
        <div class="progress-bar-bg" id="progressBarBg" v-dragto="setAudioIcon">
          <div class="progress-bar" id="progressBar"></div>
        </div>
        <div class="audio-time" style="min-height: 10px">
          <span class="audio-length-current" id="audioCurTime">{{ audioStart }}</span
          >/
          <span class="audio-length-total">{{ duration }}</span>
        </div>
        <div class="volume">
          <div
            @click.stop="
              () => {
                return false
              }
            "
            class="volume-progress"
            v-show="audioHuds"
          >
            <div class="volume-bar-bg" id="volumeBarBg" v-adjuster="handleShowMuteIcon">
              <div class="volume-bar" id="volumeBar"></div>
            </div>
          </div>
          <i class="iconfont pl-1" :class="audioIcon" @click.stop="audioHuds = !audioHuds"> </i>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      fileurl: {
        trpe: String
      }
    },
    data() {
      return {
        audioStatus: 'play',
        audioStart: '0:00',
        duration: '0:00',
        audioVolume: 0.5,
        audioHuds: false
      }
    },
  
    directives: {
      dragto: {
        inserted: function (el, binding, vnode) {
          el.addEventListener(
            'click',
            (e) => {
              let wdiv = document.getElementById('progressBarBg').clientWidth
              let audio = vnode.context.$refs.audioRef
              // 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
              let ratemin = e.offsetX / wdiv
              let rate = ratemin * 100
              document.getElementById('progressBar').style.width = rate + '%'
              audio.currentTime = audio.duration * ratemin
              audio.play()
              binding.value()
            },
            false
          )
        }
      },
      adjuster: {
        inserted: function (el, binding, vnode) {
          el.addEventListener(
            'click',
            (e) => {
              let hdiv = document.getElementById('volumeBarBg').clientHeight
              let audio = vnode.context.$refs.audioRef
              // 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
              let ratemin = e.offsetY / hdiv
              let rate = ratemin * 100
              document.getElementById('volumeBar').style.height = rate + '%'
              audio.volume = ratemin
              binding.value(rate / 100)
            },
            false
          )
        }
      }
    },
    computed: {
      audioIcon() {
        if (this.audioHuds) {
          return this.audioVolume < 0.01 ? 'checked icon-jingyin' : 'checked icon-shengyin'
        } else {
          return 'icon-shengyin'
        }
      }
    },
    mounted() {
      this.fetch()
    },
    methods: {
      fetch() {
        let that = this
        var myVid = this.$refs.audioRef
        myVid.loop = false
        // 监听音频播放完毕
        myVid.addEventListener(
          'ended',
          function () {
            that.audioStatus = 'play' // 显示播放icon
            document.getElementById('progressBar').style.width = '0%' // 进度条初始化
          },
          false
        )
        if (myVid != null) {
          myVid.oncanplay = function () {
            that.duration = that.transTime(myVid.duration) // 计算音频时长
          }
          myVid.volume = 0.5 // 设置音量50%
        }
      },
      // 播放暂停控制
      playAudio() {
        let recordAudio = this.$refs.audioRef // 获取audio元素
        if (recordAudio.paused) {
          recordAudio.play()
          this.audioStatus = 'pause'
        } else {
          recordAudio.pause()
          this.audioStatus = 'play'
        }
      },
      // 更新进度条与当前播放时间
      updateProgress(e) {
        var value = e.target.currentTime / e.target.duration
        if (document.getElementById('progressBar')) {
          document.getElementById('progressBar').style.width = value * 100 + '%'
          if (e.target.currentTime === e.target.duration) {
            this.audioStatus = 'pause'
          }
        } else {
          this.audioStatus = 'pause'
        }
  
        this.audioStart = this.transTime(this.$refs.audioRef.currentTime)
      },
      /**
       * 音频播放时间换算
       * @param {number} value - 音频当前播放时间，单位秒
       */
      transTime(time) {
        var duration = parseInt(time)
        var minute = parseInt(duration / 60)
        var sec = (duration % 60) + ''
        var isM0 = ':'
        if (minute === 0) {
          minute = '00'
        } else if (minute < 10) {
          minute = '0' + minute
        }
        if (sec.length === 1) {
          sec = '0' + sec
        }
        return minute + isM0 + sec
      },
      setAudioIcon() {
        this.audioStatus = 'pause'
      },
      handleShowMuteIcon(val) {
        this.audioVolume = val
      }
    }
  }
  </script>
  
  <style lang="less"  scoped>
  .volume {
    position: relative;
    .volume-progress {
      position: absolute;
      top: -150px;
      width: 32px;
      height: 140px;
      background: #f6f6f6;
      border-radius: 4px;
      padding-top: 10px;
    }
    .volume-bar-bg {
      margin: 0 auto;
      width: 6px;
      height: 120px;
      background: #dcdcdc;
      border-radius: 100px;
      flex: 1;
      position: relative;
      transform: rotate(180deg);
      cursor: pointer;
      .volume-bar {
        width: 6px;
        height: 50%;
        background: #56bf8b;
        border-radius: 100px;
      }
    }
    .checked {
      color: #56bf8b;
    }
  }
  .audio-right {
    width: 100%;
    height: 49px;
    line-height: 49px;
    background: #f6f6f6;
    border-radius: 6px;
    display: flex;
    padding: 0 15px;
    .dialogAudioPlay {
      cursor: pointer;
      color: #5c5e66;
      font-size: 20px;
    }
    .progress-bar-bg {
      background-color: #fff;
      flex: 1;
      position: relative;
      height: 10px;
      top: 50%;
      transform: translateY(-50%);
      margin-top: -1px;
      cursor: pointer;
      margin: 0 10px;
    }
    .progress-bar {
      background-color: #56bf8b;
      width: 0%;
      height: 10px;
      border-radius: 5px;
    }
  
    .audio-time {
      overflow: hidden;
      font-size: 14px;
      .audio-length-total {
        float: right;
      }
      .audio-length-current {
        float: left;
      }
    }
  }
  </style>
  
  