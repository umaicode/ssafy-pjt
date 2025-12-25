/**
 * @파일명 like.js
 * @설명 금융 상품 좋아요 관리 스토어
 * @기능
 *   - 좋아요 토글 (toggleLike)
 *   - 내 좋아요 목록 조회 (getLikes)
 * @API엔드포인트
 *   - POST /api/products/likes/toggle/ : 좋아요 토글
 *   - GET /api/products/likes/me/ : 내 좋아요 목록
 */

import { defineStore } from "pinia"
import { ref } from "vue"
import axios from "axios"
import { useAccountStore } from "./accounts"

export const useLikeStore = defineStore("like", () => {
  // ========================================
  // 의존성 주입
  // ========================================
  const accountStore = useAccountStore()
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = "http://127.0.0.1:8000"

  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {Ref<boolean>} 현재 상품의 좋아요 상태 (상세페이지용) */
  const liked = ref(false)

  /** @type {Ref<number>} 현재 상품의 좋아요 개수 */
  const likesCount = ref(0)

  /** 
   * @type {Ref<Array>} 내 좋아요 목록 (마이페이지용)
   * @example [{ fin_prdt_cd, product_type, created_at, kor_co_nm, fin_prdt_nm }, ...]
   */
  const likes = ref([])

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 좋아요 토글
   * @description 상품의 좋아요 상태를 토글합니다
   * @param {Object} payload - 상품 정보
   * @param {string} payload.fin_prdt_cd - 상품 코드
   * @param {string} payload.product_type - 상품 타입 ('deposit' | 'saving')
   * @returns {Promise} API 응답 Promise
   */
  const toggleLike = function (payload) {
    const fin_prdt_cd = payload.fin_prdt_cd
    const product_type = payload.product_type

    return axios({
      method: "post",
      url: `${API_URL}/api/products/likes/toggle/`,
      data: {
        fin_prdt_cd,
        product_type,
      },
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        // 응답 데이터로 상태 업데이트
        liked.value = res.data.liked
        likesCount.value = res.data.likes_count

        // 마이페이지 목록도 최신화
        getLikes()
      })
      .catch((err) => {
        if (err.response && err.response.status === 401) {
          alert("로그인이 필요합니다.")
        } else {
          console.error("좋아요 토글 실패:", err)
        }
        throw err
      })
  }

  /**
   * 내 좋아요 목록 가져오기
   * @description 마이페이지에서 좋아요한 상품 목록을 표시할 때 사용합니다
   * @returns {Promise} API 응답 Promise
   */
  const getLikes = function () {
    // 로그인 안 되어 있으면 목록 비우고 종료
    if (!accountStore.token) {
      likes.value = []
      return
    }

    return axios({
      method: "get",
      url: `${API_URL}/api/products/likes/me/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        const baseList = res.data

        // 각 항목에 상품 상세 정보(은행명, 상품명) 추가
        const detailPromises = baseList.map((w) => {
          return axios({
            method: "get",
            url: `${API_URL}/api/products/${w.product_type}/${w.fin_prdt_cd}/`,
            headers: {
              Authorization: `Token ${accountStore.token}`,
            },
          })
            .then((detailRes) => {
              return {
                ...w,
                kor_co_nm: detailRes.data.kor_co_nm,
                fin_prdt_nm: detailRes.data.fin_prdt_nm,
              }
            })
            .catch(() => {
              // 상세 조회 실패 시 기본값 설정
              return {
                ...w,
                kor_co_nm: "(조회 실패)",
                fin_prdt_nm: w.fin_prdt_cd,
              }
            })
        })

        // 모든 상세 조회가 완료되면 목록 업데이트
        return Promise.all(detailPromises).then((enrichedList) => {
          likes.value = enrichedList
        })
      })
      .catch((err) => {
        if (err.response && err.response.status === 401) {
          alert("로그인이 필요합니다.")
        } else {
          console.error("좋아요 목록 조회 실패:", err)
        }
        throw err
      })
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return {
    // 상태
    liked,
    likesCount,
    likes,
    // 액션
    toggleLike,
    getLikes,
  }
})
