import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"


export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()

  // 회원가입 함수
  const signUp = function (payload) {
    const username = payload.username
    const nickname = payload.nickname
    const password1 = payload.password1
    const password2 = payload.password2

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username,
        nickname,
        password1,
        password2,
      }
    })
    .then(res => {
      console.log('회원가입이 완료되었습니다.')
      const password = password1
      logIn({ username, password})
    })
    .catch(err => console.log(err))
  }

  // 로그인 함수
  const logIn = function (payload) {
    const username = payload.username
    const password = payload.password

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username,
        password,
      }
    })
    .then(res => { 
      token.value = res.data.key
      router.push({name: 'home'})
    })
    .catch(err => console.log(err))
  }

  // 로그아웃 함수
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`
    })
    .then((res) => {
      token.value = null
      router.push({ name: 'home' })
    })
    .catch((err) => console.log(err))
  }

  // 인증 상태 여부 확인(로그인)
  const isLogin = computed(() => {
    return token.value ? true : false
  })

  return { API_URL, signUp, logIn, logOut, token, isLogin}

}, {persist: true})