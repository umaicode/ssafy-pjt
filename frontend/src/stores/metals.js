import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from 'axios'

export const useMetalsStore = defineStore('metals', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const metal = ref('gold')
  const startDate = ref(null)
  const endDate = ref(null)

  const prices = ref([])
  const loading  = ref(false)
  const errorMessage = ref(null)

  const labels = computed(() => 
    prices.value.map(item => item.date)
  )

  const priceValues = computed(() => 
    prices.value.map(item => item.price)
  )

  const isEmpty = computed(() =>
    !loading.value && prices.value.length === 0
  )

  const setMetal = async (newMetal) => {
    metal.value = newMetal
    await loadPrices()
  }

  const setDates = async (start, end) => {
    startDate.value = start
    endDate.value = end
    await loadPrices()
  }

  const resetDates = async () => {
    startDate.value = null
    endDate.value = null
    await loadPrices()
  }

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

  return {
    metal,
    startDate,
    endDate,
    prices,
    loading,
    errorMessage,

    labels,
    priceValues,
    isEmpty,

    setMetal,
    setDates,
    resetDates,
    loadPrices,
  }
}, {persist: true})