import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

export const useProductStore = defineStore('products', () => {
  const products = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/products/deposits/`
    })
    .then(res => {
      products.value = res.data
      console.log(res)
      console.log(res.data)
    })
    .catch(err => console.log(err))
  }

  return { products, API_URL, getProducts }

}, {persist: true})