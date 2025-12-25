/**
 * @파일명 news.js
 * @설명 금융 뉴스 관리 스토어
 * @기능
 *   - 뉴스 목록 조회 (getNewsList)
 *   - 뉴스 상세 조회 (getNewsDetail)
 *   - 네이버 뉴스 검색 및 저장 (fetchNews)
 *   - 북마크 토글 (toggleBookmark)
 * @API엔드포인트
 *   - GET /api/news/ : 뉴스 목록 조회
 *   - GET /api/news/:id/ : 뉴스 상세 조회
 *   - POST /api/news/fetch/ : 네이버 뉴스 검색/저장
 *   - POST /api/news/:id/bookmark/ : 북마크 토글
 */

import { defineStore } from "pinia"
import { ref } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { useAccountStore } from "@/stores/accounts"

export const useNewsStore = defineStore('news', () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<Array>} 뉴스 목록 */
  const newsList = ref([])
  
  /** @type {Ref<Object|null>} 현재 선택된 뉴스 상세 정보 */
  const newsDetail = ref(null)
  
  /** @type {Ref<string>} 보기 모드 ('all' | 'bookmark') */
  const mode = ref('all')
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = 'http://127.0.0.1:8000'

  const accountStore = useAccountStore()
  const router = useRouter()

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 뉴스 목록 조회
   * @description 모드에 따라 전체 뉴스 또는 북마크된 뉴스만 조회합니다
   */
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
    })
    .catch(err => {
      console.error('뉴스 목록 조회 실패:', err)
      newsList.value = []
    })
  }

  /**
   * 뉴스 상세 조회
   * @description 특정 뉴스의 상세 정보를 가져옵니다
   * @param {number} newsId - 뉴스 ID
   */
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
    })
    .catch(err => {
      console.error('뉴스 상세 조회 실패:', err)
      newsDetail.value = null
    })
  }

  /**
   * 네이버 뉴스 검색 및 DB 저장
   * @description 네이버 API로 뉴스를 검색하고 DB에 저장합니다
   * @param {string} query - 검색 키워드
   */
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
      console.error('뉴스 가져오기 실패:', err)
      alert('뉴스 가져오기에 실패했습니다.')
    })
  }

  /**
   * 북마크 토글
   * @description 뉴스의 북마크 상태를 토글합니다 (로그인 필수)
   * @param {number} newsId - 뉴스 ID
   */
  const toggleBookmark = function (newsId) {
    // 로그인 체크
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

      // 상세 페이지 데이터 갱신
      if (newsDetail.value && newsDetail.value.id === updated.id) {
        newsDetail.value = updated
      }

      // 목록에서도 해당 뉴스 정보 갱신
      const idx = newsList.value.findIndex(n => n.id === updated.id)
      if (idx !== -1) {
        newsList.value[idx] = updated
      }

      // 북마크 모드에서는 목록 다시 조회 (북마크 해제된 항목 제거)
      if (mode.value === 'bookmark') {
        getNewsList()
      }
    })
    .catch(err => {
      console.error('북마크 변경 실패:', err)
      alert('북마크 변경에 실패했습니다.')
    })
  }

  /**
   * 보기 모드 변경
   * @description 전체보기/북마크보기 모드를 변경합니다
   * @param {string} newMode - 'all' 또는 'bookmark'
   */
  const setMode = function (newMode) {
    // 북마크 모드는 로그인 필수
    if (newMode === 'bookmark' && (!accountStore.isLogin || !accountStore.token)) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'LogInView' })
      return
    }
    mode.value = newMode
    getNewsList()
  }

  /**
   * 상세 정보 초기화
   * @description 뉴스 상세 데이터를 비웁니다
   */
  const clearDetail = function () {
    newsDetail.value = null
  }

  /**
   * 전체 데이터 초기화
   * @description 로그아웃 시 모든 뉴스 데이터를 초기화합니다
   */
  const clearAllData = function () {
    newsList.value = []
    newsDetail.value = null
    mode.value = 'all'
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    newsList,
    newsDetail,
    mode,
    API_URL,
    // 액션
    getNewsList,
    getNewsDetail,
    fetchNews,
    toggleBookmark,
    setMode,
    clearDetail,
    clearAllData,
  }

})
