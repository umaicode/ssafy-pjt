import { defineStore } from "pinia"
import { ref } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { useAccountStore } from "@/stores/accounts"

export const useNewsStore = defineStore('news', () => {
  const newsList = ref([])
  const newsDetail = ref(null)
  const mode = ref('all')   // all | bookmark

  const API_URL = 'http://127.0.0.1:8000'

  const accountStore = useAccountStore()
  const router = useRouter()

  // 목록 조회
  const getNewsList = function () {
    const params = {}
    if (mode.value === 'bookmark') {
      params.mode = 'bookmark'
    }

    axios({
      method: 'get',
      url: `${API_URL}/api/news/`,
      params,
      headers: accountStore.token
        ? { Authorization: `Token ${accountStore.token}` }
        : {}
    })
    .then(res => {
      newsList.value = res.data
      console.log(res.data)
    })
    .catch(err => {
      console.log(err)
      newsList.value = []
    })
  }

  // 상세 조회
  const getNewsDetail = function (newsId) {
    axios({
      method: 'get',
      url: `${API_URL}/api/news/${newsId}/`,
      headers: accountStore.token
        ? { Authorization: `Token ${accountStore.token}` }
        : {}
    })
    .then(res => {
      newsDetail.value = res.data
      console.log(res.data)
    })
    .catch(err => {
      console.log(err)
      newsDetail.value = null
    })
  }

  // 네이버 뉴스 가져오기 -> DB 저장
  const fetchNews = function (query) {
    axios({
      method: 'post',
      url: `${API_URL}/api/news/fetch/`,
      data: { query },
      headers: accountStore.token
        ? { Authorization: `Token ${accountStore.token}` }
        : {}
    })
    .then(res => {
      alert(`새로 저장된 뉴스: ${res.data.created}건`)
      mode.value = 'all'
      getNewsList()
    })
    .catch(err => {
      console.log(err)
      alert('뉴스 가져오기에 실패했습니다.')
    })
  }

  // 북마크 토글 (로그인 필수)
  const toggleBookmark = function (newsId) {
    if (!accountStore.isLogin || !accountStore.token) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'LogInView' })
      return
    }

    axios({
      method: 'post',
      url: `${API_URL}/api/news/${newsId}/bookmark/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    .then(res => {
      const updated = res.data

      // 상세 갱신
      if (newsDetail.value && newsDetail.value.id === updated.id) {
        newsDetail.value = updated
      }

      // 목록 갱신 (있으면 반영)
      const idx = newsList.value.findIndex(n => n.id === updated.id)
      if (idx !== -1) {
        newsList.value[idx] = updated
      }

      // 북마크 모드면 다시 조회
      if (mode.value === 'bookmark') {
        getNewsList()
      }
    })
    .catch(err => {
      console.log(err)
      alert('북마크 변경에 실패했습니다.')
    })
  }

  // 모드 변경 (북마크 모드는 로그인만)
  const setMode = function (newMode) {
    if (newMode === 'bookmark' && (!accountStore.isLogin || !accountStore.token)) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'LogInView' })
      return
    }
    mode.value = newMode
    getNewsList()
  }

  // 상세 비우기
  const clearDetail = function () {
    newsDetail.value = null
  }

  return {
    newsList,
    newsDetail,
    mode,
    API_URL,
    getNewsList,
    getNewsDetail,
    fetchNews,
    toggleBookmark,
    setMode,
    clearDetail,
  }

}, { persist: true })
