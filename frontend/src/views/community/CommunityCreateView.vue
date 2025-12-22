<template>
  <div class="create-page">
    <div class="container">
      <RouterLink class="back-link" :to="{ name: 'CommunityView' }">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5"/>
          <path d="M12 19l-7-7 7-7"/>
        </svg>
        목록으로 돌아가기
      </RouterLink>

      <section class="create-card">
        <div class="card-header">
          <h1 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            새 글 작성하기
          </h1>
          <p class="card-description">커뮤니티에 공유하고 싶은 이야기를 작성해주세요</p>
        </div>

        <form class="create-form" @submit.prevent="onSubmit">
          <div class="form-group">
            <label class="form-label" for="title">제목</label>
            <input 
              id="title"
              v-model.trim="title" 
              class="form-input" 
              placeholder="제목을 입력하세요" 
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="content">내용</label>
            <textarea 
              id="content"
              v-model.trim="content" 
              class="form-textarea" 
              placeholder="내용을 입력하세요"
            ></textarea>
          </div>

          <div class="form-actions">
            <button class="btn btn-primary" type="submit" :disabled="!canSubmit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 2L11 13"/>
                <path d="M22 2l-7 20-4-9-9-4 20-7z"/>
              </svg>
              게시하기
            </button>
            <RouterLink class="btn btn-secondary" :to="{ name: 'CommunityView' }">
              취소
            </RouterLink>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import { useAccountStore } from '@/stores/accounts'

const store = useCommunityStore()
const accountStore = useAccountStore()
const router = useRouter()

const title = ref('')
const content = ref('')

const canSubmit = computed(() => title.value && content.value)

const onSubmit = () => {
  if (!accountStore.isLogin) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'LogInView' })
    return
  }

  store.createArticle({ title: title.value, content: content.value })
    .then(() => {
      title.value = ''
      content.value = ''
      router.push({ name: 'CommunityView' })
    })
    .catch((err) => {
      console.log(err)
      alert(`저장 실패: ${JSON.stringify(err.response?.data)}`)
    })
}
</script>

<style scoped>
.create-page {
  min-height: calc(100vh - 72px);
  padding: 48px 24px;
  background: linear-gradient(180deg, #faf5ff 0%, #f5f3ff 50%, #fafafa 100%);
}

.container {
  max-width: 720px;
  margin: 0 auto;
}

/* Back Link */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #71717a;
  text-decoration: none;
  margin-bottom: 24px;
  transition: color 0.2s;
}

.back-link:hover {
  color: #9333ea;
}

.back-link svg {
  width: 18px;
  height: 18px;
}

/* Create Card */
.create-card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.card-header {
  padding: 32px 32px 24px;
  border-bottom: 1px solid #f4f4f5;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  margin: 0 0 8px;
}

.card-title svg {
  width: 28px;
  height: 28px;
  color: #9333ea;
}

.card-description {
  font-size: 0.9375rem;
  color: #71717a;
  margin: 0;
}

/* Form */
.create-form {
  padding: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #52525b;
  margin-bottom: 8px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 14px 18px;
  font-size: 1rem;
  background: #fafafa;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  outline: none;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #9333ea;
  background: white;
  box-shadow: 0 0 0 4px rgba(147, 51, 234, 0.1);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #a1a1aa;
}

.form-textarea {
  min-height: 240px;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  font-size: 0.9375rem;
  font-weight: 600;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn svg {
  width: 18px;
  height: 18px;
}

.btn-primary {
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  color: white;
  border: none;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(147, 51, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #52525b;
  border: 2px solid #e4e4e7;
}

.btn-secondary:hover {
  border-color: #9333ea;
  color: #9333ea;
}

/* Responsive */
@media (max-width: 768px) {
  .create-page {
    padding: 32px 16px;
  }

  .card-header,
  .create-form {
    padding-left: 24px;
    padding-right: 24px;
  }

  .card-title {
    font-size: 1.25rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
