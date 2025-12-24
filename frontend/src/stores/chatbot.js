import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useChatbotStore = defineStore('chatbot', () => {
  const API_URL = 'http://127.0.0.1:8000'
  
  const isOpen = ref(false)
  const messages = ref([])
  const isLoading = ref(false)
  const suggestions = ref([])
  
  // 채팅창 토글
  const toggleChat = () => {
    isOpen.value = !isOpen.value
  }
  
  // 채팅창 열기
  const openChat = () => {
    isOpen.value = true
  }
  
  // 채팅창 닫기
  const closeChat = () => {
    isOpen.value = false
  }
  
  // 추천 질문 가져오기
  const fetchSuggestions = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/chatbot/suggestions/`)
      suggestions.value = response.data.suggestions
    } catch (error) {
      console.error('추천 질문 로드 실패:', error)
    }
  }
  
  // 메시지 전송
  const sendMessage = async (message, location = null) => {
    if (!message.trim() || isLoading.value) return
    
    // 사용자 메시지 추가
    messages.value.push({
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    })
    
    isLoading.value = true
    
    try {
      const requestData = { message: message }
      
      // 위치 정보가 있으면 추가
      if (location) {
        requestData.location = location
      }
      
      const response = await axios.post(`${API_URL}/api/chatbot/`, requestData)
      
      // AI 응답 추가
      messages.value.push({
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.message,
        data: response.data,
        intent: response.data.intent,
        timestamp: new Date()
      })
      
    } catch (error) {
      console.error('챗봇 오류:', error)
      messages.value.push({
        id: Date.now() + 1,
        type: 'bot',
        content: '죄송합니다. 일시적인 오류가 발생했어요. 다시 시도해 주세요. 🙏',
        error: true,
        timestamp: new Date()
      })
    } finally {
      isLoading.value = false
    }
  }
  
  // 채팅 초기화
  const clearMessages = () => {
    messages.value = []
  }
  
  // 메시지 직접 추가
  const addMessage = (msg) => {
    messages.value.push({
      id: Date.now() + Math.random(),
      type: msg.type,
      content: msg.content,
      data: msg.data || null,
      timestamp: new Date()
    })
  }
  
  // 위치 정보로 은행 검색
  const searchBankWithLocation = async (bankName, lat, lng) => {
    // 위치 확인 메시지 삭제 (마지막 메시지)
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].content.includes('위치를 확인')) {
      messages.value.pop()
    }
    
    isLoading.value = true
    
    try {
      const response = await axios.post(`${API_URL}/api/chatbot/bank-search/`, {
        bank_name: bankName,
        lat: lat,
        lng: lng
      })
      
      messages.value.push({
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.message,
        data: response.data,
        timestamp: new Date()
      })
      
    } catch (error) {
      console.error('은행 검색 오류:', error)
      messages.value.push({
        id: Date.now() + 1,
        type: 'bot',
        content: '은행 검색 중 오류가 발생했어요. 다시 시도해 주세요. 🙏',
        error: true,
        timestamp: new Date()
      })
    } finally {
      isLoading.value = false
    }
  }
  
  // 초기 인사 메시지
  const initGreeting = () => {
    if (messages.value.length === 0) {
      messages.value.push({
        id: Date.now(),
        type: 'bot',
        content: '안녕하세요! 👋 저는 핑프, F!NK AI 챗봇이에요.\n\n무엇이든 물어보세요!\n• 금융 상품 추천\n• 가까운 은행 찾기\n• 뉴스 검색\n• 투자 조언\n• 여행 예산 상담',
        timestamp: new Date()
      })
    }
  }
  
  return {
    isOpen,
    messages,
    isLoading,
    suggestions,
    toggleChat,
    openChat,
    closeChat,
    fetchSuggestions,
    sendMessage,
    clearMessages,
    addMessage,
    searchBankWithLocation,
    initGreeting
  }
})
