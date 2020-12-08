<template>
  <div class="palette">

<!--画板-->
    <div
      class="palette_wrapper"
      ref="palette_wrapper"
      :style="
        `width:${Size[0]}px;height:${Size[1]}px;border:${paletteStyleCopy.borderStyle} ${paletteStyleCopy.borderWidth}px ${paletteStyleCopy.borderColor};`
      ">
      <canvas
        ref="palette"
        :width="Size[0] - 2 * paletteStyleCopy.borderWidth"
        :height="Size[1] - 2 * paletteStyleCopy.borderWidth"
      ></canvas>
    </div>
<!--    <div class="palette_tip">-->
<!--      <button type="button" @click="paintRandom">画笔</button>-->
<!--      <button  type="button" @click="clearPalette">清除</button>-->
<!--      <button  type="button"-->
<!--               @click="savePalette(showbarOptionCopy.saveBtn.imageType)"-->
<!--               v-if="showbarOptionCopy.saveBtn.isShow">生成图片</button>-->

<!--    </div>-->
    <!-- 生成图片 -->
<!--    <div class="images" @click.self="closeImage" v-if="lastBase64">-->
<!--      <img :src="lastBase64" ref="resultImg" />-->
<!--    </div>-->
  </div>
</template>
<script>
  const transformKey =
    document.body.style.transform === undefined
      ? '-webkit-transform'
      : 'transform';

  export default {
    name: 'Draw',
    props: {
      point: {
        type: String,
        default: ''
      },
      // 展板显示的工具
      showbarOption: {
        type: Object,
        default: () => {
          return {};
        }
      },
      // 画板基础样式
      paletteStyle: {
        type: Object,
        default: () => {
          return {};
        }
      },
      Size: {
        type: Array,
        default: () => {
          return {};
        }
      },

    },
    data() {
      return {
        paletteStyleCopy: {
          width: 200,
          height: 200,
          backgroundColor: 'white',
          borderStyle: 'solid',
          borderColor: '#1765ad',
          borderWidth: 3,
          defaultColor: '#1765ad', // 全局默认颜色
          defaultLineWidth: 2 // 全局默认线条宽度
        },
        showbarOptionCopy: {
          clearBtn: true,
          saveBtn: {
            isShow: true,
            imageType: 'png'
          },
          lineBtn: true,
          hollowIrregularPolygonBtn: true,
          solidIrregularPolygonBtn: true,
          paintCircleBtn: true,
          paintRectangleBtn: true,
          // paintTextBtn: false,
          eraserBtn: true
        },
        cans: null,
        ctx: null,
        currentStatus: '普通画笔', //画笔状态
        touchType: 'Random',
        preCurrentStatus: '',
        preTouchType: '',
        startNew: null, //当前点击的点
        startOld: [], //存放之前点过的历史点
        move: {}, //移动的点
        endPoints: [], //该数组只存放最后两个结束的点，用于确定圆心或者矩形画完之后，有没有被移动过，进而确定圆心等用的是哪个数据
        circle: null,
        rectangle: null,
        text: null,
        eraserOptions: {
          size: 20,
          backgroundColor: 'black',
          isRect: false //是否是圆形的
        },
        history: [], //存放历史操作数组
        lastBase64: '' //最后生成的图片
      };
    },
    watch: {
      Size: {
        handler(newValue, oldValue) {
          // console.log("!!!!!!!!!!")
          // for (let i = 0; i < newValue.length; i++) {
          //   if (oldValue[i] != newValue[i]) {
          //     console.log(newValue)
          //   }
          // }
        },
        deep: true,
        immediate:true,
      }
    },
    mounted() {
      Object.assign(this.paletteStyleCopy, this.paletteStyle);
      this.init();
    },
    methods: {
      // 手绘
      startPoint(e) {
        const event = e || window.event;
        // 点击的时候，确认最先触摸的屏幕点
        this.startNew = {
          x: event.clientX
            ? event.clientX - this.$refs.palette.getBoundingClientRect().left
            : event.targetTouches[0].clientX -
            this.$refs.palette.getBoundingClientRect().left,
          y: event.clientY
            ? event.clientY - this.$refs.palette.getBoundingClientRect().top
            : event.targetTouches[0].clientY -
            this.$refs.palette.getBoundingClientRect().top,
          isPaint: false
        };
        // 然后立马存放进历史
        this.startOld.push(this.startNew);
        // 如果在触摸或者鼠标按下的时候是随机线的状态
        if (this.touchType == 'Random' || this.touchType == 'Eraser') {
          this.ctx.beginPath();
          this.ctx.lineWidth = this.paletteStyleCopy.defaultLineWidth;
          this.ctx.moveTo(this.startNew.x, this.startNew.y);
            this.ctx.lineWidth = this.paletteStyleCopy.defaultLineWidth;
            this.ctx.strokeStyle = this.paletteStyleCopy.defaultColor;
        }

        this.$refs.palette_wrapper.addEventListener(
          'touchmove',
          this.movePoint,
          false
        );
        this.$refs.palette_wrapper.addEventListener(
          'mousemove',
          this.movePoint,
          false
        );
      },
      movePoint(e) {
        const event = e || window.event;
        // 如果鼠标按下或者触摸事件被触发，那么isPaint就不能为false，因为这个点不可能成为不规则折线的折点了
        // 这一块，谷歌浏览器的mousedown和mousemove一起执行了，很奇怪，所以通过判断mousedown和mousemove的位置是否相同来判断是否真正触发mousemove
        if (this.startNew.x != this.move.x || this.startNew.y != this.move.y) {
          // this.startOld[this.startOld.length - 1].isPaint = true;
          // 当鼠标或者手指真正发生移动的时候，才能开始给移动坐标数组添加数据
          this.move = {
            x: event.clientX
              ? event.clientX - this.$refs.palette.getBoundingClientRect().left
              : event.targetTouches[0].clientX -
              this.$refs.palette.getBoundingClientRect().left,
            y: event.clientY
              ? event.clientY - this.$refs.palette.getBoundingClientRect().top
              : event.targetTouches[0].clientY -
              this.$refs.palette.getBoundingClientRect().top
          };
        }
        if (this.touchType == 'Random' || this.touchType == 'Eraser') {
          // 任意的线条跟橡皮擦的逻辑是一样的，只是橡皮擦的颜色跟背景色要相同，而且橡皮擦不能让它超出范围
          if (this.touchType == 'Eraser') {
            // 橡皮擦不能让它超出范围
            if (this.move.x <= this.$refs.eraser.offsetWidth / 2) {
              this.move.x = this.$refs.eraser.offsetWidth / 2;
            }
            if (this.move.y <= this.$refs.eraser.offsetHeight / 2) {
              this.move.y = this.$refs.eraser.offsetHeight / 2;
            }
            if (
              this.move.x >=
              this.Size[0] -
              2 * this.paletteStyleCopy.borderWidth -
              this.$refs.eraser.offsetWidth / 2
            ) {
              this.move.x =
                this.Size[0] -
                2 * this.paletteStyleCopy.borderWidth -
                this.$refs.eraser.offsetWidth / 2;
            }

            if (
              this.move.y >=
              this.Size[1] -
              2 * this.paletteStyleCopy.borderWidth -
              this.$refs.eraser.offsetHeight / 2
            ) {
              this.move.y =
                this.Size[1] -
                2 * this.paletteStyleCopy.borderWidth -
                this.$refs.eraser.offsetHeight / 2;
            }
            this.$refs.eraser.style[transformKey] = `translate3d(${this.move.x -
            this.eraserOptions.size / 2}px,${this.move.y -
            this.eraserOptions.size / 2}px,0)`;
          }
          this.ctx.lineTo(this.move.x, this.move.y);
          this.ctx.stroke();
        }
      },
      endPoint() {
        if (this.touchType == 'Random') {
          if (this.startNew) {
            this.ctx.beginPath();
            this.ctx.strokeStyle = this.paletteStyleCopy.defaultColor;

            this.ctx.arc(
              this.startNew.x,
              this.startNew.y,
              this.paletteStyleCopy.defaultLineWidth / 2,
              0,
              360,
              false
            );
            this.ctx.fillStyle = this.paletteStyleCopy.defaultColor;
            this.ctx.fill();
          }
        }
        this.startNew = null;
        this.$refs.palette_wrapper.removeEventListener(
          'touchmove',
          this.movePoint,
          false
        );
        this.$refs.palette_wrapper.removeEventListener(
          'mousemove',
          this.movePoint,
          false
        );
      },
      // 初始化画笔
      initpaint() {
        // if (this.isEdit) {
        //   this.startOld = [];
        // }
      },
      // 随便画
      paintRandom() {
        this.touchType = 'Random';
        this.currentStatus = '普通画笔';
        this.initpaint();
      },
      // 关闭图片
      closeImage() {
        this.lastBase64 = '';
      },
      // 初始化画布
      init() {
        this.cans = this.$refs.palette;
        this.circle = this.$refs.circle;
        this.rectangle = this.$refs.rectangle;
        this.ctx = this.$refs.palette.getContext('2d');
        let t = new Date();
        this.history.push({
          time: `${t.getHours() < 10 ? '0' + t.getHours() : t.getHours()}:${
            t.getMinutes() < 10 ? '0' + t.getMinutes() : t.getMinutes()
          }:${t.getSeconds() < 10 ? '0' + t.getSeconds() : t.getSeconds()}`,
          text: '创建画布',
          data: this.ctx.getImageData(
            0,
            0,
            this.Size[0] - 2 * this.paletteStyleCopy.borderWidth,
            this.Size[1] - 2 * this.paletteStyleCopy.borderWidth
            // this.Size[0] - 2 * this.Size.borderWidth,
            // this.Size.height - 2 * this.Size.borderWidth
          )
        });
        this.$refs.palette_wrapper.addEventListener(
          'touchstart',
          this.startPoint,
          false
        );
        this.$refs.palette_wrapper.addEventListener(
          'mousedown',
          this.startPoint,
          false
        );
        this.$refs.palette_wrapper.addEventListener(
          'touchend',
          this.endPoint,
          false
        );
        this.$refs.palette_wrapper.addEventListener(
          'mouseup',
          this.endPoint,
          false
        );
      },
      // 清除画布
      clearPalette() {
        this.ctx.clearRect(
          0,
          0,
          this.Size[0] - 2 * this.paletteStyleCopy.borderWidth,
          this.Size[1] - 2 * this.paletteStyleCopy.borderWidth
        );
        this.startNew = null;
        this.startOld = [];
        this.history = [];
      },
      // 将画布转为图片
      savePalette(type = 'png') {
        if (type == 'png') {
          this.lastBase64 = this.cans.toDataURL('image/png');
        } else if (type == 'jpeg') {
          this.lastBase64 = this.cans.toDataURL('image/jpeg', 1);
        }
        // 生成图片弹出弹窗
        // this.$nextTick(() => {
        //   let timer = setTimeout(() => {
        //     this.$refs.resultImg.style[transformKey] = `translate3d(0,0,0)`;
        //     clearTimeout(timer);
        //   }, 0);
        // });
        this.$emit('getImg', this.lastBase64);
      },
    }
  };
</script>
<style scoped>
  * {
    margin: 0px;
  }
  .palette {
    overflow: hidden;
    user-select: none;
  }
  .palette_tip {
    position: relative;
    margin: 10px 15px;
    padding: 10px 0px;
    font-size: 24px;
    line-height: 24px;
    font-weight: 600;
    text-align: left;
    border-bottom: 1px solid #eeeeee;
  }

  .palette_wrapper {
    box-sizing: border-box;
    position: relative;
    margin: 0 auto;
    width: 100px;
    height: 100px;
    overflow: hidden;
  }

  .palette_wrapper canvas {
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 1;
  }
  /* 图片弹窗 */
  .palette .images {
    margin: auto;
    position: fixed;
    left: 0px;
    right: 0px;
    top: 0px;
    bottom: 0px;
    background-color: rgba(0, 0, 0, 0.4);
    z-index: 99;
  }
  .palette .images img {
    margin: auto;
    position: fixed;
    left: 0px;
    right: 0px;
    top: 0px;
    bottom: 0px;
    border: 5px solid #fed640;
    background-color: white;
    z-index: 100;
    transform: translate3d(0, 120%, 0);
    transition: all 0.5s;
  }
</style>
