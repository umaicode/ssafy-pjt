import { defineStore } from "pinia";
import axios from "axios";
import { ref, computed } from "vue";
import { useAccountStore } from "@/stores/accounts";
import { useRouter } from "vue-router";

export const useAnalysisStore = defineStore('analysis', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const result = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const router = useRouter()

  // 선택된 상품 목록 (마이페이지 그래프용)
  const selectedProducts = ref([])

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
      console.log('[analysis create]', res.data)
      router.push(`/analysis/${res.data.analysis_id}/result`)
    })
    .catch(err => {
      console.error('[analysis create error]', err)
      console.log('🔥 server response data =', err.response?.data) // ✅ 추가
      error.value = err
      throw err
    })
    .finally(() => {
      loading.value = false
    })
  }

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
      console.log('[analysis result]', res.data)
      result.value = res.data
    })
    .catch(err => {
      console.error('[analysis result error]', err)
      error.value = err
    })
    .finally(() => {
      loading.value = false
    })
  }

  const resetResult = function () {
    result.value = null
    error.value = null
  }

  // === 선택된 상품 관리 기능 ===
  
  // 상품 선택 추가
  const addSelectedProduct = function (product) {
    const exists = selectedProducts.value.find(
      p => p.fin_prdt_cd === product.fin_prdt_cd && p.product_type === product.product_type
    )
    if (!exists) {
      selectedProducts.value.push(product)
    }
  }

  // 상품 선택 해제
  const removeSelectedProduct = function (fin_prdt_cd, product_type) {
    selectedProducts.value = selectedProducts.value.filter(
      p => !(p.fin_prdt_cd === fin_prdt_cd && p.product_type === product_type)
    )
  }

  // 상품이 선택되어 있는지 확인
  const isProductSelected = function (fin_prdt_cd, product_type) {
    return selectedProducts.value.some(
      p => p.fin_prdt_cd === fin_prdt_cd && p.product_type === product_type
    )
  }

  // 선택된 상품 전체 초기화
  const clearSelectedProducts = function () {
    selectedProducts.value = []
  }

  // 월별 누적 시뮬레이션 계산 (적금)
  const calculateMonthlyAccumulation = function (product, monthlyAmount) {
    if (!product || product.product_type !== 'saving') return []
    
    const months = parseInt(product.save_trm) || 12
    const rate = parseFloat(product.intr_rate2) / 100
    const monthly = monthlyAmount || product.simulation?.monthlyDeposit || 300000
    
    const data = []
    let cumulative = 0
    let totalInterest = 0
    
    for (let month = 1; month <= months; month++) {
      cumulative += monthly
      // 단리 이자 계산 (해당 월까지의 누적 이자)
      const monthlyInterest = monthly * (months - month + 1) * (rate / 12)
      totalInterest += monthly * (rate / 12)
      
      data.push({
        month,
        principal: cumulative,
        interest: Math.round(monthly * (month * (month + 1) / 2) * (rate / 12) / month * month), // 현재까지 예상 이자
        total: cumulative + Math.round(monthly * (month * (month + 1) / 2) * (rate / 12)),
      })
    }
    
    return data
  }

  // 선택된 적금 상품들
  const selectedSavings = computed(() => 
    selectedProducts.value.filter(p => p.product_type === 'saving')
  )

  // 선택된 예금 상품들
  const selectedDeposits = computed(() => 
    selectedProducts.value.filter(p => p.product_type === 'deposit')
  )

  return { 
    API_URL, 
    result, 
    loading, 
    error, 
    selectedProducts,
    selectedSavings,
    selectedDeposits,
    createAnalysis, 
    fetchResult, 
    resetResult,
    addSelectedProduct,
    removeSelectedProduct,
    isProductSelected,
    clearSelectedProducts,
    calculateMonthlyAccumulation,
  }
}, {persist: true})