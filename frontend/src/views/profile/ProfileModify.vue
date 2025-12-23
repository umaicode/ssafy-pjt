<template>
  <div class="modify-section">
    <div class="section-header">
      <div class="header-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 20h9"/>
          <path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
        </svg>
      </div>
      <div class="header-text">
        <h2 class="section-title">정보 수정</h2>
        <p class="section-description">닉네임과 비밀번호를 변경할 수 있어요</p>
      </div>
    </div>

    <!-- Nickname Section -->
    <section class="card">
      <div class="card-header">
        <div class="card-icon nickname-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <div class="card-title-group">
          <h4 class="card-title">닉네임 변경</h4>
          <p class="card-subtitle">다른 사용자에게 표시되는 이름이에요</p>
        </div>
      </div>

      <form class="form" @submit.prevent="onUpdateNickname">
        <div class="input-group">
          <label class="input-label">새 닉네임</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <input 
              v-model.trim="newNickname" 
              class="input" 
              type="text"
              placeholder="변경할 닉네임을 입력하세요" 
            />
          </div>
        </div>
        <button class="btn-primary" type="submit" :disabled="!newNickname">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          저장하기
        </button>
      </form>
    </section>

    <!-- Password Section -->
    <section class="card">
      <div class="card-header">
        <div class="card-icon password-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0110 0v4"/>
          </svg>
        </div>
        <div class="card-title-group">
          <h4 class="card-title">비밀번호 변경</h4>
          <p class="card-subtitle">보안을 위해 주기적으로 변경해주세요</p>
        </div>
      </div>

      <form class="form" @submit.prevent="onChangePassword">
        <div class="input-group">
          <label class="input-label">현재 비밀번호</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
            </svg>
            <input 
              v-model="oldPassword" 
              class="input" 
              type="password" 
              placeholder="현재 비밀번호를 입력하세요" 
            />
          </div>
        </div>

        <div class="input-group">
          <label class="input-label">새 비밀번호</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0110 0v4"/>
            </svg>
            <input 
              v-model="newPassword1" 
              class="input" 
              type="password" 
              placeholder="새 비밀번호를 입력하세요" 
            />
          </div>
        </div>

        <div class="input-group">
          <label class="input-label">새 비밀번호 확인</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 11 12 14 22 4"/>
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
            </svg>
            <input 
              v-model="newPassword2" 
              class="input" 
              type="password" 
              placeholder="새 비밀번호를 다시 입력하세요" 
            />
          </div>
        </div>

        <button class="btn-primary" type="submit" :disabled="!canSubmitPw">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0110 0v4"/>
          </svg>
          비밀번호 변경
        </button>
      </form>

      <div class="hint-box">
        <svg class="hint-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="16" x2="12" y2="12"/>
          <line x1="12" y1="8" x2="12.01" y2="8"/>
        </svg>
        <p class="hint">변경 후 보안을 위해 다시 로그인하게 됩니다.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

const newNickname = ref('')

const oldPassword = ref('')
const newPassword1 = ref('')
const newPassword2 = ref('')

// 비밀번호 입력 완료 여부
const canSubmitPw = computed(() => {
  return oldPassword.value && newPassword1.value && newPassword2.value
})

// 닉네임 변경
const onUpdateNickname = () => {
  accountStore.updateNickname(newNickname.value)
    .then(() => {
      newNickname.value = '' // 입력값 초기화
    })
    .catch(() => {
      // updateNickname 내부에서 alert 처리 중이므로 여기선 생략 가능
    })
}

// 비밀번호 변경
const onChangePassword = () => {
  if (newPassword1.value !== newPassword2.value) {
    alert('새 비밀번호가 서로 일치하지 않습니다.')
    return
  }

  accountStore.changePassword({
    old_password: oldPassword.value,
    new_password1: newPassword1.value,
    new_password2: newPassword2.value,
  })
  .then(() => {
    // changePassword 내부에서 로그아웃 + 이동 처리
  })
  .catch(() => {
    // 에러 메시지도 store에서 처리 중
  })
}
</script>

<style scoped>
.modify-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  margin: 0;
}

.section-description {
  font-size: 0.9375rem;
  color: #71717a;
  margin: 0;
}

/* Card */
.card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f4f4f5;
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon svg {
  width: 22px;
  height: 22px;
}

.nickname-icon {
  background: #f0fdf4;
  color: #16a34a;
}

.password-icon {
  background: #fef3c7;
  color: #d97706;
}

.card-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.card-subtitle {
  font-size: 0.875rem;
  color: #71717a;
  margin: 0;
}

/* Form */
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 400px;
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
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  width: 18px;
  height: 18px;
  color: #a1a1aa;
  pointer-events: none;
}

.input {
  width: 100%;
  padding: 14px 16px 14px 48px;
  font-size: 0.9375rem;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  background: white;
  transition: all 0.2s;
}

.input::placeholder {
  color: #a1a1aa;
}

.input:focus {
  outline: none;
  border-color: #7469B6;
  box-shadow: 0 0 0 4px rgba(116, 105, 182, 0.1);
}

/* Button */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
  width: fit-content;
}

.btn-primary svg {
  width: 18px;
  height: 18px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(116, 105, 182, 0.35);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Hint Box */
.hint-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 20px;
  padding: 14px 16px;
  background: #fffbeb;
  border-radius: 12px;
  border: 1px solid #fde68a;
}

.hint-icon {
  width: 18px;
  height: 18px;
  color: #d97706;
  flex-shrink: 0;
  margin-top: 1px;
}

.hint {
  font-size: 0.875rem;
  color: #92400e;
  margin: 0;
  line-height: 1.5;
}

/* Responsive */
@media (max-width: 640px) {
  .card {
    padding: 20px;
  }
  
  .form {
    max-width: 100%;
  }
  
  .btn-primary {
    width: 100%;
  }
}
</style>
