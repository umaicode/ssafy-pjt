<template>
  <div class="wrap">
    <RouterLink class="back" :to="{ name: 'CommunityView' }">← 목록으로</RouterLink>

    <section v-if="store.article" class="card">
      <!-- 수정 모드 -->
      <template v-if="isEditing">
        <h2 class="h2">게시글 수정</h2>
        <form class="edit-form" @submit.prevent="onUpdateArticle">
          <input v-model.trim="editTitle" class="input" placeholder="제목" />
          <textarea v-model.trim="editContent" class="textarea" placeholder="내용"></textarea>
          <div class="edit-actions">
            <button class="btn" type="submit" :disabled="!canSave">저장</button>
            <button class="btn ghost" type="button" @click="cancelEdit">취소</button>
          </div>
        </form>
      </template>

      <!-- 보기 모드 -->
      <template v-else>
        <div class="top">
          <h2 class="h2">{{ store.article.title }}</h2>

          <div v-if="isAuthor" class="actions">
            <button class="edit" type="button" @click="startEdit">수정</button>
            <button class="danger" type="button" @click="onDeleteArticle">삭제</button>
          </div>
        </div>

        <div class="meta">
          <span>작성자: {{ store.article.author_nickname ?? '익명' }}</span>
          <span>작성일: {{ formatDate(store.article.created_at) }}</span>
          <span>조회: {{ store.article.views ?? 0 }}</span>
        </div>

        <p class="body">{{ store.article.content }}</p>
      </template>
    </section>

    <p v-else class="loading">게시글을 불러오는 중...</p>

    <!-- 댓글 목록 -->
    <Comment
      :comments="store.comments"
      @delete="onDeleteComment"
      @update="onUpdateComment"
    />
    <!-- 댓글 작성 -->
    <CommentCreate @submit="onCreateComment" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import { useAccountStore } from '@/stores/accounts'
import Comment from '@/components/community/Comment.vue'
import CommentCreate from '@/components/community/CommentCreate.vue'

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()
const accountStore = useAccountStore()

const articleId = route.params.id

// 수정 모드 상태
const isEditing = ref(false)
const editTitle = ref('')
const editContent = ref('')

// 저장 버튼 활성화 조건
const canSave = computed(() => editTitle.value && editContent.value)

// 현재 로그인 유저가 작성자인지 확인
const isAuthor = computed(() => {
  if (!accountStore.nickname || !store.article) return false
  return accountStore.nickname === store.article.author_nickname
})

onMounted(() => {
  store.getArticleDetail(articleId)
    .then(() => store.getComments(articleId))
    .catch(() => {})
})

// 수정 모드 시작
const startEdit = () => {
  editTitle.value = store.article.title
  editContent.value = store.article.content
  isEditing.value = true
}

// 수정 취소
const cancelEdit = () => {
  isEditing.value = false
  editTitle.value = ''
  editContent.value = ''
}

// 게시글 수정
const onUpdateArticle = () => {
  store.updateArticle(articleId, {
    title: editTitle.value,
    content: editContent.value
  })
    .then(() => {
      isEditing.value = false
      alert('수정되었습니다.')
    })
    .catch((err) => {
      console.log(err)
      alert('수정에 실패했습니다.')
    })
}

// 게시글 삭제
const onDeleteArticle = () => {
  const ok = window.confirm('게시글을 삭제할까요?\n삭제 후 복구할 수 없습니다.')
  if (!ok) return

  store.deleteArticle(articleId)
    .then(() => {
      alert('삭제되었습니다.')
      router.push({ name: 'CommunityView' })
    })
    .catch(() => {
      alert('게시글 삭제에 실패했습니다.')
    })
}

// 댓글 작성
const onCreateComment = (content) => {
  if (!content.trim()) return

  store.createComment(articleId, content)
    .then(() => {})
    .catch(() => {
      alert('댓글 작성에 실패했습니다.')
    })
}

// 댓글 수정
const onUpdateComment = ({ id, content }) => {
  store.updateComment(id, content)
    .then(() => {})
    .catch(() => {
      alert('댓글 수정에 실패했습니다.')
    })
}

// 댓글 삭제
const onDeleteComment = (commentId) => {
  store.deleteComment(commentId)
    .then(() => {})
    .catch(() => {
      alert('댓글 삭제에 실패했습니다.')
    })
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
.wrap { max-width: 1000px; margin: 0 auto; padding: 24px 16px; }
.back { display: inline-block; margin-bottom: 12px; text-decoration: none; color: #333; }
.card { border: 1px solid #eee; border-radius: 12px; padding: 16px; }
.top { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.h2 { margin: 0; }
.actions { display: flex; gap: 8px; }
.meta { display: flex; gap: 12px; color: #666; font-size: 13px; margin-top: 8px; flex-wrap: wrap; }
.body { margin-top: 14px; white-space: pre-wrap; }
.loading { color: #777; }

/* 버튼 스타일 */
.edit { border: 1px solid #ddd; background: #fff; border-radius: 10px; padding: 8px 10px; cursor: pointer; }
.edit:hover { background: #f5f5f5; }
.danger { border: 1px solid #f2b8c6; color: #b00020; background: #fff; border-radius: 10px; padding: 8px 10px; cursor: pointer; }
.danger:hover { background: #fff5f7; border-color: #b00020; }

/* 수정 폼 */
.edit-form { display: grid; gap: 10px; margin-top: 12px; }
.input, .textarea { padding: 10px 12px; border: 1px solid #ddd; border-radius: 10px; }
.textarea { min-height: 180px; resize: vertical; }
.edit-actions { display: flex; gap: 10px; }
.btn { padding: 10px 12px; border: 1px solid #333; border-radius: 10px; background: #fff; cursor: pointer; }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.ghost { border-color: #ddd; }
</style>
