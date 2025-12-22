<template>
  <section class="card">
    <h2 class="h2">게시글 작성</h2>

    <form class="form" @submit.prevent="onSubmit">
      <input v-model.trim="title" class="input" placeholder="제목" />
      <textarea v-model.trim="content" class="textarea" placeholder="내용"></textarea>

      <div class="actions">
        <button class="btn" type="submit" :disabled="!canSubmit">
          저장
        </button>
        <RouterLink class="btn ghost" :to="{ name: 'CommunityView' }">취소</RouterLink>
      </div>
    </form>
  </section>
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
.card { border: 1px solid #eee; border-radius: 12px; padding: 16px; }
.h2 { margin: 0 0 12px; }
.form { display: grid; gap: 10px; max-width: 640px; }
.input, .textarea { padding: 10px 12px; border: 1px solid #ddd; border-radius: 10px; }
.textarea { min-height: 180px; resize: vertical; }
.actions { display: flex; gap: 10px; align-items: center; }
.btn { padding: 10px 12px; border: 1px solid #333; border-radius: 10px; background: #fff; cursor: pointer; text-decoration: none; color: #111; }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.ghost { border-color: #ddd; }
</style>
