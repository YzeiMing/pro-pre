<template>
  <view class="naming-page">
    <!-- 顶部标题 -->
    <view class="header">
      <text class="title">👶 宝宝取名助手</text>
      <text class="subtitle">吉祥如意 · 寓意美好</text>
    </view>

    <!-- 输入模块 -->
    <view class="input-card card">

      <!-- 姓氏 -->
      <view class="input-group">
        <text class="label">姓氏</text>
        <view class="input-wrap">
          <input
            v-model="formData.surname"
            class="input"
            placeholder="请输入姓氏"
            placeholder-class="placeholder"
            maxlength="2"
          />
        </view>
      </view>

      <!-- 性别 -->
      <view class="input-group">
        <text class="label">性别</text>
        <view class="radio-group">
          <view
            v-for="item in genderOptions"
            :key="item.value"
            class="radio-item"
            :class="{ active: formData.gender === item.value }"
            @click="formData.gender = item.value"
          >
            <text class="radio-text">{{ item.label }}</text>
          </view>
        </view>
      </view>

      <!-- 字数 -->
      <view class="input-group">
        <text class="label">字数</text>
        <view class="radio-group">
          <view
            v-for="item in lengthOptions"
            :key="item.value"
            class="radio-item"
            :class="{ active: formData.length === item.value }"
            @click="formData.length = item.value"
          >
            <text class="radio-text">{{ item.label }}</text>
          </view>
        </view>
      </view>

      <!-- 其他要求 -->
      <view class="input-group">
        <text class="label">其他要求</text>
        <view class="input-wrap">
          <textarea
            v-model="formData.other"
            class="textarea"
            placeholder="输入名字的其他要求，如包含某个字，或者名字的寓意"
            placeholder-class="placeholder"
            maxlength="100"
            :show-count="false"
          />
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="btn-group">
        <button class="btn reset" @click="resetForm">重置</button>
        <button class="btn generate" @click="onGenerateNames">起名</button>
      </view>
    </view>

    <!-- 结果模块 -->
	<!--1. TypeError: Cannot read property 'length' of undefined.
	这里有问题names && names.length-->
    <view class="result-card card" v-if="names.length > 0">
      <view class="card-title">🎯 推荐名字（{{ names.length }} 个）</view>
      <view class="result-list">
        <view
          v-for="(item, index) in names"
          :key="index"
          class="result-item"
        >
          <view class="name">{{ item.name }}</view>
		  <view class="source">
			<text class="source-icon">📜</text>
			<text class="source-text">{{ item.reference }}</text>
		  </view>
          <view class="meaning">{{ item.moral }}</view>
        </view>
      </view>
	  
	  <!-- 🔑 新增：换一批按钮 -->
	    <button class="btn-reload" @click="onReloadNames" :disabled="loading">
	      {{ loading ? '生成中...' : '🔄 换一批' }}
	    </button>
    </view>

    <!-- 空状态 -->
    <view v-else class="empty-tips">
      <text class="empty-text">暂无推荐名字，请填写信息后点击「起名」</text>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import http from "/http/http.js"

const formData = reactive({
  surname: '',
  gender: "不限",
  length: "不限",
  other: ''
})

let loading = ref(false);

const genderOptions = [
  { label: '不限', value: "不限" },
  { label: '男生', value: "男" },
  { label: '女生', value: "女" }
]

const lengthOptions = [
  { label: '不限', value: "不限" },
  { label: '单字', value: "单字" },
  { label: '两字', value: "两字" }
]

const names = ref([])

const resetForm = () => {
  formData.surname = ''
  formData.gender = "不限"
  formData.length = "不限"
  formData.other = ''
  names.value = []
}

const generateNames = async (exclude=[]) => {
	if (!formData.surname.trim()) {
	    uni.showToast({ title: '请输入姓氏', icon: 'none' })
	    return
	}
	loading.value = true;
	uni.showLoading({title:'正在起名中'});
	
	//发起网络请求
	try{
		let result = await http.generateName({
			surname: formData.surname,
			gender:formData.gender,
			length: formData.length,
			other: formData.other,
			exclude: exclude
		});
		///这里的result.name是对应后端函数返回的name,所以名字要一样!!!
		names.value = result.name;
	}catch(e){
		uni.showToast({
			title: e.message,
			icon: "none"
		})
	}finally{
		loading.value = false;
		uni.hideLoading();
	}
}

const onGenerateNames = async () => {
	await generateNames();
}

const onReloadNames = async () => {
	await generateNames(names.value.map((obj) => obj['name']));
}
</script>

<style scoped>
/* ======== 关键修复：输入框区域样式 ======== */
.input-wrap {
  position: relative;
  width: 100%;
  /* 确保热区足够，避免点击穿透 */
  min-height: 88rpx;
}

.input, .textarea {
  width: 100%;
  padding: 24rpx 28rpx;
  border-radius: 16rpx;
  background: #fafafa;
  border: 2rpx solid #e0e0e0;
  font-size: 30rpx;
  color: #333;
  box-sizing: border-box;
  /* 关键修复：显式启用文本光标 & 防止误触 */
  cursor: text;
  user-select: text;
  /* iOS 兼容性增强 */
  -webkit-tap-highlight-color: transparent;
}

.input {
  height: 88rpx;
}

.textarea {
  min-height: 120rpx;
  line-height: 1.5;
  /* 不再设固定 height，避免高度计算异常 */
  height: auto;
  padding-top: 20rpx;
  padding-bottom: 20rpx;
}

.input:focus, .textarea:focus {
  border-color: #ff9e80;
  background: #fff9f8;
  /* 微动效增强反馈 */
  transform: scale(1.005);
}

.placeholder {
  color: #aaa;
}

/* 其余样式保持不变（为节省篇幅，此处省略重复代码，实际使用请保留原完整样式） */
/* 注意：以下为简化保留的核心样式结构，完整样式请参考上一版，仅替换 .input-wrap 及 input/textarea 样式 */

page {
  background: linear-gradient(135deg, #fef9f0 0%, #ffebe6 100%);
  padding: 20rpx;
}

.naming-page {
  min-height: 100vh;
  padding: 0 24rpx;
}

.header {
  text-align: center;
  margin-bottom: 40rpx;
}

.title {
  font-size: 48rpx;
  font-weight: 700;
  color: #e74c3c;
  display: block;
  margin-bottom: 12rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #888;
}

.card {
  background: #ffffff;
  border-radius: 24rpx;
  box-shadow: 0 8rpx 30rpx rgba(231, 76, 60, 0.12);
  padding: 40rpx 32rpx;
  margin-bottom: 32rpx;
}

.card-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 32rpx;
  padding-bottom: 16rpx;
  border-bottom: 2rpx dashed #f5f5f5;
}

.input-group {
  margin-bottom: 36rpx;
}

.label {
  display: block;
  font-size: 30rpx;
  color: #555;
  margin-bottom: 16rpx;
  font-weight: 500;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.radio-item {
  padding: 16rpx 32rpx;
  border-radius: 50rpx;
  background: #f8f8f8;
  border: 2rpx solid #e0e0e0;
  font-size: 28rpx;
  color: #666;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.radio-item.active {
  background: #fff2f0;
  border-color: #ff9e80;
  color: #e74c3c;
  transform: scale(1.03);
}

.radio-dot {
  display: inline-block;
  width: 32rpx;
  height: 32rpx;
  line-height: 32rpx;
  text-align: center;
  margin-right: 8rpx;
  color: #e74c3c;
  font-weight: bold;
}

.btn-group {
  display: flex;
  justify-content: space-between;
  gap: 20rpx;
  margin-top: 20rpx;
}

.btn {
  flex: 1;
  height: 88rpx;
  line-height: 88rpx;
  font-size: 32rpx;
  font-weight: 600;
  border-radius: 50rpx;
  color: #fff;
  border: none;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.1);
}

.reset {
  background: linear-gradient(135deg, #95a5a6, #7f8c8d);
}

.generate {
  background: linear-gradient(135deg, #ff9e80, #e74c3c);
}

.btn:active {
  transform: scale(0.96);
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.result-item {
  padding: 32rpx;
  background: #fdf7f6;
  border-radius: 20rpx;
  border-left: 6rpx solid #ff9e80;
  transition: all 0.2s;
}

.result-item:active {
  background: #fceae7;
  transform: translateX(6rpx);
}

.name {
  font-size: 40rpx;
  font-weight: 700;
  color: #e74c3c;
  margin-bottom: 12rpx;
}

.meaning {
  font-size: 28rpx;
  color: #555;
  line-height: 1.6;
}

.empty-tips {
  text-align: center;
  margin-top: 60rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #aaa;
}

/* ===== 新增：来源样式 ===== */
.source {
  display: flex;
  align-items: center;
  margin: 8rpx 0 12rpx;
  font-size: 24rpx;
  color: #888;
}

.source-icon {
  margin-right: 8rpx;
  font-size: 22rpx;
}

.source-text {
  font-style: italic;
  /* 可选：加一点文献感 */
  /* font-family: "Songti SC", serif; */
}

/* ===== 新增：换一批按钮 ===== */
.btn-reload {
  display: block;
  width: 100%;
  height: 64rpx;
  line-height: 64rpx;
  margin-top: 24rpx;
  padding: 0;
  font-size: 28rpx;
  color: #e67e67;
  background: #fff8f6;
  border: 1rpx solid #ffd8d2;
  border-radius: 40rpx;
  box-shadow: 0 2rpx 8rpx rgba(230, 126, 103, 0.1);
  transition: all 0.2s;
}

.btn-reload:active {
  background: #ffefed;
  transform: scale(0.98);
}

.btn-reload[disabled] {
  opacity: 0.6;
  color: #aaa;
}
</style>