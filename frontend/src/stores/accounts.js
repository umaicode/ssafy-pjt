import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { useNewsStore } from "@/stores/news"

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
      nickname.value = null
      
      // 다른 store들 초기화 (뉴스 store 초기화)
      const newsStore = useNewsStore()
      newsStore.clearAllData()
      
      // 로컬 스토리지에서 news store 데이터 제거
      localStorage.removeItem('news')
      
      router.push({ name: 'home' })
    })
    .catch((err) => console.log(err))
  }

  // 회원탈퇴
  const deleteUser = function () {
    // 1️⃣ 사용자 실수 방지용 확인창
    const ok = window.confirm('정말 회원탈퇴 하시겠습니까?\n삭제 후 복구할 수 없습니다.')

    // 취소 누르면 아무 것도 안 함
    if (!ok) return

    // 2️⃣ 확인 누르면 삭제 요청
    axios({
      method: 'delete',
      url: `${API_URL}/accounts/delete/`,
      headers: {
        Authorization: `Token ${token.value}`,
      }
    })
    .then(() => {
      // 3️⃣ 탈퇴 성공 시 프론트 상태 정리
      token.value = null
      nickname.value = null

      alert('계정이 삭제되었습니다.')
      router.push({ name: 'home' })
    })
    .catch(err => {
      console.log(err)
      alert('회원탈퇴에 실패했습니다.')
    })
  }


  // 인증 상태 여부 확인(로그인)
  const isLogin = computed(() => {
    return token.value ? true : false
  })

  // 닉네임 변경 (PATCH /accounts/user/)
  const updateNickname = async function (newNickname) {
    if (!token.value) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'LogInView' })
      return
    }

    try {
      await axios({
        method: 'patch',
        url: `${API_URL}/accounts/update/`,
        data: { nickname: newNickname },
        headers: { Authorization: `Token ${token.value}` },
      })

      // 수정 후 내 정보 갱신
      await getUserInfo()
      alert('닉네임이 수정되었습니다.')
    } catch (err) {
      console.log(err)
      alert('닉네임 수정에 실패했습니다.')
    }
  }


  // 비밀번호 변경 (POST /accounts/password/change/)
  const changePassword = async function (payload) {
    if (!token.value) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'LogInView' })
      return
    }

    const { old_password, new_password1, new_password2 } = payload

    try {
      await axios({
        method: 'post',
        url: `${API_URL}/accounts/password/change/`,
        data: { old_password, new_password1, new_password2 },
        headers: { Authorization: `Token ${token.value}` },
      })

      alert('비밀번호가 변경되었습니다. 다시 로그인해주세요.')

      // 보안상 토큰/닉네임 제거 후 로그인 화면으로
      token.value = null
      nickname.value = null
      router.push({ name: 'LogInView' })
    } catch (err) {
      console.log(err)
      const msg = err?.response?.data
      if (msg) alert(`비밀번호 변경 실패: ${JSON.stringify(msg)}`)
      else alert('비밀번호 변경에 실패했습니다.')
    }
  }


  return { API_URL, signUp, logIn, logOut, token, isLogin, nickname, getUserInfo,
  updateNickname,changePassword, deleteUser,
  }

}, {persist: true})