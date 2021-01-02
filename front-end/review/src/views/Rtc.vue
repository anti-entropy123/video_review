<template>
    <div></div>
</template>

<script>
import 'aliyun-webrtc-sdk'

export default {
    name: "Rtc",
    data() {
        return{
            aliWebrtc: null,
        }
    },
    props: [
        'userId', 'meetingId', 'rtc'
    ],
    mounted() {
        console.log('rtc初始化')
        // 初始化语音模块
        console.log(AliRtcEngine)
        this.aliWebrtc = new AliRtcEngine();
        this.aliWebrtc.isSupport().then(re => {
            console.log(re);
        }).catch(error => {
            alert(error.message);
        })
        console.log('语音模块', this.aliWebrtc);
        this.aliWebrtc.on("onJoin", (publisher) => {
            //重置订阅状态
            //默认订阅远端音频和视频大流，但需要调用subscribe才能生效
            //这里取消默认订阅，根据需求进行订阅
            this.aliWebrtc.configRemoteAudio(publisher.userId, true);
            this.aliWebrtc.configRemoteCameraTrack(publisher.userId, false, false);
            // showAlert(publisher.displayName + "加入房间","success");
            console.log(publisher.displayName + "加入房间");
        });
        this.aliWebrtc.on("onPublisher", (publisher) => {
            console.log("onPublisher", publisher);
            // let index = publisherList.getIndexByProprety(publisher.userId, "userId");
            if (index === -1) {
                //新增
                // publisherList.push(publisher);
            } else {
                //流状态更新
                // updatePublisherStream(publisher, index);
            }
        });
        this.aliWebrtc.on("onUnPublisher", (publisher) => {
            console.log("onUnPublisher",publisher);
            // detelePublisher(publisher.userId);
            // removeDom(publisher.userId);
            // initialization(publisher.userId);
        });
        this.aliWebrtc.on("onBye",(message) =>{
            //1:被服务器踢出
            //2:频道关闭
            //3:同一个ID在其他端登录,被服务器踢出
            var msg;
            switch (message.code) {
                case 1: msg = "被服务器踢出";
                    break;
                case 2: msg = "频道关闭";
                    break;
                case 3: msg = "同一个ID在其他端登录,被服务器踢出";
                    break;
                default: msg = "onBye";
            }
            showAlert(msg,"danger");
        });
        var authInfo = this.GenerateAliRtcAuthInfo(this.meetingId);
        this.aliWebrtc.joinChannel(authInfo, this.userId).then(() => {
        }).catch((error) => {
            showAlert("[加入房间失败]" + error.message, "danger");
        })
        console.log('rtc初始化完成');
    },
    watch: {
        rtc: function(){
            console.log(this.rtc);
            // console.log('语音模块', this.aliWebrtc);
            var authInfo = this.GenerateAliRtcAuthInfo(this.meetingId);
            this.aliWebrtc.configLocalAudioPublish = this.rtc;
            this.aliWebrtc.configLocalCameraPublish = this.rtc;
            this.aliWebrtc.publish().then(re => {
                    setTimeout(() => {
                    },2000);
                    console.log('推流成功')
                }).catch(error => {
                    setTimeout(() => {
                    }, 2000);
                });
        }
    },
    methods: {
        GenerateAliRtcAuthInfo(channelId) {
            var appId = "60okegzi";// 修改为自己的appid 该方案仅为开发测试使用，正式上线需要使用服务端的AppServer
            var appKey = "6c3c9206b0d3dcc11f44495391a53df8";// 修改为自己的appkey 该方案仅为开发测试使用，正式上线需要使用服务端的AppServer
            var timestamp = parseInt(new Date().getTime() / 1000 + 48 * 60 * 60);
            var nonce = 'AK-' + timestamp;
            var token = sha256(appId + appKey + channelId + this.userId + nonce + timestamp);
            return {
                appid:appId,
                userid: this.userId,
                timestamp:timestamp,
                nonce:nonce,
                token:token,
                gslb: ["https://rgslb.rtc.aliyuncs.com"],
                channel:channelId
            };
        },
    }
}
</script>

<style scoped>

</style>