import { defineStore } from "pinia"
import { ref, computed } from "vue"
import axios from "axios"
import { useAccountStore } from "./accounts"


export const useWishlistStore = defineStore("wishlist", () => {
  const accountStore = useAccountStore()
  const API_URL = 'http://127.0.0.1:8000'
  const liked = ref(false)

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

  return { liked, toggleWishlist }
})