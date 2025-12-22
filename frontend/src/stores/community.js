import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useCommunityStore = defineStore('community', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const accountStore = useAccountStore()

  const articles = ref([])
  const totalPages = ref(1)
  const currentPage = ref(1)
  const article = ref(null)
  const comments = ref([])

  // 1) 게시글 목록 (페이지네이션)
  const getArticles = (page = 1) => {
    return axios.get(`${API_URL}/api/v1/articles/`, { params: { page } })
      .then((res) => {
        articles.value = res.data.results ?? []
        totalPages.value = res.data.total_pages ?? 1
        currentPage.value = res.data.current_page ?? 1
      })
      .catch((err) => {
        console.log(err)
        articles.value = []
      })
  }

  // 2) 게시글 생성
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

  // 3) 게시글 상세
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
        console.log(err)
        article.value = null
      })
  }


  // 4) 게시글 수정
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

  // 5) 게시글 삭제
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

  // 6) 댓글 목록
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
        console.log(err)
        comments.value = []
      })
  }

  // 7) 댓글 생성
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
        comments.value.unshift(res.data)
        return res.data
      })
  }

  // 8) 댓글 수정
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
        const idx = comments.value.findIndex((c) => c.id === commentId)
        if (idx !== -1) {
          comments.value[idx] = res.data
        }
        return res.data
      })
  }

  // 9) 댓글 삭제
  const deleteComment = (commentId) => {
    return axios({
      method: 'delete',
      url: `${API_URL}/api/v1/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(() => {
        comments.value = comments.value.filter((c) => c.id !== commentId)
      })
      .catch((err) => {
        console.log(err)
        return Promise.reject(err)
      })
  }

  // ✅ 게시글 좋아요 토글
  const toggleArticleLike = function (articleId) {
    return axios({
      method: "post",
      url: `${API_URL}/api/v1/articles/${articleId}/like/`,
      headers: accountStore.token ? { Authorization: `Token ${accountStore.token}` } : {},
    })
      .then((res) => {
        // res.data = { liked, likes_count }
        if (article.value) {
          article.value.is_liked = res.data.liked
          article.value.likes_count = res.data.likes_count
        }
      })
  }

  // ✅ 댓글 좋아요 토글 추가
  const toggleCommentLike = function (commentId) {
    return axios({
      method: "post",
      url: `${API_URL}/api/v1/comments/${commentId}/like/`,
      headers: accountStore.token
        ? { Authorization: `Token ${accountStore.token}` }
        : {}, // 로그인 체크는 안 하지만 토큰 있으면 넣기
    })
      .then((res) => {
        // res.data = { liked, likes_count }

        // ✅ store.comments에서 해당 댓글 찾아 값 갱신
        const target = comments.value.find((c) => c.id === commentId)
        if (target) {
          target.is_liked = res.data.liked
          target.likes_count = res.data.likes_count
        }
      })
      .catch((err) => {
        console.log("toggleCommentLike 실패:", err)
        throw err
      })
  }

  return {
    API_URL,
    articles,
    totalPages,
    currentPage,
    article,
    comments,
    getArticles,
    createArticle,
    getArticleDetail,
    updateArticle,
    deleteArticle,
    getComments,
    createComment,
    updateComment,
    deleteComment,
    toggleArticleLike,
    toggleCommentLike,
  }
})
