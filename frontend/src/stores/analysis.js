import { defineStore } from "pinia";
import axios from "axios";
import { ref } from "vue";
import { useAccountStore } from "@/stores/accounts";
import { useRouter } from "vue-router";

export const useAnalysisStore = defineStore('analysis', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const result = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const router = useRouter()

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

  return { API_URL, result, loading, error, createAnalysis, fetchResult, resetResult }
}, {persist: true})