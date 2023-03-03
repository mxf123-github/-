// 页面路径：store/index.js 
import { createStore } from 'vuex'
export default createStore({
    state: {
        licenseNum:" ",
		time:"尚未登录",
		timeColor:"red",
        version:'1.2'
      },
    mutations:{
        setLicenseNum(state,licenseNum){
            state.licenseNum=licenseNum;
        },
        setTime(state,time){
            state.time=time;
        },
        setTimeColor(state,timeColor){
            state.timeColor=timeColor;
        }
    }

})