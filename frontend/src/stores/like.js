import { defineStore } from "pinia"
import { ref } from "vue"
import axios from "axios"
import { useAccountStore } from "./accounts"

export const useLikeStore = defineStore("like", () => {
  const accountStore = useAccountStore()
  const API_URL = "http://127.0.0.1:8000"

  // ✅ 상세페이지에서 "현재 상품이 좋아요인지" 표시할 때 쓰는 값
  const liked = ref(false)

  // ✅ 좋아요 개수 표시용 (상품 상세에서 바로 보여주기)
  const likesCount = ref(0)

  // ✅ 마이페이지에서 보여줄 좋아요 목록
  // 예: [{ fin_prdt_cd, product_type, created_at, kor_co_nm, fin_prdt_nm }, ...]
  const likes = ref([])

  // ✅ 좋아요 토글
  // payload: { fin_prdt_cd, product_type }
  const toggleLike = function (payload) {
    const fin_prdt_cd = payload.fin_prdt_cd
    const product_type = payload.product_type

    return axios({
      method: "post",
      // ✅ [변경] wishlist -> likes 토글 엔드포인트로
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
        // res.data = { liked: boolean, likes_count: number }
        liked.value = res.data.liked
        likesCount.value = res.data.likes_count

        // ✅ 토글 후 마이페이지 목록도 최신화(좋아요 목록 화면에서 즉시 반영)
        getLikes()
      })
      .catch((err) => {
        if (err.response && err.response.status === 401) {
          alert("로그인이 필요합니다.")
        } else {
          console.log(err)
        }
        throw err
      })
  }

  // ✅ 내 좋아요 목록 가져오기 (마이페이지에서 사용)
  // 1) GET /api/products/likes/me/  -> 좋아요한 항목의 (코드/타입/날짜) 목록
  // 2) 각 항목마다 상품 상세 API를 추가로 호출해서 (은행명/상품명) 붙이기
  const getLikes = function () {
    // 로그인 안 되어 있으면 목록 비우고 끝
    if (!accountStore.token) {
      likes.value = []
      return
    }

    return axios({
      method: "get",
      // ✅ [변경] wishlist/me -> likes/me
      url: `${API_URL}/api/products/likes/me/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        const baseList = res.data
        // baseList 예시: [{ fin_prdt_cd, product_type, created_at }, ...]

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
              return {
                ...w,
                kor_co_nm: "(조회 실패)",
                fin_prdt_nm: w.fin_prdt_cd,
              }
            })
        })

        return Promise.all(detailPromises).then((enrichedList) => {
          likes.value = enrichedList
        })
      })
      .catch((err) => {
        if (err.response && err.response.status === 401) {
          alert("로그인이 필요합니다.")
        } else {
          console.log(err)
        }
        throw err
      })
  }

  return {
    liked,
    likesCount,
    likes,
    toggleLike,
    getLikes,
  }
})
