import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useCommunityStore = defineStore('community', () => {
  const API_BASE = 'http://127.0.0.1:8000/api/v1'

  const articles = ref([])
  const totalPages = ref(1)
  const article = ref(null)
  const comments = ref([])

  // 1) 게시글 목록
  const getArticles = (page = 1) => {
    return axios.get(`${API_BASE}/articles/`, { params: { page } })
      .then((res) => {
        if (Array.isArray(res.data)) {
          articles.value = res.data
          totalPages.value = 10
        } else {
          articles.value = res.data.results ?? []
          totalPages.value = res.data.total_pages ?? 10
        }
      })
      .catch((err) => {
        console.log(err)
        articles.value = []
      })
  }

  // 2) 게시글 생성
  const createArticle = (payload) => {
    return axios.post(`${API_BASE}/articles/`, payload)
      .then((res) => res.data)
  }

  // 3) 게시글 상세
  const getArticleDetail = (id) => {
    return axios.get(`${API_BASE}/articles/${id}/`)
      .then((res) => { article.value = res.data })
      .catch((err) => { console.log(err); article.value = null })
  }

  // 4) 게시글 삭제
  const deleteArticle = (id) => {
    return axios.delete(`${API_BASE}/articles/${id}/`)
      .then(() => { article.value = null })
  }

  // 5) 댓글 목록
  const getComments = (articleId) => {
    return axios.get(`${API_BASE}/articles/${articleId}/comments/`)
      .then((res) => { comments.value = res.data })
      .catch((err) => { console.log(err); comments.value = [] })
  }

  // 6) 댓글 생성
  const createComment = (articleId, content) => {
    return axios.post(`${API_BASE}/articles/${articleId}/comments/create/`, { content })
      .then((res) => {
        comments.value.push(res.data)
        return res.data
      })
  }

  // 7) 댓글 삭제 (comment_detail 재활용 기준)
  const deleteComment = (commentId) => {
    return axios.delete(`${API_BASE}/comments/${commentId}/`)
      .then(() => {
        comments.value = comments.value.filter((c) => c.id !== commentId)
      })
      .catch((err) => {
        console.log(err)
        return Promise.reject(err)
      })
  }

  return {
    API_BASE,
    articles,
    totalPages,
    article,
    comments,
    getArticles,
    createArticle,
    getArticleDetail,
    deleteArticle,
    getComments,
    createComment,
    deleteComment,
  }
})
