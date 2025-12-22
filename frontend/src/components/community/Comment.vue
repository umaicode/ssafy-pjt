<template>
  <section class="card">
    <h3>댓글 ({{ comments.length }})</h3>

    <ul v-if="comments.length" class="list">
      <li v-for="c in comments" :key="c.id" class="item">
        <div class="left">
          <div class="meta">
            <strong>{{ c.author_nickname ?? '익명' }}</strong>
            <span class="date">{{ formatDate(c.created_at) }}</span>
          </div>
          <div class="content">{{ c.content }}</div>
        </div>

        <!-- ✅ 댓글 삭제 -->
        <button class="del" type="button" @click="onDelete(c.id)">삭제</button>
      </li>
    </ul>

    <p v-else class="empty">댓글이 없습니다.</p>
  </section>
</template>

<script setup>
const props = defineProps({
  comments: { type: Array, default: () => [] },
})

const emit = defineEmits(['delete'])

const onDelete = (id) => {
  const ok = window.confirm('댓글을 삭제할까요?')
  if (!ok) return
  emit('delete', id)
}

const formatDate = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}.${m}.${day}`
}
</script>

<style scoped>
.card { border: 1px solid #eee; border-radius: 12px; padding: 16px; margin-top: 12px; }
.list { padding-left: 16px; margin: 10px 0 0; }
.item { display: flex; justify-content: space-between; gap: 10px; padding: 10px 0; border-bottom: 1px solid #f2f2f2; }
.item:last-child { border-bottom: 0; }
.meta { display: flex; gap: 10px; color: #555; font-size: 13px; }
.date { opacity: .7; }
.content { margin-top: 4px; white-space: pre-wrap; }
.del { border: 1px solid #ddd; background: #fff; border-radius: 10px; padding: 8px 10px; cursor: pointer; }
.empty { color: #777; margin: 10px 0 0; }
</style>
