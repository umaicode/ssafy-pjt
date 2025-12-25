/**
 * @파일명 youtube/channels.js
 * @설명 저장된 채널 관리 스토어
 * @기능
 *   - 채널 저장 토글 (toggleChannel)
 *   - 채널 제거 (removeChannel)
 *   - 저장 목록 전체 삭제 (clearChannels)
 * @저장 localStorage에 영구 저장 (Pinia persist)
 */

import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useChannelStore = defineStore("channel", () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<Array>} 저장된 채널 목록 */
  const savedChannels = ref([])

  // ========================================
  // 계산된 속성 (Getters)
  // ========================================

  /**
   * 채널 저장 여부 확인
   * @param {string} channelId - 채널 ID
   * @returns {boolean} 저장 여부
   */
  const isSaved = computed(() => {
    return (channelId) => savedChannels.value.some(c => c.id === channelId)
  })

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 채널 저장 토글
   * @description 이미 저장되어 있으면 제거, 없으면 추가
   * @param {Object} channel - 채널 정보 객체
   */
  const toggleChannel = function (channel) {
    const exists = savedChannels.value.some(c => c.id === channel.id)

    if (exists) {
      savedChannels.value = savedChannels.value.filter(c => c.id !== channel.id)
    }
    else {
      savedChannels.value.unshift(channel)  // 맨 앞에 추가
    }
  }

  /**
   * 채널 제거
   * @param {string} channelId - 제거할 채널 ID
   */
  const removeChannel = function (channelId) {
    savedChannels.value = savedChannels.value.filter(c => c.id !== channelId)
  }

  /**
   * 모든 채널 삭제
   * @description 저장된 채널 목록을 전체 초기화
   */
  const clearChannels = function () {
    savedChannels.value = []
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    savedChannels, 
    // 계산된 속성
    isSaved, 
    // 액션
    toggleChannel, 
    removeChannel, 
    clearChannels
  }
}, { persist: true })  // Pinia persist 플러그인: 새로고침 시에도 저장 목록 유지