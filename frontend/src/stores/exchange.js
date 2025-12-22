import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useExchangeStore = defineStore('exchange', () => {
  const rates = ref([])
  const loading = ref(false)
  const error = ref(null)
  const lastUpdated = ref(null)

  const API_URL = 'http://127.0.0.1:8000'

  // 환율 데이터를 외부 API에서 가져와 DB에 저장
  const fetchAndSaveExchangeRates = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post(`${API_URL}/api/exchange/fetch/`)
      console.log('환율 API 호출 성공:', response.data)
      
      // 저장 후 DB에서 조회
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

  // DB에서 환율 데이터 조회
  const getExchangeRates = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/api/exchange/rates/`)
      rates.value = response.data.rates || []
      
      // localStorage에 캐싱
      if (rates.value.length > 0) {
        localStorage.setItem('exchangeRates', JSON.stringify(rates.value))
        localStorage.setItem('exchangeLastUpdated', new Date().toISOString())
        lastUpdated.value = rates.value[0]?.updated_at || null
      }
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || '환율 정보를 불러오는데 실패했습니다.'
      console.error('환율 조회 에러:', err)
      
      // 에러 시 localStorage에서 로드
      loadFromCache()
      
      throw err
    } finally {
      loading.value = false
    }
  }

  // localStorage에서 캐시된 데이터 로드
  const loadFromCache = () => {
    const cachedRates = localStorage.getItem('exchangeRates')
    const cachedDate = localStorage.getItem('exchangeLastUpdated')
    
    if (cachedRates) {
      rates.value = JSON.parse(cachedRates)
      lastUpdated.value = cachedDate
    }
  }

  // 초기화 시 캐시에서 로드
  loadFromCache()

  return {
    rates,
    loading,
    error,
    lastUpdated,
    fetchAndSaveExchangeRates,
    getExchangeRates,
    loadFromCache
  }
})
