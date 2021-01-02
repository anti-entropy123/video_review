

// axios.defaults.baseURL = "https://api.video-review.top:1314/api/";
// baseUrl 在main.js中配置完成
const base = ''

// 用户

export const login = base + 'login/';

export const register = base + 'register/';

export const checkCode = base + 'checkCode';

export const user = base + 'user';

export const userInfo = base + 'userInfo/';

export const userlist = base + 'userlist/';

export const resetPassword = base + 'user/resetPassword/';

export const uploadImg = base +'uploadImg/';

//会议

export const meeting_search = base +'meeting/search/';

export const meeting_mine = base +'meeting/mine';

export const meeting_todo = base +'meeting/todo/';

export const meeting_history = base +'meeting/history/';

export const create_meeting = base +'meeting/';

//视频
export const create_video = base +'video/';

//完成审阅
export const video_review = base +'video/<videoId>/review/';

export const video_mine = base +'video/mine/';

export const uploadVideo = base +'uploadVideo/';

//项目
export const create_project= base +'project/';

export const get_user_video = base +'project/<projectId>/userAndVideo';

export const invite_user = base +'project/<projectId>/inviteUser/';

export const join = base +'project/<projectId>/join/';

export const get_projects = base +'projects';

export const get_meeting = base +'project/<projectId>/getMeeting';

export const remove_user = base +'project/<projectId>/removeUser';

export const remove_video = base +'project/<projectId>/removeVideo';

// 消息
export const get_messages = base + 'messages/'

export const message_detail = base +'message/<messageId>'
