import { defineStore } from "pinia"
import { ref, computed } from "vue"
import axios from "axios"
import { useAccountStore } from "./accounts"


export const useWishlistStore = defineStore("wishlist", () => {
  const accountStore = useAccountStore()
  const API_URL = 'http://127.0.0.1:8000'

  // 상세페이지에서 "현재 상품이 좋아요인지" 표시할 때 쓰는 값
  const liked = ref(false)

  // ✅ 마이페이지에서 보여줄 좋아요 목록
  // 예: [{ fin_prdt_cd, product_type, created_at, kor_co_nm, fin_prdt_nm }, ...]
  const wishlist = ref([])

  const toggleWishlist = function (payload) {
    const fin_prdt_cd = payload.fin_prdt_cd
    const product_type = payload.product_type
    
    axios({
      method: 'post',
      url: `${API_URL}/api/products/wishlist/`,
      data: {
        fin_prdt_cd,
        product_type,
      },
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    })
    .then(res => {
      liked.value = res.data.liked
      // ✅ 토글 후 마이페이지 목록도 최신화(좋아요 목록 화면에서 즉시 반영)
      getWishlist()
    })
    .catch(err => {
      if (err.response.status === 401) {
        alert("로그인이 필요합니다.")
      }
      else {
        console.log(err)
      }
    })
  }

  // ✅ 내 좋아요 목록 가져오기 (마이페이지에서 사용)
  // 1) GET /api/products/wishlist/me/  -> 좋아요한 항목의 (코드/타입/날짜) 목록
  // 2) 각 항목마다 상품 상세 API를 추가로 호출해서 (은행명/상품명) 붙이기
  const getWishlist = function () {
    // 로그인 안 되어 있으면 목록 비우고 끝
    if (!accountStore.token) {
      wishlist.value = []
      return
    }
    axios({
      method: 'get',
      url: `${API_URL}/api/products/wishlist/me/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    })
      .then(res => {
        const baseList = res.data
        // baseList 예시: [{ fin_prdt_cd, product_type, created_at }, ...]

        // ✅ 각 좋아요 항목마다 "상품 상세" 요청을 만들고,
        // Promise.all로 전부 끝나면 한 번에 wishlist에 저장
        const detailPromises = baseList.map(w => {
          return axios({
            method: 'get',
            // product_type이 deposit/saving 이라고 가정 (너 프로젝트 백엔드 구조)
            url: `${API_URL}/api/products/${w.product_type}/${w.fin_prdt_cd}/`,
            headers: {
              'Authorization': `Token ${accountStore.token}`
            }
          })
            .then(detailRes => {
              // base 정보 + 상세 정보(은행명/상품명) 합쳐서 반환
              return {
                ...w,
                kor_co_nm: detailRes.data.kor_co_nm,
                fin_prdt_nm: detailRes.data.fin_prdt_nm,
              }
            })
            .catch(() => {
              // 상세 조회가 실패해도 목록이 깨지지 않게 "최소 정보"로 반환
              return {
                ...w,
                kor_co_nm: '(조회 실패)',
                fin_prdt_nm: w.fin_prdt_cd,
              }
            })
        })

        // 모든 상세 요청이 끝나면 한번에 최종 목록 저장
        // wishlist.value.push(item)와 같음
        Promise.all(detailPromises)  // 좋아요한 모든 상품의 상세 요청이 끝날 때까지 기다림
          .then(enrichedList => {
            wishlist.value = enrichedList  // enrichedList는 최종 결과 배열 한번에 wishlist.value에 넣음
          })
      })
      .catch(err => {
        if (err.response && err.response.status === 401) {
          alert("로그인이 필요합니다.")
        } else {
          console.log(err)
        }
      })
  }

  return { liked, wishlist, getWishlist, toggleWishlist }
})