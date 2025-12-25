/**
 * @파일명 main.js
 * @설명 Vue 애플리케이션 진입점 (Entry Point)
 * @기능
 *   - Vue 앱 인스턴스 생성
 *   - Pinia 상태 관리 설정
 *   - Vue Router 설정
 *   - 전역 스타일 및 폰트 적용
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

// F!NK 디자인 시스템 - 전역 CSS
import './assets/styles/global.css'

// Pretendard 폰트 (한글 최적화 웹폰트)
import "pretendard/dist/web/variable/pretendardvariable.css"

// ========================================
// 앱 초기화
// ========================================

// Vue 앱 인스턴스 생성
const app = createApp(App)

// Pinia 상태 관리 설정
const pinia = createPinia()

// Pinia persist 플러그인 적용 (새로고침 시에도 상태 유지)
pinia.use(piniaPluginPersistedstate)

// 플러그인 등록
app.use(pinia)   // Pinia 상태 관리
app.use(router)  // Vue Router

// DOM에 앱 마운트
app.mount('#app')
