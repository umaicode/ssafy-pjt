/**
 * @파일명 youtube/videos.js
 * @설명 저장된 동영상 관리 스토어
 * @기능
 *   - 동영상 저장 토글 (toggleVideo)
 *   - 동영상 제거 (removeVideo)
 *   - 저장 목록 전체 삭제 (clearVideos)
 * @저장 localStorage에 영구 저장 (Pinia persist)
 */

import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useVideoStore = defineStore("video", () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<Array>} 저장된 동영상 목록 */
  const savedVideos = ref([])

  // ========================================
  // 계산된 속성 (Getters)
  // ========================================

  /**
   * 동영상 저장 여부 확인
   * @param {string} videoId - 동영상 ID
   * @returns {boolean} 저장 여부
   */
  const isSaved = computed(() => {
    return (videoId) => savedVideos.value.some(v => v.id === videoId)
  })

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 동영상 저장 토글
   * @description 이미 저장되어 있으면 제거, 없으면 추가
   * @param {Object} video - 동영상 정보 객체
   */
  const toggleVideo = function (video) {
    const exists = savedVideos.value.some(v => v.id === video.id)
    
    if (exists) {
      savedVideos.value = savedVideos.value.filter(v => v.id !== video.id)
    }
    else {
      savedVideos.value.unshift(video)  // 맨 앞에 추가
    }
  }

  /**
   * 동영상 제거
   * @param {string} videoId - 제거할 동영상 ID
   */
  const removeVideo = function (videoId) {
    savedVideos.value = savedVideos.value.filter(v => v.id !== videoId)
  }

  /**
   * 모든 동영상 삭제
   * @description 저장된 동영상 목록을 전체 초기화
   */
  const clearVideos = function () {
    savedVideos.value = []
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    savedVideos, 
    // 계산된 속성
    isSaved, 
    // 액션
    toggleVideo, 
    removeVideo, 
    clearVideos
  }
}, { persist: true })  // Pinia persist 플러그인: 새로고침 시에도 저장 목록 유지