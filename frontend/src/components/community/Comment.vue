<template>
  <section class="card">
    <h3>댓글 ({{ comments.length }})</h3>

    <ul v-if="comments.length" class="list">
      <li v-for="c in comments" :key="c.id" class="item">
        <!-- 수정 모드 -->
        <template v-if="editingId === c.id">
          <div class="edit-row">
            <input v-model.trim="editContent" class="input" placeholder="댓글 수정" />
            <button class="btn" type="button" @click="onSaveEdit(c.id)" :disabled="!editContent">저장</button>
            <button class="btn ghost" type="button" @click="cancelEdit">취소</button>
          </div>
        </template>

        <!-- 보기 모드 -->
        <template v-else>
          <div class="left">
            <div class="meta">
              <strong>{{ c.author_nickname ?? '익명' }}</strong>
              <span class="date">{{ formatDate(c.created_at) }}</span>
            </div>
            <div class="content">{{ c.content }}</div>
            <div class="like-row">
              <button class="like-btn" type="button" @click="onToggleCommentLike(c.id)">
                {{ c.is_liked ? '❤️' : '🤍' }}
                좋아요 {{ c.likes_count ?? 0 }}
              </button>
            </div>
          </div>

          <div v-if="isAuthor(c)" class="actions">
            <button class="edit" type="button" @click="startEdit(c)">수정</button>
            <button class="del" type="button" @click="onDelete(c.id)">삭제</button>
          </div>
        </template>
      </li>
    </ul>

    <p v-else class="empty">댓글이 없습니다.</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const props = defineProps({
  comments: { type: Array, default: () => [] },
})

const emit = defineEmits(['delete', 'update', 'toggle-like'])

const accountStore = useAccountStore()

// 수정 모드 상태
const editingId = ref(null)
const editContent = ref('')

// 현재 로그인 유저가 댓글 작성자인지 확인
const isAuthor = (comment) => {
  if (!accountStore.nickname) return false
  return accountStore.nickname === comment.author_nickname
}

// 수정 시작
const startEdit = (comment) => {
  editingId.value = comment.id
  editContent.value = comment.content
}

// 수정 취소
const cancelEdit = () => {
  editingId.value = null
  editContent.value = ''
}

// 수정 저장
const onSaveEdit = (id) => {
  emit('update', { id, content: editContent.value })
  cancelEdit()
}

// 삭제
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

// ✅ 댓글 좋아요 토글 요청 (로그인 체크 없음)
const onToggleCommentLike = (commentId) => {
  emit('toggle-like', commentId)
}

</script>

<style scoped>
.card { border: 1px solid #eee; border-radius: 12px; padding: 16px; margin-top: 12px; }
.list { padding-left: 16px; margin: 10px 0 0; }
.item { display: flex; justify-content: space-between; gap: 10px; padding: 10px 0; border-bottom: 1px solid #f2f2f2; }
.item:last-child { border-bottom: 0; }
.left { flex: 1; }
.meta { display: flex; gap: 10px; color: #555; font-size: 13px; }
.date { opacity: .7; }
.content { margin-top: 4px; white-space: pre-wrap; }

/* 버튼 영역 */
.actions { display: flex; gap: 6px; align-items: flex-start; }
.edit { border: 1px solid #ddd; background: #fff; border-radius: 10px; padding: 6px 10px; cursor: pointer; font-size: 12px; }
.edit:hover { background: #f5f5f5; }
.del { border: 1px solid #ddd; background: #fff; border-radius: 10px; padding: 6px 10px; cursor: pointer; font-size: 12px; }
.del:hover { background: #fff5f7; border-color: #f2b8c6; }

/* 수정 폼 */
.edit-row { display: flex; gap: 8px; width: 100%; align-items: center; }
.input { flex: 1; padding: 8px 10px; border: 1px solid #ddd; border-radius: 10px; }
.btn { padding: 8px 10px; border: 1px solid #333; border-radius: 10px; background: #fff; cursor: pointer; font-size: 12px; }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.ghost { border-color: #ddd; }

.empty { color: #777; margin: 10px 0 0; }

.like-row {
  margin-top: 14px;
  display: flex;
  justify-content: flex-start;
}

.like-btn {
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 14px;
}

.like-btn:hover {
  background: #f7f7f7;
}
</style>
