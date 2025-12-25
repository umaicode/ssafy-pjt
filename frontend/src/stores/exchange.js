/**
 * @파일명 exchange.js
 * @설명 환율 정보 관리 스토어
 * @기능
 *   - 외부 API에서 환율 데이터 가져오기 (fetchAndSaveExchangeRates)
 *   - DB에서 환율 데이터 조회 (getExchangeRates)
 *   - localStorage 캐싱으로 오프라인 지원
 * @API엔드포인트
 *   - POST /api/exchange/fetch/ : 환율 데이터 가져와서 DB 저장
 *   - GET /api/exchange/rates/ : DB에서 환율 데이터 조회
 */

import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useExchangeStore = defineStore('exchange', () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<Array>} 환율 데이터 배열 */
  const rates = ref([])
  
  /** @type {Ref<boolean>} 로딩 상태 */
  const loading = ref(false)
  
  /** @type {Ref<string|null>} 에러 메시지 */
  const error = ref(null)
  
  /** @type {Ref<string|null>} 마지막 업데이트 시간 */
  const lastUpdated = ref(null)
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = 'http://127.0.0.1:8000'

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 환율 데이터 가져오기 및 DB 저장
   * @description 한국수출입은행 API에서 환율 데이터를 가져와 DB에 저장합니다
   * @returns {Promise<Object>} API 응답 데이터
   */
  const fetchAndSaveExchangeRates = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post(`${API_URL}/api/exchange/fetch/`)
      
      // 저장 후 DB에서 조회하여 상태 업데이트
      await getExchangeRates()
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || '환율 정보를 가져오는데 실패했습니다.'
      console.error('환율 fetch 에러:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * DB에서 환율 데이터 조회
   * @description 저장된 환율 데이터를 조회하고 localStorage에 캐싱합니다
   * @returns {Promise<Object>} API 응답 데이터
   */
  const getExchangeRates = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/api/exchange/rates/`)
      rates.value = response.data.rates || []
      
      // localStorage에 캐싱 (네트워크 실패 시 대비)
      if (rates.value.length > 0) {
        localStorage.setItem('exchangeRates', JSON.stringify(rates.value))
        localStorage.setItem('exchangeLastUpdated', new Date().toISOString())
        lastUpdated.value = rates.value[0]?.updated_at || null
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || '환율 정보를 불러오는데 실패했습니다.'
      console.error('환율 조회 에러:', err)
      
      // 에러 시 localStorage에서 캐시 로드
      loadFromCache()
      
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * localStorage에서 캐시된 데이터 로드
   * @description 네트워크 실패 시 캐시된 환율 데이터를 사용합니다
   */
  const loadFromCache = () => {
    const cachedRates = localStorage.getItem('exchangeRates')
    const cachedDate = localStorage.getItem('exchangeLastUpdated')
    
    if (cachedRates) {
      rates.value = JSON.parse(cachedRates)
      lastUpdated.value = cachedDate
    }
  }

  // 스토어 초기화 시 캐시에서 로드
  loadFromCache()

  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    rates,
    loading,
    error,
    lastUpdated,
    // 액션
    fetchAndSaveExchangeRates,
    getExchangeRates,
    loadFromCache
  }
})
