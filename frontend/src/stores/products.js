/**
 * @파일명 products.js
 * @설명 금융 상품(예금/적금) 상태 관리 스토어
 * @기능
 *   - 예금 상품 목록 조회 (getDeposits)
 *   - 적금 상품 목록 조회 (getSavings)
 * @API엔드포인트
 *   - GET /api/products/deposits/ : 예금 상품 목록
 *   - GET /api/products/savings/ : 적금 상품 목록
 */

import { defineStore } from "pinia"
import { ref } from "vue"
import axios from "axios"

export const useProductStore = defineStore('products', () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<Array>} 예금 상품 목록 */
  const deposits = ref([])
  
  /** @type {Ref<Array>} 적금 상품 목록 */
  const savings = ref([])
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = 'http://127.0.0.1:8000'

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 예금 상품 목록 조회
   * @description 금융감독원 API에서 가져온 예금 상품 데이터를 조회합니다
   */
  const getDeposits = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/products/deposits/`
    })
    .then(res => {
      deposits.value = res.data
    })
    .catch(err => {
      console.error('예금 상품 조회 실패:', err)
    })
  }

  /**
   * 적금 상품 목록 조회
   * @description 금융감독원 API에서 가져온 적금 상품 데이터를 조회합니다
   */
  const getSavings = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/products/savings/`
    })
    .then(res => {
      savings.value = res.data
    })
    .catch(err => {
      console.error('적금 상품 조회 실패:', err)
    })
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return { 
    // 상태
    deposits, 
    savings, 
    API_URL, 
    // 액션
    getDeposits, 
    getSavings 
  }

}, { persist: true })  // Pinia persist 플러그인: 새로고침 시에도 상태 유지