/**
 * @파일명 metals.js
 * @설명 금/은 현물 가격 조회 스토어
 * @기능
 *   - 금속 종류 선택 (setMetal)
 *   - 기간 설정 (setDates)
 *   - 가격 데이터 로드 (loadPrices)
 * @API엔드포인트
 *   - GET /api/metals/ : 금속 가격 데이터 조회
 */

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from 'axios'

export const useMetalsStore = defineStore('metals', () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = 'http://127.0.0.1:8000'

  /** @type {Ref<string>} 선택된 금속 종류 ('gold' | 'silver') */
  const metal = ref('gold')
  
  /** @type {Ref<string|null>} 조회 시작일 */
  const startDate = ref(null)
  
  /** @type {Ref<string|null>} 조회 종료일 */
  const endDate = ref(null)

  /** @type {Ref<Array>} 가격 데이터 배열 */
  const prices = ref([])
  
  /** @type {Ref<boolean>} 로딩 상태 */
  const loading = ref(false)
  
  /** @type {Ref<string|null>} 에러 메시지 */
  const errorMessage = ref(null)

  // ========================================
  // 계산된 속성 (Getters)
  // ========================================

  /** @returns {Array<string>} 차트 X축 라벨 (날짜) */
  const labels = computed(() => 
    prices.value.map(item => item.date)
  )

  /** @returns {Array<number>} 차트 Y축 데이터 (가격) */
  const priceValues = computed(() => 
    prices.value.map(item => item.price)
  )

  /** @returns {boolean} 데이터가 비어있는지 여부 */
  const isEmpty = computed(() =>
    !loading.value && prices.value.length === 0
  )

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 금속 종류 변경
   * @description 금속 종류를 변경하고 가격 데이터를 새로 로드합니다
   * @param {string} newMetal - 'gold' 또는 'silver'
   */
  const setMetal = async (newMetal) => {
    metal.value = newMetal
    await loadPrices()
  }

  /**
   * 조회 기간 설정
   * @description 시작일과 종료일을 설정하고 가격 데이터를 새로 로드합니다
   * @param {string} start - 시작일 (YYYY-MM-DD)
   * @param {string} end - 종료일 (YYYY-MM-DD)
   */
  const setDates = async (start, end) => {
    startDate.value = start
    endDate.value = end
    await loadPrices()
  }

  /**
   * 기간 초기화
   * @description 기간 설정을 초기화하고 전체 데이터를 로드합니다
   */
  const resetDates = async () => {
    startDate.value = null
    endDate.value = null
    await loadPrices()
  }

  /**
   * 가격 데이터 로드
   * @description 선택된 금속과 기간에 맞는 가격 데이터를 API에서 가져옵니다
   */
  const loadPrices = async () => {
    loading.value = true
    errorMessage.value = null

    try {
      const res = await axios.get(`${API_URL}/api/metals/`, {
        params: {
          metal: metal.value,
          start: startDate.value,
          end: endDate.value
        }
      })

      prices.value = res.data
    } catch (err) {
      prices.value = []
      errorMessage.value = err.response?.data?.detail || '데이터를 불러오는 중 오류가 발생했습니다.'
    } finally {
      loading.value = false
    }
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    metal,
    startDate,
    endDate,
    prices,
    loading,
    errorMessage,
    // 계산된 속성
    labels,
    priceValues,
    isEmpty,
    // 액션
    setMetal,
    setDates,
    resetDates,
    loadPrices
  }
}, { persist: true })  // Pinia persist 플러그인: 새로고침 시에도 상태 유지