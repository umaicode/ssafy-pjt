<template>
  <form class="card" @submit.prevent="submit">
    <h3>댓글 작성</h3>

    <div class="row">
      <input v-model.trim="content" class="input" placeholder="댓글을 입력하세요" />
      <button class="btn" type="submit" :disabled="!content">등록</button>
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
.card { border: 1px solid #eee; border-radius: 12px; padding: 16px; margin-top: 12px; }
.row { display: flex; gap: 10px; align-items: center; }
.input { flex: 1; padding: 10px 12px; border: 1px solid #ddd; border-radius: 10px; }
.btn { padding: 10px 12px; border: 1px solid #333; border-radius: 10px; background: #fff; cursor: pointer; }
.btn:disabled { opacity: .5; cursor: not-allowed; }
</style>
