/**
 * @파일명 theme.js
 * @설명 다크/라이트 테마 관리 스토어
 * @기능
 *   - 시스템 테마 감지 (prefers-color-scheme)
 *   - 테마 토글 (toggleTheme)
 *   - 테마 설정 (setTheme)
 *   - localStorage 자동 저장
 */

import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // ========================================
  // 초기화 함수
  // ========================================
  
  /**
   * 초기 테마 결정
   * @description localStorage 저장값 → 시스템 설정 순으로 확인합니다
   * @returns {string} 'dark' 또는 'light'
   */
  const getInitialTheme = () => {
    // 1. localStorage에 저장된 테마가 있으면 사용
    const saved = localStorage.getItem('theme')
    if (saved) return saved
    
    // 2. 시스템 다크모드 설정 확인
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<string>} 현재 테마 ('dark' | 'light') */
  const theme = ref(getInitialTheme())
  
  /** @type {Ref<boolean>} 다크모드 여부 */
  const isDark = ref(theme.value === 'dark')

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 테마 토글
   * @description 현재 테마를 반대로 전환합니다
   */
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    isDark.value = theme.value === 'dark'
  }

  /**
   * 특정 테마로 설정
   * @param {string} newTheme - 설정할 테마 ('dark' | 'light')
   */
  const setTheme = (newTheme) => {
    theme.value = newTheme
    isDark.value = newTheme === 'dark'
  }

  // ========================================
  // 감시자 (Watcher)
  // ========================================
  
  /**
   * 테마 변경 시 DOM 및 localStorage 업데이트
   * @description HTML data-theme 속성과 localStorage를 동기화합니다
   */
  watch(theme, (newTheme) => {
    document.documentElement.setAttribute('data-theme', newTheme)
    localStorage.setItem('theme', newTheme)
  }, { immediate: true })  // 즉시 실행하여 초기 테마 적용

  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    theme,
    isDark,
    // 액션
    toggleTheme,
    setTheme
  }
})
