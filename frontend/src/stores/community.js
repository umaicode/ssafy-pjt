/**
 * @파일명 community.js
 * @설명 커뮤니티 게시판 스토어
 * @기능
 *   - 게시글 CRUD (목록, 생성, 상세, 수정, 삭제)
 *   - 댓글 CRUD (목록, 생성, 수정, 삭제)
 *   - 게시글/댓글 좋아요 토글
 * @API엔드포인트
 *   - GET /api/v1/articles/ : 게시글 목록 (페이지네이션)
 *   - POST /api/v1/articles/ : 게시글 생성
 *   - GET /api/v1/articles/:id/ : 게시글 상세
 *   - PATCH /api/v1/articles/:id/ : 게시글 수정
 *   - DELETE /api/v1/articles/:id/ : 게시글 삭제
 *   - POST /api/v1/articles/:id/like/ : 게시글 좋아요 토글
 *   - GET /api/v1/articles/:id/comments/ : 댓글 목록
 *   - POST /api/v1/articles/:id/comments/create/ : 댓글 생성
 *   - PATCH /api/v1/comments/:id/ : 댓글 수정
 *   - DELETE /api/v1/comments/:id/ : 댓글 삭제
 *   - POST /api/v1/comments/:id/like/ : 댓글 좋아요 토글
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useCommunityStore = defineStore('community', () => {
  // ========================================
  // 의존성 주입
  // ========================================
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = 'http://127.0.0.1:8000'
  const accountStore = useAccountStore()

  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<Array>} 게시글 목록 */
  const articles = ref([])
  
  /** @type {Ref<number>} 전체 페이지 수 */
  const totalPages = ref(1)
  
  /** @type {Ref<number>} 현재 페이지 번호 */
  const currentPage = ref(1)
  
  /** @type {Ref<Object|null>} 현재 게시글 상세 */
  const article = ref(null)
  
  /** @type {Ref<Array>} 현재 게시글의 댓글 목록 */
  const comments = ref([])

  // ========================================
  // 액션 (Actions) - 게시글 관련
  // ========================================

  /**
   * 게시글 목록 조회
   * @description 페이지네이션이 적용된 게시글 목록을 가져옵니다
   * @param {number} page - 조회할 페이지 번호 (기본: 1)
   * @returns {Promise} API 응답 Promise
   */
  const getArticles = (page = 1) => {
    return axios.get(`${API_URL}/api/v1/articles/`, { params: { page } })
      .then((res) => {
        articles.value = res.data.results ?? []
        totalPages.value = res.data.total_pages ?? 1
        currentPage.value = res.data.current_page ?? 1
      })
      .catch((err) => {
        console.error('게시글 목록 조회 실패:', err)
        articles.value = []
      })
  }

  /**
   * 게시글 생성
   * @description 새로운 게시글을 작성합니다
   * @param {Object} payload - 게시글 데이터 (title, content)
   * @returns {Promise<Object>} 생성된 게시글 데이터
   */
  const createArticle = (payload) => {
    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => res.data)
  }

  /**
   * 게시글 상세 조회
   * @description 특정 게시글의 상세 정보를 가져옵니다
   * @param {number} id - 게시글 ID
   * @returns {Promise} API 응답 Promise
   */
  const getArticleDetail = (id) => {
    return axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/${id}/`,
      headers: accountStore.token
        ? { Authorization: `Token ${accountStore.token}` }
        : {},
    })
      .then((res) => {
        article.value = res.data
      })
      .catch((err) => {
        console.error('게시글 상세 조회 실패:', err)
        article.value = null
      })
  }

  /**
   * 게시글 수정
   * @description 기존 게시글을 수정합니다
   * @param {number} id - 게시글 ID
   * @param {Object} payload - 수정할 데이터
   * @returns {Promise<Object>} 수정된 게시글 데이터
   */
  const updateArticle = (id, payload) => {
    return axios({
      method: 'patch',
      url: `${API_URL}/api/v1/articles/${id}/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        article.value = res.data
        return res.data
      })
  }

  /**
   * 게시글 삭제
   * @description 게시글을 삭제합니다
   * @param {number} id - 게시글 ID
   * @returns {Promise} API 응답 Promise
   */
  const deleteArticle = (id) => {
    return axios({
      method: 'delete',
      url: `${API_URL}/api/v1/articles/${id}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(() => { article.value = null })
  }

  /**
   * 게시글 좋아요 토글
   * @description 게시글의 좋아요 상태를 토글합니다
   * @param {number} articleId - 게시글 ID
   * @returns {Promise} API 응답 Promise
   */
  const toggleArticleLike = function (articleId) {
    return axios({
      method: "post",
      url: `${API_URL}/api/v1/articles/${articleId}/like/`,
      headers: accountStore.token ? { Authorization: `Token ${accountStore.token}` } : {},
    })
      .then((res) => {
        // 현재 게시글의 좋아요 상태 업데이트
        if (article.value) {
          article.value.is_liked = res.data.liked
          article.value.likes_count = res.data.likes_count
        }
      })
  }

  // ========================================
  // 액션 (Actions) - 댓글 관련
  // ========================================

  /**
   * 댓글 목록 조회
   * @description 특정 게시글의 댓글 목록을 가져옵니다
   * @param {number} articleId - 게시글 ID
   * @returns {Promise} API 응답 Promise
   */
  const getComments = (articleId) => {
    return axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/${articleId}/comments/`,
      headers: accountStore.token
        ? { Authorization: `Token ${accountStore.token}` }
        : {},
    })
      .then((res) => {
        comments.value = res.data
      })
      .catch((err) => {
        console.error('댓글 목록 조회 실패:', err)
        comments.value = []
      })
  }

  /**
   * 댓글 생성
   * @description 새로운 댓글을 작성합니다
   * @param {number} articleId - 게시글 ID
   * @param {string} content - 댓글 내용
   * @returns {Promise<Object>} 생성된 댓글 데이터
   */
  const createComment = (articleId, content) => {
    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/${articleId}/comments/create/`,
      data: { content },
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        // 새 댓글을 목록 맨 앞에 추가
        comments.value.unshift(res.data)
        return res.data
      })
  }

  /**
   * 댓글 수정
   * @description 기존 댓글을 수정합니다
   * @param {number} commentId - 댓글 ID
   * @param {string} content - 수정할 내용
   * @returns {Promise<Object>} 수정된 댓글 데이터
   */
  const updateComment = (commentId, content) => {
    return axios({
      method: 'patch',
      url: `${API_URL}/api/v1/comments/${commentId}/`,
      data: { content },
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        // 목록에서 해당 댓글 업데이트
        const idx = comments.value.findIndex((c) => c.id === commentId)
        if (idx !== -1) {
          comments.value[idx] = res.data
        }
        return res.data
      })
  }

  /**
   * 댓글 삭제
   * @description 댓글을 삭제합니다
   * @param {number} commentId - 댓글 ID
   * @returns {Promise} API 응답 Promise
   */
  const deleteComment = (commentId) => {
    return axios({
      method: 'delete',
      url: `${API_URL}/api/v1/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(() => {
        // 목록에서 해당 댓글 제거
        comments.value = comments.value.filter((c) => c.id !== commentId)
      })
      .catch((err) => {
        console.error('댓글 삭제 실패:', err)
        return Promise.reject(err)
      })
  }

  /**
   * 댓글 좋아요 토글
   * @description 댓글의 좋아요 상태를 토글합니다
   * @param {number} commentId - 댓글 ID
   * @returns {Promise} API 응답 Promise
   */
  const toggleCommentLike = function (commentId) {
    return axios({
      method: "post",
      url: `${API_URL}/api/v1/comments/${commentId}/like/`,
      headers: accountStore.token
        ? { Authorization: `Token ${accountStore.token}` }
        : {},
    })
      .then((res) => {
        // 목록에서 해당 댓글의 좋아요 상태 업데이트
        const target = comments.value.find((c) => c.id === commentId)
        if (target) {
          target.is_liked = res.data.liked
          target.likes_count = res.data.likes_count
        }
      })
      .catch((err) => {
        console.error("댓글 좋아요 토글 실패:", err)
        throw err
      })
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    API_URL,
    articles,
    totalPages,
    currentPage,
    article,
    comments,
    // 게시글 액션
    getArticles,
    createArticle,
    getArticleDetail,
    updateArticle,
    deleteArticle,
    toggleArticleLike,
    // 댓글 액션
    getComments,
    createComment,
    updateComment,
    deleteComment,
    toggleCommentLike,
  }
})
