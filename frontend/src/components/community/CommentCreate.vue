<template>
  <form class="comment-create" @submit.prevent="submit">
    <div class="create-header">
      <div class="avatar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
      </div>
      <div class="input-wrapper">
        <input 
          v-model.trim="content" 
          class="comment-input" 
          placeholder="댓글을 입력하세요..." 
        />
      </div>
      <button class="btn-submit" type="submit" :disabled="!content">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="22" y1="2" x2="11" y2="13"/>
          <polygon points="22 2 15 22 11 13 2 9 22 2"/>
        </svg>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['submit'])
const content = ref('')

const submit = () => {
  // ✅ 부모로 댓글 내용 전달
  emit('submit', content.value)
  content.value = ''
}
</script>

<style scoped>
.comment-create {
  background: white;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  margin-top: 12px;
}

.create-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #E1AFD1 0%, #AD88C6 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar svg {
  width: 20px;
  height: 20px;
  color: #7469B6;
}

.input-wrapper {
  flex: 1;
}

.comment-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 0.9375rem;
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  background: #fafafa;
  transition: all 0.2s;
  box-sizing: border-box;
}

.comment-input:focus {
  outline: none;
  border-color: #7469B6;
  background: white;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.1);
}

.comment-input::placeholder {
  color: #a1a1aa;
}

.btn-submit {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-submit svg {
  width: 20px;
  height: 20px;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.4);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
