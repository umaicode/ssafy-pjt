/**
 * @파일명 accounts.js
 * @설명 사용자 인증 및 계정 관리 스토어
 * @기능
 *   - 회원가입 (signUp)
 *   - 로그인/로그아웃 (logIn, logOut)
 *   - 회원탈퇴 (deleteUser)
 *   - 닉네임 변경 (updateNickname)
 *   - 비밀번호 변경 (changePassword)
 * @API엔드포인트
 *   - POST /accounts/signup/ : 회원가입
 *   - POST /accounts/login/ : 로그인
 *   - POST /accounts/logout/ : 로그아웃
 *   - DELETE /accounts/delete/ : 회원탈퇴
 *   - PATCH /accounts/update/ : 닉네임 수정
 *   - POST /accounts/password/change/ : 비밀번호 변경
 */

import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { useNewsStore } from "@/stores/news"
import { useExchangeStore } from './exchange'


export const useAccountStore = defineStore('account', () => {
  // ========================================
  // 상태 (State)
  // ========================================
  
  /** @type {string} 백엔드 API 기본 URL */
  const API_URL = 'http://127.0.0.1:8000'
  
  /** @type {Ref<string|null>} 인증 토큰 (로그인 시 발급) */
  const token = ref(null)
  
  /** @type {Ref<string|null>} 사용자 닉네임 */
  const nickname = ref(null)
  
  /** @type {Router} Vue Router 인스턴스 */
  const router = useRouter()

  // ========================================
  // 계산된 속성 (Getters)
  // ========================================
  
  /**
   * 로그인 여부 확인
   * @returns {boolean} 로그인 상태
   */
  const isLogin = computed(() => {
    return token.value ? true : false
  })

  // ========================================
  // 액션 (Actions)
  // ========================================

  /**
   * 사용자 정보 조회
   * @description 로그인된 사용자의 닉네임 정보를 가져옵니다
   * @returns {Promise} API 응답 Promise
   */
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

  /**
   * 회원가입
   * @description 새 사용자를 등록하고 자동으로 로그인 처리합니다
   * @param {Object} payload - 회원가입 정보
   * @param {string} payload.username - 아이디
   * @param {string} payload.nickname - 닉네임
   * @param {string} payload.password1 - 비밀번호
   * @param {string} payload.password2 - 비밀번호 확인
   */
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
      // 회원가입 성공 시 자동 로그인
      const password = password1
      logIn({ username, password })
    })
    .catch(err => {
      console.error('회원가입 실패:', err)
    })
  }

  /**
   * 로그인
   * @description 사용자 인증 후 토큰을 저장하고 환율 정보를 불러옵니다
   * @param {Object} payload - 로그인 정보
   * @param {string} payload.username - 아이디
   * @param {string} payload.password - 비밀번호
   */
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
      // 토큰 저장 및 사용자 정보 조회
      token.value = res.data.key
      await getUserInfo()
      
      // 로그인 성공 시 환율 데이터 가져와서 DB에 저장
      const exchangeStore = useExchangeStore()
      try {
        await exchangeStore.fetchAndSaveExchangeRates()
      } catch (err) {
        console.warn('환율 정보를 가져오지 못했습니다:', err)
      }
      
      router.push({ name: 'home' })
    })
    .catch(err => {
      console.error('로그인 실패:', err)
    })
  }

  /**
   * 로그아웃
   * @description 서버에 로그아웃 요청 후 로컬 상태를 초기화합니다
   */
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`
    })
    .then((res) => {
      // 상태 초기화
      token.value = null
      nickname.value = null
      
      // 다른 store들 초기화 (뉴스 store 초기화)
      const newsStore = useNewsStore()
      newsStore.clearAllData()
      
      // 로컬 스토리지에서 news store 데이터 제거
      localStorage.removeItem('news')
      
      router.push({ name: 'home' })
    })
    .catch((err) => {
      console.error('로그아웃 실패:', err)
    })
  }

  /**
   * 회원탈퇴
   * @description 확인 후 계정을 영구 삭제합니다
   */
  const deleteUser = function () {
    // 사용자 실수 방지용 확인창
    const ok = window.confirm('정말 회원탈퇴 하시겠습니까?\n삭제 후 복구할 수 없습니다.')

    // 취소 시 아무 것도 안 함
    if (!ok) return

    // 확인 시 삭제 요청
    axios({
      method: 'delete',
      url: `${API_URL}/accounts/delete/`,
      headers: {
        Authorization: `Token ${token.value}`,
      }
    })
    .then(() => {
      // 탈퇴 성공 시 프론트 상태 정리
      token.value = null
      nickname.value = null

      alert('계정이 삭제되었습니다.')
      router.push({ name: 'home' })
    })
    .catch(err => {
      console.error('회원탈퇴 실패:', err)
      alert('회원탈퇴에 실패했습니다.')
    })
  }

  /**
   * 닉네임 변경
   * @description 사용자의 닉네임을 수정합니다
   * @param {string} newNickname - 새 닉네임
   */
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
      console.error('닉네임 수정 실패:', err)
      alert('닉네임 수정에 실패했습니다.')
    }
  }

  /**
   * 비밀번호 변경
   * @description 비밀번호 변경 후 재로그인을 요구합니다
   * @param {Object} payload - 비밀번호 변경 정보
   * @param {string} payload.old_password - 현재 비밀번호
   * @param {string} payload.new_password1 - 새 비밀번호
   * @param {string} payload.new_password2 - 새 비밀번호 확인
   */
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
      console.error('비밀번호 변경 실패:', err)
      const msg = err?.response?.data
      if (msg) alert(`비밀번호 변경 실패: ${JSON.stringify(msg)}`)
      else alert('비밀번호 변경에 실패했습니다.')
    }
  }

  // ========================================
  // 반환 (Export)
  // ========================================
  return { 
    // 상태
    API_URL, 
    token, 
    nickname,
    // 계산된 속성
    isLogin, 
    // 액션
    signUp, 
    logIn, 
    logOut, 
    getUserInfo,
    updateNickname, 
    changePassword, 
    deleteUser,
  }

}, { persist: true })  // Pinia persist 플러그인: 새로고침 시에도 로그인 상태 유지