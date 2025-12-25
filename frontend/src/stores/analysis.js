/**
 * @파일명 analysis.js
 * @설명 AI 금융 분석 스토어
 * @기능
 *   - AI 분석 요청 (createAnalysis)
 *   - 분석 결과 조회 (fetchResult)
 *   - 상품 선택 관리 (마이페이지 그래프용)
 *   - 월별 누적 시뮬레이션 계산
 * @API엔드포인트
 *   - POST /api/v1/analysis/ : AI 분석 생성
 *   - GET /api/v1/analysis/:id/result/ : 분석 결과 조회
 */

import { defineStore } from "pinia";
import axios from "axios";
import { ref, computed } from "vue";
import { useAccountStore } from "@/stores/accounts";
import { useRouter } from "vue-router";

export const useAnalysisStore = defineStore('analysis', () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = 'http://127.0.0.1:8000'

  /** @type {Ref<Object|null>} AI 분석 결과 */
  const result = ref(null)
  
  /** @type {Ref<boolean>} 로딩 상태 */
  const loading = ref(false)
  
  /** @type {Ref<Error|null>} 에러 정보 */
  const error = ref(null)
  
  /** @type {Router} Vue Router 인스턴스 */
  const router = useRouter()

  /** @type {Ref<Array>} 선택된 상품 목록 (마이페이지 그래프용) */
  const selectedProducts = ref([])

  // ========================================
  // 계산된 속성 (Getters)
  // ========================================

  /** @returns {Array} 선택된 적금 상품들 */
  const selectedSavings = computed(() => 
    selectedProducts.value.filter(p => p.product_type === 'saving')
  )

  /** @returns {Array} 선택된 예금 상품들 */
  const selectedDeposits = computed(() => 
    selectedProducts.value.filter(p => p.product_type === 'deposit')
  )

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * AI 분석 생성
   * @description 사용자 정보를 바탕으로 AI 분석을 요청합니다
   * @param {Object} payload - 분석 요청 데이터 (목적, 기간, 금액 등)
   */
  const createAnalysis = function (payload) {
    const accountStore = useAccountStore()

    loading.value = true
    error.value = null

    axios({
      method: 'post',
      url: `${API_URL}/api/v1/analysis/`,
      data: payload,
      headers: {
        'Authorization': `Token ${accountStore.token}`,
      },
    })
    .then(res => {
      // 분석 완료 후 결과 페이지로 이동
      router.push(`/analysis/${res.data.analysis_id}/result`)
    })
    .catch(err => {
      console.error('AI 분석 생성 실패:', err)
      error.value = err
      throw err
    })
    .finally(() => {
      loading.value = false
    })
  }

  /**
   * 분석 결과 조회
   * @description 특정 분석 ID의 결과를 가져옵니다
   * @param {number} analysisId - 분석 ID
   */
  const fetchResult = function (analysisId) {
    const accountStore = useAccountStore()

    loading.value = true
    error.value = null

    axios({
      method: 'get',
      url: `${API_URL}/api/v1/analysis/${analysisId}/result/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`,
      },
    })
    .then(res => {
      result.value = res.data
    })
    .catch(err => {
      console.error('분석 결과 조회 실패:', err)
      error.value = err
    })
    .finally(() => {
      loading.value = false
    })
  }

  /**
   * 분석 결과 초기화
   * @description 분석 결과와 에러 상태를 초기화합니다
   */
  const resetResult = function () {
    result.value = null
    error.value = null
  }

  // === 선택된 상품 관리 기능 ===
  
  /**
   * 상품 선택 추가
   * @description 선택된 상품 목록에 상품을 추가합니다 (중복 방지)
   * @param {Object} product - 상품 정보
   */
  const addSelectedProduct = function (product) {
    const exists = selectedProducts.value.find(
      p => p.fin_prdt_cd === product.fin_prdt_cd && p.product_type === product.product_type
    )
    if (!exists) {
      selectedProducts.value.push(product)
    }
  }

  /**
   * 상품 선택 해제
   * @description 선택된 상품 목록에서 상품을 제거합니다
   * @param {string} fin_prdt_cd - 상품 코드
   * @param {string} product_type - 상품 타입
   */
  const removeSelectedProduct = function (fin_prdt_cd, product_type) {
    selectedProducts.value = selectedProducts.value.filter(
      p => !(p.fin_prdt_cd === fin_prdt_cd && p.product_type === product_type)
    )
  }

  /**
   * 상품 선택 여부 확인
   * @description 특정 상품이 선택되어 있는지 확인합니다
   * @param {string} fin_prdt_cd - 상품 코드
   * @param {string} product_type - 상품 타입
   * @returns {boolean} 선택 여부
   */
  const isProductSelected = function (fin_prdt_cd, product_type) {
    return selectedProducts.value.some(
      p => p.fin_prdt_cd === fin_prdt_cd && p.product_type === product_type
    )
  }

  /**
   * 선택된 상품 전체 초기화
   * @description 모든 선택된 상품을 초기화합니다
   */
  const clearSelectedProducts = function () {
    selectedProducts.value = []
  }

  /**
   * 월별 누적 시뮬레이션 계산 (적금용)
   * @description 적금 상품의 월별 원금/이자 누적을 계산합니다
   * @param {Object} product - 적금 상품 정보
   * @param {number} monthlyAmount - 월 납입액 (기본: 30만원)
   * @returns {Array} 월별 누적 데이터 배열
   */
  const calculateMonthlyAccumulation = function (product, monthlyAmount) {
    if (!product || product.product_type !== 'saving') return []
    
    const months = parseInt(product.save_trm) || 12
    const rate = parseFloat(product.intr_rate2) / 100
    const monthly = monthlyAmount || product.simulation?.monthlyDeposit || 300000
    
    const data = []
    let cumulative = 0
    
    for (let month = 1; month <= months; month++) {
      cumulative += monthly
      // 단리 이자 계산
      const monthlyInterest = monthly * (months - month + 1) * (rate / 12)
      
      data.push({
        month,
        principal: cumulative,
        interest: Math.round(monthly * (month * (month + 1) / 2) * (rate / 12) / month * month),
        total: cumulative + Math.round(monthly * (month * (month + 1) / 2) * (rate / 12)),
      })
    }
    
    return data
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return { 
    // 상태
    API_URL, 
    result, 
    loading, 
    error, 
    selectedProducts,
    // 계산된 속성
    selectedSavings,
    selectedDeposits,
    // 액션
    createAnalysis, 
    fetchResult, 
    resetResult,
    addSelectedProduct,
    removeSelectedProduct,
    isProductSelected,
    clearSelectedProducts,
    calculateMonthlyAccumulation,
  }
}, { persist: true })  // Pinia persist 플러그인: 새로고침 시에도 상태 유지