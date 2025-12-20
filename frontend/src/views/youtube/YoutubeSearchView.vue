<template>
  <section>
    <h3>비디오 검색</h3>

    <form class="search" @submit.prevent="onSearch">
      <input
        v-model.trim="q"
        class="input"
        placeholder="검색어를 입력하세요 (예: 삼성전자)"
      />
      <button class="btn" :disabled="loading || !q">
        {{ loading ? '검색중...' : 'Search' }}
      </button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="items.length" class="grid">
      <VideoCard v-for="it in items" :key="it.etag" :item="it" />
    </div>

    <p v-else class="empty">검색 결과가 없습니다.</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { searchVideos } from '@/stores/youtube/youtube'
import VideoCard from '@/components/youtube/VideoCard.vue'

const q = ref('')
const items = ref([])
const loading = ref(false)
const error = ref('')

async function onSearch() {
  error.value = ''
  items.value = []
  loading.value = true

  try {
    items.value = await searchVideos(q.value)
  } catch (e) {
    error.value = '검색 중 오류가 발생했어요. API Key/쿼터/네트워크를 확인하세요.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.search {
  display: flex;
  gap: 8px;
  margin: 12px 0 16px;
}

.input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.btn {
  padding: 10px 14px;
  border: 1px solid #333;
  background: #fff;
  border-radius: 10px;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  color: #c0392b;
  margin: 8px 0 12px;
}

.grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.empty {
  color: #777;
}
</style>
