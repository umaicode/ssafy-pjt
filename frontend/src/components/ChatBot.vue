<template>
  <div class="chatbot-wrapper">
    <!-- 플로팅 버튼 -->
    <Transition name="bounce">
      <button 
        v-if="!chatbotStore.isOpen" 
        class="chatbot-fab"
        @click="openChatbot"
        title="AI 챗봇"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
          <circle cx="9" cy="10" r="1" fill="currentColor"/>
          <circle cx="12" cy="10" r="1" fill="currentColor"/>
          <circle cx="15" cy="10" r="1" fill="currentColor"/>
        </svg>
        <span class="fab-badge" v-if="unreadCount > 0">{{ unreadCount }}</span>
      </button>
    </Transition>

    <!-- 채팅 창 -->
    <Transition name="slide-up">
      <div v-if="chatbotStore.isOpen" class="chatbot-window">
        <!-- 헤더 -->
        <div class="chatbot-header">
          <div class="header-info">
            <div class="bot-avatar">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="10" rx="2"/>
                <circle cx="12" cy="5" r="3"/>
                <path d="M8 15h.01M16 15h.01"/>
              </svg>
            </div>
            <div class="bot-info">
              <span class="bot-name">핑프 AI</span>
              <span class="bot-status">
                <span class="status-dot"></span>
                온라인
              </span>
            </div>
          </div>
          <div class="header-actions">
            <button class="header-btn" @click="chatbotStore.clearMessages" title="대화 초기화">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
              </svg>
            </button>
            <button class="header-btn close-btn" @click="chatbotStore.closeChat" title="닫기">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- 메시지 영역 -->
        <div class="chatbot-messages" ref="messagesContainer">
          <TransitionGroup name="message">
            <div 
              v-for="msg in chatbotStore.messages" 
              :key="msg.id"
              :class="['message', msg.type === 'user' ? 'message-user' : 'message-bot']"
            >
              <div class="message-content">
                <div class="message-bubble" v-html="formatMessage(msg.content)"></div>
                
                <!-- 추가 데이터 표시 (상품, 지도 링크 등) -->
                <div v-if="msg.data" class="message-extras">
                  <!-- 금융 상품 카드 -->
                  <template v-if="msg.data.type === 'product_search' && msg.data.products">
                    <div class="product-cards">
                      <div v-if="msg.data.products.best_saving" class="product-card">
                        <span class="product-type">적금 추천</span>
                        <span class="product-bank">{{ msg.data.products.best_saving.bank }}</span>
                        <span class="product-name">{{ msg.data.products.best_saving.name }}</span>
                        <span class="product-rate">최고 {{ msg.data.products.best_saving.max_rate }}%</span>
                      </div>
                      <div v-if="msg.data.products.best_deposit" class="product-card">
                        <span class="product-type">예금 추천</span>
                        <span class="product-bank">{{ msg.data.products.best_deposit.bank }}</span>
                        <span class="product-name">{{ msg.data.products.best_deposit.name }}</span>
                        <span class="product-rate">최고 {{ msg.data.products.best_deposit.max_rate }}%</span>
                      </div>
                    </div>
                    <router-link to="/products" class="action-btn" @click="chatbotStore.closeChat">
                      상품 더보기 →
                    </router-link>
                  </template>

                  <!-- 은행 위치 액션 -->
                  <template v-if="msg.data.type === 'bank_location'">
                    <!-- 지도 표시 -->
                    <div v-if="msg.data.show_map && msg.data.bank_info" class="bank-map-container">
                      <div class="bank-info-card">
                        <div class="bank-icon">🏦</div>
                        <div class="bank-details">
                          <span class="bank-name-label">{{ msg.data.bank_info.place_name }}</span>
                          <span class="bank-address">{{ msg.data.bank_info.road_address || msg.data.bank_info.address }}</span>
                          <span v-if="msg.data.bank_info.phone" class="bank-phone">📞 {{ msg.data.bank_info.phone }}</span>
                        </div>
                      </div>
                      <a 
                        :href="msg.data.bank_info.place_url || `https://map.kakao.com/link/map/${msg.data.bank_info.place_name},${msg.data.bank_info.lat},${msg.data.bank_info.lng}`" 
                        target="_blank" 
                        class="action-btn map-btn"
                      >
                        📍 카카오맵에서 보기
                      </a>
                    </div>
                    <!-- 위치 요청 버튼 -->
                    <button 
                      v-else-if="msg.data.need_location" 
                      class="action-btn location-btn"
                      @click="requestLocation(msg.data.bank_name)"
                    >
                      📍 내 위치로 가까운 지점 찾기
                    </button>
                    <!-- 기존 지도로 이동 링크 -->
                    <router-link 
                      v-else
                      :to="{ name: 'KakaoMapView', query: { bank: msg.data.bank_name } }" 
                      class="action-btn map-btn"
                      @click="chatbotStore.closeChat"
                    >
                      🗺️ 지도에서 찾기
                    </router-link>
                  </template>

                  <!-- 뉴스 카드 -->
                  <template v-if="(msg.data.type === 'news_search' || msg.data.type === 'investment_advice') && msg.data.news?.length">
                    <div class="news-cards">
                      <a 
                        v-for="(news, idx) in msg.data.news.slice(0, 3)" 
                        :key="idx"
                        :href="news.link"
                        target="_blank"
                        class="news-card"
                      >
                        <span class="news-title">{{ truncateText(news.title, 50) }}</span>
                        <span class="news-desc">{{ truncateText(news.description, 60) }}</span>
                      </a>
                    </div>
                  </template>

                  <!-- 투자 조언 유튜브 -->
                  <template v-if="msg.data.type === 'investment_advice' && msg.data.youtube_videos?.length">
                    <div class="youtube-cards">
                      <a 
                        v-for="video in msg.data.youtube_videos.slice(0, 2)" 
                        :key="video.video_id"
                        :href="video.url"
                        target="_blank"
                        class="youtube-card"
                      >
                        <img :src="video.thumbnail" :alt="video.title" class="youtube-thumb"/>
                        <span class="youtube-title">{{ truncateText(video.title, 40) }}</span>
                      </a>
                    </div>
                  </template>

                  <!-- 여행 유튜브 영상 -->
                  <template v-if="msg.data.type === 'travel_budget' && msg.data.youtube_videos?.length">
                    <div class="youtube-cards">
                      <a 
                        v-for="video in msg.data.youtube_videos.slice(0, 3)" 
                        :key="video.video_id"
                        :href="video.url"
                        target="_blank"
                        class="youtube-card"
                      >
                        <img :src="video.thumbnail" :alt="video.title" class="youtube-thumb"/>
                        <span class="youtube-title">{{ truncateText(video.title, 40) }}</span>
                      </a>
                    </div>
                    <router-link to="/analysis" class="action-btn" @click="chatbotStore.closeChat">
                      ✨ AI 분석으로 여행 계획 세우기
                    </router-link>
                  </template>
                </div>

                <span class="message-time">{{ formatTime(msg.timestamp) }}</span>
              </div>
            </div>
          </TransitionGroup>

          <!-- 로딩 표시 -->
          <div v-if="chatbotStore.isLoading" class="message message-bot">
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- 추천 질문 -->
        <div v-if="chatbotStore.messages.length <= 1 && chatbotStore.suggestions.length > 0" class="suggestions-area">
          <div class="suggestions-scroll">
            <button 
              v-for="(cat, idx) in chatbotStore.suggestions" 
              :key="idx"
              class="suggestion-chip"
              @click="sendSuggestion(cat.questions[0])"
            >
              {{ cat.questions[0] }}
            </button>
          </div>
        </div>

        <!-- 입력 영역 -->
        <div class="chatbot-input">
          <input 
            v-model="inputMessage"
            type="text"
            placeholder="메시지를 입력하세요..."
            @keyup.enter="sendMessage"
            :disabled="chatbotStore.isLoading"
          />
          <button 
            class="send-btn" 
            @click="sendMessage"
            :disabled="!inputMessage.trim() || chatbotStore.isLoading"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { useChatbotStore } from '@/stores/chatbot'

const chatbotStore = useChatbotStore()
const inputMessage = ref('')
const messagesContainer = ref(null)
const unreadCount = ref(0)

// 챗봇 열기
const openChatbot = () => {
  chatbotStore.openChat()
  chatbotStore.initGreeting()
  chatbotStore.fetchSuggestions()
  unreadCount.value = 0
}

// 메시지 전송
const sendMessage = () => {
  if (!inputMessage.value.trim()) return
  chatbotStore.sendMessage(inputMessage.value)
  inputMessage.value = ''
}

// 추천 질문 전송
const sendSuggestion = (question) => {
  chatbotStore.sendMessage(question)
}

// 위치 요청 함수
const requestLocation = (bankName) => {
  if (!navigator.geolocation) {
    chatbotStore.addMessage({
      type: 'bot',
      content: '이 브라우저는 위치 서비스를 지원하지 않습니다. 😢',
    })
    return
  }

  chatbotStore.addMessage({
    type: 'bot',
    content: '📍 위치를 확인하고 있어요...',
  })

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords
      // 위치 정보와 함께 은행 검색 요청
      await chatbotStore.searchBankWithLocation(bankName, latitude, longitude)
    },
    (error) => {
      let errorMsg = '위치 정보를 가져올 수 없어요. 😢'
      if (error.code === error.PERMISSION_DENIED) {
        errorMsg = '위치 권한이 거부되었어요. 브라우저 설정에서 위치 권한을 허용해 주세요. 🔐'
      }
      chatbotStore.addMessage({
        type: 'bot',
        content: errorMsg,
      })
    },
    { enableHighAccuracy: true, timeout: 10000 }
  )
}

// 메시지 포맷팅 (줄바꿈 처리)
const formatMessage = (content) => {
  return content?.replace(/\n/g, '<br>') || ''
}

// 시간 포맷팅
const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
}

// 텍스트 자르기
const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

// 메시지 추가 시 스크롤
watch(() => chatbotStore.messages.length, () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
})

onMounted(() => {
  chatbotStore.fetchSuggestions()
})
</script>

<style scoped>
.chatbot-wrapper {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
}

/* 플로팅 버튼 */
.chatbot-fab {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(116, 105, 182, 0.4);
  transition: all 0.3s ease;
  position: relative;
}

.chatbot-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 30px rgba(116, 105, 182, 0.5);
}

.chatbot-fab svg {
  width: 28px;
  height: 28px;
  color: white;
}

.fab-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: white;
  font-size: 12px;
  font-weight: 600;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 채팅 창 */
.chatbot-window {
  width: 380px;
  height: 560px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 50px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 헤더 */
.chatbot-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bot-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bot-avatar svg {
  width: 24px;
  height: 24px;
  color: white;
}

.bot-info {
  display: flex;
  flex-direction: column;
}

.bot-name {
  font-size: 16px;
  font-weight: 700;
  color: white;
}

.bot-status {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #4ade80;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.header-actions {
  display: flex;
  gap: 8px;
}

.header-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.header-btn svg {
  width: 18px;
  height: 18px;
  color: white;
}

/* 메시지 영역 */
.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #f8f9fa;
}

.message {
  display: flex;
  max-width: 85%;
}

.message-user {
  align-self: flex-end;
}

.message-bot {
  align-self: flex-start;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
  word-break: break-word;
}

.message-user .message-bubble {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message-bot .message-bubble {
  background: white;
  color: #1f2937;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-time {
  font-size: 11px;
  color: #9ca3af;
  padding: 0 4px;
}

.message-user .message-time {
  text-align: right;
}

/* 추가 데이터 */
.message-extras {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-cards {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 12px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-type {
  font-size: 11px;
  color: #7469B6;
  font-weight: 600;
}

.product-bank {
  font-size: 12px;
  color: #6b7280;
}

.product-name {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.product-rate {
  font-size: 14px;
  font-weight: 700;
  color: #7469B6;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  background: #7469B6;
  color: white;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #5a4f9e;
}

.map-btn {
  background: #10b981;
}

.map-btn:hover {
  background: #059669;
}

/* 은행 정보 카드 */
.bank-map-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bank-info-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  border-radius: 12px;
}

.bank-icon {
  font-size: 24px;
}

.bank-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bank-name-label {
  font-size: 14px;
  font-weight: 600;
  color: #065f46;
}

.bank-address {
  font-size: 12px;
  color: #047857;
}

.bank-phone {
  font-size: 12px;
  color: #059669;
}

.location-btn {
  background: #3b82f6;
}

.location-btn:hover {
  background: #2563eb;
}

/* 뉴스 카드 */
.news-cards {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.news-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px 12px;
  background: white;
  border-radius: 10px;
  border-left: 3px solid #7469B6;
  text-decoration: none;
  transition: all 0.2s;
}

.news-card:hover {
  background: #f9fafb;
  transform: translateX(4px);
}

.news-title {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
}

.news-desc {
  font-size: 11px;
  color: #6b7280;
  line-height: 1.3;
}

/* 유튜브 카드 */
.youtube-cards {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.youtube-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s;
}

.youtube-card:hover {
  background: #f3f4f6;
}

.youtube-thumb {
  width: 60px;
  height: 45px;
  border-radius: 6px;
  object-fit: cover;
}

.youtube-title {
  font-size: 12px;
  color: #1f2937;
  line-height: 1.3;
}

/* 타이핑 인디케이터 */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: white;
  border-radius: 18px;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #9ca3af;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: 0s; }
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

/* 추천 질문 */
.suggestions-area {
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #e5e7eb;
}

.suggestions-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.suggestions-scroll::-webkit-scrollbar {
  height: 4px;
}

.suggestions-scroll::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

.suggestion-chip {
  flex-shrink: 0;
  padding: 8px 14px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  font-size: 12px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.suggestion-chip:hover {
  background: #7469B6;
  border-color: #7469B6;
  color: white;
}

/* 입력 영역 */
.chatbot-input {
  padding: 16px;
  background: white;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 12px;
}

.chatbot-input input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.chatbot-input input:focus {
  border-color: #7469B6;
}

.chatbot-input input::placeholder {
  color: #9ca3af;
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn svg {
  width: 20px;
  height: 20px;
  color: white;
}

/* 애니메이션 */
.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.bounce-leave-active {
  animation: bounce-in 0.3s reverse;
}

@keyframes bounce-in {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.slide-up-enter-active {
  animation: slide-up 0.3s ease-out;
}

.slide-up-leave-active {
  animation: slide-up 0.2s ease-in reverse;
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message-enter-active {
  animation: message-in 0.3s ease-out;
}

@keyframes message-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 */
@media (max-width: 480px) {
  .chatbot-wrapper {
    bottom: 16px;
    right: 16px;
  }

  .chatbot-window {
    width: calc(100vw - 32px);
    height: calc(100vh - 100px);
    max-height: 600px;
  }
}

/* 다크 모드 */
[data-theme="dark"] .chatbot-window {
  background: #1f1f23;
}

[data-theme="dark"] .chatbot-messages {
  background: #121214;
}

[data-theme="dark"] .message-bot .message-bubble {
  background: #27272a;
  color: #e4e4e7;
}

[data-theme="dark"] .product-card {
  background: linear-gradient(135deg, #27272a 0%, #1f1f23 100%);
}

[data-theme="dark"] .product-name {
  color: #e4e4e7;
}

[data-theme="dark"] .suggestions-area {
  background: #1f1f23;
  border-color: #3f3f46;
}

[data-theme="dark"] .suggestion-chip {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .chatbot-input {
  background: #1f1f23;
  border-color: #3f3f46;
}

[data-theme="dark"] .chatbot-input input {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .youtube-card {
  background: #27272a;
}

[data-theme="dark"] .youtube-card:hover {
  background: #3f3f46;
}

[data-theme="dark"] .youtube-title {
  color: #e4e4e7;
}

[data-theme="dark"] .typing-indicator {
  background: #27272a;
}

[data-theme="dark"] .news-card {
  background: #27272a;
  border-left-color: #AD88C6;
}

[data-theme="dark"] .news-card:hover {
  background: #3f3f46;
}

[data-theme="dark"] .news-title {
  color: #e4e4e7;
}

[data-theme="dark"] .news-desc {
  color: #a1a1aa;
}

[data-theme="dark"] .bank-info-card {
  background: linear-gradient(135deg, #1c3829 0%, #14532d 100%);
}

[data-theme="dark"] .bank-name-label {
  color: #86efac;
}

[data-theme="dark"] .bank-address {
  color: #4ade80;
}

[data-theme="dark"] .bank-phone {
  color: #34d399;
}
</style>
