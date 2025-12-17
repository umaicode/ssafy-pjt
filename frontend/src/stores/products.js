import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

export const useProductStore = defineStore('products', () => {
  const deposits = ref([])
  const savings = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getDeposits = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/products/deposits/`
    })
    .then(res => {
      deposits.value = res.data
      console.log(res)
      console.log(res.data)
    })
    .catch(err => console.log(err))
  }

  const getSavings = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/products/savings/`
    })
    .then(res => {
      savings.value = res.data
      console.log(res)
      console.log(res.data)
    })
    .catch(err => console.log(err))
  }

  return { deposits, savings, API_URL, getDeposits, getSavings }

}, {persist: true})