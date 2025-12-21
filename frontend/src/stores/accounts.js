import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()
  const nickname = ref(null)

  // 닉네임 가져오는 함수
  const getUserInfo = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(res => {
      nickname.value = res.data.nickname
    })
  }

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
    .then(async (res) => { 
      token.value = res.data.key
      await getUserInfo()
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

  // ---------------------------------(확인중)
    // ✅ 닉네임 변경 (PATCH /accounts/user/)
  const updateNickname = function (newNickname) {
    if (!token.value) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'LogInView' })
      return Promise.reject('need login')
    }

    return axios({
      method: 'patch',
      url: `${API_URL}/accounts/user/`,
      data: { nickname: newNickname },
      headers: { Authorization: `Token ${token.value}` }
    })
    .then(async () => {
      // 서버 반영 후 내 정보 다시 가져와서 상단 닉네임 즉시 갱신
      await getUserInfo()
      alert('닉네임이 수정되었습니다.')
    })
    .catch(err => {
      console.log(err)
      alert('닉네임 수정에 실패했습니다.')
      return Promise.reject(err)
    })
  }

  // ✅ 비밀번호 변경 (dj-rest-auth 기본: POST /accounts/password/change/)
  // payload: { old_password, new_password1, new_password2 }
  const changePassword = function (payload) {
    if (!token.value) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'LogInView' })
      return Promise.reject('need login')
    }

    const old_password = payload.old_password
    const new_password1 = payload.new_password1
    const new_password2 = payload.new_password2

    return axios({
      method: 'post',
      url: `${API_URL}/accounts/password/change/`,
      data: { old_password, new_password1, new_password2 },
      headers: { Authorization: `Token ${token.value}` }
    })
    .then(() => {
      alert('비밀번호가 변경되었습니다. 다시 로그인해주세요.')
      // 보안상 토큰 제거 후 로그인으로 이동 권장
      token.value = null
      nickname.value = null
      router.push({ name: 'LogInView' })
    })
    .catch(err => {
      console.log(err)
      // 서버에서 에러 메시지 내려주면 보여주기(선택)
      const msg = err?.response?.data
      if (msg) {
        alert(`비밀번호 변경 실패: ${JSON.stringify(msg)}`)
      } else {
        alert('비밀번호 변경에 실패했습니다.')
      }
      return Promise.reject(err)
    })
  }

  return { API_URL, signUp, logIn, logOut, token, isLogin, nickname, getUserInfo,
        updateNickname,   // ✅ 추가
    changePassword,   // ✅ 추가
  }

}, {persist: true})