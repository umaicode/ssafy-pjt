<template>
  <div class="auth-page">
    <div class="auth-container">
      <!-- Left Side - Branding -->
      <div class="auth-branding">
        <div class="branding-content">
          <div class="branding-logo">F!NK</div>
          <h1 class="branding-title">
            스마트한 금융,<br>
            <span class="text-gradient">지금 시작하세요</span>
          </h1>
          <p class="branding-description">
            회원가입 후 AI 맞춤 추천을 받고<br>
            나에게 딱 맞는 금융상품을 찾아보세요.
          </p>
          
          <div class="branding-features">
            <div class="feature-item">
              <div class="feature-check">✓</div>
              <span>무료 가입, 무료 이용</span>
            </div>
            <div class="feature-item">
              <div class="feature-check">✓</div>
              <span>1분 만에 가입 완료</span>
            </div>
            <div class="feature-item">
              <div class="feature-check">✓</div>
              <span>개인정보 안전 보호</span>
            </div>
          </div>
        </div>
        
        <div class="branding-decoration">
          <div class="decoration-orb orb-1"></div>
          <div class="decoration-orb orb-2"></div>
        </div>
      </div>

      <!-- Right Side - Form -->
      <div class="auth-form-section">
        <div class="auth-form-container">
          <div class="auth-header">
            <h2 class="auth-title">회원가입</h2>
            <p class="auth-subtitle">F!NK 멤버가 되어 모든 혜택을 누리세요</p>
          </div>

          <form @submit.prevent="signUp" class="auth-form">
            <div class="input-group">
              <label class="input-label" for="username">아이디</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                <input 
                  type="text" 
                  id="username" 
                  v-model.trim="username"
                  class="input input-with-icon"
                  placeholder="아이디를 입력하세요"
                  required
                />
              </div>
            </div>

            <div class="input-group">
              <label class="input-label" for="nickname">닉네임</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
                <input 
                  type="text" 
                  id="nickname" 
                  v-model.trim="nickname"
                  class="input input-with-icon"
                  placeholder="사용할 닉네임을 입력하세요"
                  required
                />
              </div>
            </div>
            
            <div class="input-group">
              <label class="input-label" for="password1">비밀번호</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>

                <input
                  :type="password1Visible ? 'text' : 'password'"
                  id="password1"
                  v-model.trim="password1"
                  class="input input-with-icon input-with-toggle"
                  placeholder="비밀번호를 입력하세요"
                  required
                />

                <!-- 👁️ -->
                <button
                  type="button"
                  class="password-toggle"
                  @click="password1Visible = !password1Visible"
                  aria-label="비밀번호 보기"
                >
                  <svg v-if="!password1Visible" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.94 10.94 0 0112 19c-7 0-11-7-11-7"/>
                    <path d="M1 1l22 22"/>
                  </svg>
                </button>
              </div>
            </div>

            <div class="input-group">
              <label class="input-label" for="password2">비밀번호 확인</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>

                <input
                  :type="password2Visible ? 'text' : 'password'"
                  id="password2"
                  v-model.trim="password2"
                  class="input input-with-icon input-with-toggle"
                  placeholder="비밀번호를 다시 입력하세요"
                  required
                />

                <!-- 👁️ -->
                <button
                  type="button"
                  class="password-toggle"
                  @click="password2Visible = !password2Visible"
                  aria-label="비밀번호 보기"
                >
                  <svg v-if="!password2Visible" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.94 10.94 0 0112 19c-7 0-11-7-11-7"/>
                    <path d="M1 1l22 22"/>
                  </svg>
                </button>
              </div>
            </div>


            <button type="submit" class="btn btn-primary btn-lg btn-block">
              가입하기
            </button>
          </form>

          <div class="auth-divider">
            <span>또는</span>
          </div>

          <div class="auth-footer">
            <p>이미 계정이 있으신가요?</p>
            <RouterLink :to="{ name: 'LogInView' }" class="auth-link">
              로그인 하기 <span class="arrow">→</span>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const username = ref('')
const nickname = ref('')
const password1 = ref('')
const password2 = ref('')

const password1Visible = ref(false)
const password2Visible = ref(false)

const accountStore = useAccountStore()

const signUp = function () {
  const payload = {
    username: username.value,
    nickname: nickname.value,
    password1: password1.value,
    password2: password2.value,
  }
  accountStore.signUp(payload)
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 72px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
}

.auth-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1100px;
  width: 100%;
  background: white;
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
}

/* Branding Section */
.auth-branding {
  position: relative;
  background: linear-gradient(135deg, #1d1d1f 0%, #2D2660 50%, #1d1d1f 100%);
  padding: 60px 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.branding-content {
  position: relative;
  z-index: 1;
}

.branding-logo {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 35%, #AD88C6 70%, #7469B6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 32px;
}

.branding-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: white;
  line-height: 1.2;
  margin-bottom: 20px;
}

.text-gradient {
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 35%, #AD88C6 70%, #7469B6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.branding-description {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 40px;
}

.branding-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9375rem;
}

.feature-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(116, 105, 182, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: #E1AFD1;
}

.branding-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.decoration-orb {
  position: absolute;
  border-radius: 50%;
}

.orb-1 {
  top: -100px;
  right: -100px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(116, 105, 182, 0.4) 0%, transparent 70%);
}

.orb-2 {
  bottom: -50px;
  left: -50px;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(225, 175, 209, 0.3) 0%, transparent 70%);
}

/* Form Section */
.auth-form-section {
  padding: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-form-container {
  width: 100%;
  max-width: 380px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 8px;
}

.auth-subtitle {
  color: #71717a;
  font-size: 0.9375rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #3f3f46;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #a1a1aa;
  pointer-events: none;
}

input.input-with-icon {
  padding-left: 48px;
}

.input {
  width: 100%;
  padding: 14px 18px;
  font-size: 1rem;
  background: #fafafa;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  transition: all 0.2s ease;
  outline: none;
}

.input:focus {
  border-color: #7469B6;
  background: white;
  box-shadow: 0 0 0 4px rgba(116, 105, 182, 0.1);
}

.input::placeholder {
  color: #a1a1aa;
}

.auth-divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 28px 0;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e4e4e7;
}

.auth-divider span {
  font-size: 0.8125rem;
  color: #a1a1aa;
}

.auth-footer {
  text-align: center;
}

.auth-footer p {
  color: #71717a;
  font-size: 0.9375rem;
  margin-bottom: 8px;
}

.auth-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #7469B6;
  text-decoration: none;
  transition: gap 0.2s ease;
}

.auth-link:hover {
  gap: 10px;
}

/* Responsive */
@media (max-width: 900px) {
  .auth-container {
    grid-template-columns: 1fr;
    max-width: 480px;
  }

  .auth-branding {
    display: none;
  }

  .auth-form-section {
    padding: 48px 32px;
  }
}

@media (max-width: 480px) {
  .auth-page {
    padding: 24px 16px;
  }

  .auth-form-section {
    padding: 40px 24px;
  }
}

/* Dark Mode Styles */
[data-theme="dark"] .auth-page {
  background: #0a0a0a;
}

[data-theme="dark"] .auth-container {
  background: #18181b;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .auth-form-section {
  background: #18181b;
}

[data-theme="dark"] .auth-title {
  color: #e4e4e7;
}

[data-theme="dark"] .auth-subtitle {
  color: #a1a1aa;
}

[data-theme="dark"] .input-label {
  color: #a1a1aa;
}

[data-theme="dark"] .input {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .input:focus {
  background: #27272a;
  border-color: #7469B6;
}

[data-theme="dark"] .input::placeholder {
  color: #71717a;
}

[data-theme="dark"] .input-icon {
  color: #71717a;
}

[data-theme="dark"] .auth-divider::before,
[data-theme="dark"] .auth-divider::after {
  background: #3f3f46;
}

[data-theme="dark"] .auth-divider span {
  color: #71717a;
}

[data-theme="dark"] .auth-footer p {
  color: #a1a1aa;
}

[data-theme="dark"] .auth-link {
  color: #E1AFD1;
}
/* 비밀번호 보기 버튼 */
.password-toggle {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #a1a1aa;
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

.password-toggle:hover {
  color: #7469B6;
}

/* 오른쪽 아이콘 공간 확보 */
.input-with-toggle {
  padding-right: 48px;
}

/* 다크모드 */
[data-theme="dark"] .password-toggle {
  color: #71717a;
}

[data-theme="dark"] .password-toggle:hover {
  color: #E1AFD1;
}

</style>