<template>
  <section class="comments-section">
    <div class="comments-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
          </svg>
        </div>
        <h3>댓글 <span class="count">{{ comments.length }}</span></h3>
      </div>
      <div class="sort-buttons">
        <button 
          class="sort-btn" 
          :class="{ active: sortType === 'latest' }" 
          type="button" 
          @click="changeSortType('latest')"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <polyline points="19 12 12 19 5 12"/>
          </svg>
          최신순
        </button>
        <button 
          class="sort-btn" 
          :class="{ active: sortType === 'likes' }" 
          type="button" 
          @click="changeSortType('likes')"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
          </svg>
          좋아요순
        </button>
      </div>
    </div>

    <ul v-if="comments.length" class="comments-list">
      <li v-for="c in sortedComments" :key="c.id" class="comment-item">
        <!-- 수정 모드 -->
        <template v-if="editingId === c.id">
          <div class="edit-mode">
            <input 
              v-model.trim="editContent" 
              class="edit-input" 
              placeholder="댓글 수정" 
            />
            <div class="edit-actions">
              <button class="btn-save" type="button" @click="onSaveEdit(c.id)" :disabled="!editContent">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                저장
              </button>
              <button class="btn-cancel" type="button" @click="cancelEdit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                취소
              </button>
            </div>
          </div>
        </template>

        <!-- 보기 모드 -->
        <template v-else>
          <div class="comment-main">
            <div class="comment-avatar">
              {{ (c.author_nickname ?? '익').charAt(0) }}
            </div>
            <div class="comment-body">
              <div class="comment-meta">
                <strong class="author">{{ c.author_nickname ?? '익명' }}</strong>
                <span class="date">{{ formatDate(c.created_at) }}</span>
              </div>
              <div class="comment-content">{{ c.content }}</div>
              <div class="comment-footer">
                <button 
                  class="like-btn" 
                  :class="{ liked: c.is_liked }" 
                  type="button" 
                  @click="onToggleCommentLike(c.id)"
                >
                  <svg viewBox="0 0 24 24" :fill="c.is_liked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                    <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
                  </svg>
                  <span>{{ c.likes_count ?? 0 }}</span>
                </button>
              </div>
            </div>
          </div>

          <div v-if="isAuthor(c)" class="comment-actions">
            <button class="action-btn edit" type="button" @click="startEdit(c)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="action-btn delete" type="button" @click="onDelete(c.id)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
              </svg>
            </button>
          </div>
        </template>
      </li>
    </ul>

    <div v-else class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
      </svg>
      <p>아직 댓글이 없습니다.<br>첫 댓글을 작성해보세요!</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const props = defineProps({
  comments: { type: Array, default: () => [] },
})

const emit = defineEmits(['delete', 'update', 'toggle-like'])

const accountStore = useAccountStore()

// 정렬 타입
const sortType = ref('latest')

// 정렬된 댓글 목록
const sortedComments = computed(() => {
  const commentsCopy = [...props.comments]
  if (sortType.value === 'latest') {
    return commentsCopy.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } else if (sortType.value === 'likes') {
    return commentsCopy.sort((a, b) => (b.likes_count || 0) - (a.likes_count || 0))
  }
  return commentsCopy
})

// 정렬 타입 변경
const changeSortType = (type) => {
  sortType.value = type
}

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
.comments-section {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  margin-top: 16px;
}

.comments-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e4e4e7;
  margin-bottom: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.comments-header h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.comments-header .count {
  color: #7469B6;
  margin-left: 4px;
}

/* Sort Buttons */
.sort-buttons {
  display: flex;
  gap: 8px;
}

.sort-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #71717a;
  background: white;
  border: 1px solid #e4e4e7;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-btn svg {
  width: 14px;
  height: 14px;
}

.sort-btn:hover {
  background: #fafafa;
  border-color: #d4d4d8;
  color: #3f3f46;
}

.sort-btn.active {
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
}

.sort-btn.active:hover {
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

/* Comments List */
.comments-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #fafafa;
  border-radius: 14px;
  transition: background 0.2s;
}

.comment-item:hover {
  background: #f4f4f5;
}

.comment-main {
  display: flex;
  gap: 12px;
  flex: 1;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #E1AFD1 0%, #AD88C6 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 700;
  color: #7469B6;
  flex-shrink: 0;
}

.comment-body {
  flex: 1;
  min-width: 0;
}

.comment-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.author {
  font-size: 0.875rem;
  font-weight: 700;
  color: #18181b;
}

.date {
  font-size: 0.75rem;
  color: #a1a1aa;
}

.comment-content {
  font-size: 0.9375rem;
  color: #3f3f46;
  line-height: 1.6;
  white-space: pre-wrap;
}

.comment-footer {
  margin-top: 10px;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #71717a;
  background: white;
  border: 1px solid #e4e4e7;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn svg {
  width: 14px;
  height: 14px;
}

.like-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.like-btn.liked {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

/* Comment Actions */
.comment-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #e4e4e7;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn svg {
  width: 14px;
  height: 14px;
  color: #71717a;
}

.action-btn.edit:hover {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.action-btn.edit:hover svg {
  color: #16a34a;
}

.action-btn.delete:hover {
  background: #fef2f2;
  border-color: #fecaca;
}

.action-btn.delete:hover svg {
  color: #dc2626;
}

/* Edit Mode */
.edit-mode {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.edit-input {
  width: 100%;
  padding: 12px 14px;
  font-size: 0.9375rem;
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  background: white;
  transition: all 0.2s;
  box-sizing: border-box;
}

.edit-input:focus {
  outline: none;
  border-color: #7469B6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.1);
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.btn-save,
.btn-cancel {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save svg,
.btn-cancel svg {
  width: 14px;
  height: 14px;
}

.btn-save {
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border: none;
}

.btn-save:hover {
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.4);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-cancel {
  color: #52525b;
  background: white;
  border: 1px solid #e4e4e7;
}

.btn-cancel:hover {
  background: #f4f4f5;
}

/* Empty State */
.empty-state {
  padding: 40px 20px;
  text-align: center;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #d4d4d8;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 0.9375rem;
  color: #71717a;
  line-height: 1.6;
  margin: 0;
}

/* Dark Mode */
[data-theme="dark"] .comments-section {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .comments-header {
  border-bottom-color: #27272a;
}

[data-theme="dark"] .comments-header h3 {
  color: #e4e4e7;
}

[data-theme="dark"] .comments-header .count {
  color: #E1AFD1;
}

[data-theme="dark"] .sort-btn {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .sort-btn:hover {
  background: #3f3f46;
  border-color: #52525b;
  color: #d4d4d8;
}

[data-theme="dark"] .sort-btn.active {
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
}

[data-theme="dark"] .comment-item {
  background: #27272a;
}

[data-theme="dark"] .comment-item:hover {
  background: #3f3f46;
}

[data-theme="dark"] .author {
  color: #e4e4e7;
}

[data-theme="dark"] .date {
  color: #71717a;
}

[data-theme="dark"] .comment-content {
  color: #a1a1aa;
}

[data-theme="dark"] .like-btn {
  background: #18181b;
  border-color: #3f3f46;
  color: #71717a;
}

[data-theme="dark"] .like-btn:hover {
  background: rgba(220, 38, 38, 0.1);
  border-color: rgba(220, 38, 38, 0.3);
}

[data-theme="dark"] .like-btn.liked {
  background: rgba(220, 38, 38, 0.1);
  border-color: rgba(220, 38, 38, 0.3);
}

[data-theme="dark"] .action-btn {
  background: #18181b;
  border-color: #3f3f46;
}

[data-theme="dark"] .action-btn svg {
  color: #71717a;
}

[data-theme="dark"] .action-btn.edit:hover {
  background: rgba(22, 163, 74, 0.1);
  border-color: rgba(22, 163, 74, 0.3);
}

[data-theme="dark"] .action-btn.delete:hover {
  background: rgba(220, 38, 38, 0.1);
  border-color: rgba(220, 38, 38, 0.3);
}

[data-theme="dark"] .edit-input {
  background: #18181b;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .edit-input:focus {
  border-color: #7469B6;
}

[data-theme="dark"] .btn-cancel {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .btn-cancel:hover {
  background: #3f3f46;
}

[data-theme="dark"] .empty-state svg {
  color: #52525b;
}

[data-theme="dark"] .empty-state p {
  color: #71717a;
}
</style>
