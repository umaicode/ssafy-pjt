<template>
  <div class="page">
    <NewsHeader />
    <main class="container">
      <div class="layout">
        <NewsList />
        <NewsDetail />
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useNewsStore } from '@/stores/news'

import NewsHeader from '@/components/news/NewsHeader.vue'
import NewsList from '@/components/news/NewsList.vue'
import NewsDetail from '@/components/news/NewsDetail.vue'

const route = useRoute()
const newsStore = useNewsStore()

const syncModeAndLoad = function () {
  if (route.name === 'NewsBookmarkView') {
    newsStore.mode = 'bookmark'
  } else {
    newsStore.mode = 'all'
  }
  newsStore.clearDetail()
  newsStore.getNewsList()
}

onMounted(() => {
  syncModeAndLoad()
})

watch(
  () => route.name,
  () => {
    syncModeAndLoad()
  }
)
</script>

<style scoped>
.page { min-height: 100vh; background: #fff; }
.container { padding: 16px; }
.layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 14px;

  /* ⭐ 핵심 */
  height: calc(100vh - 72px); /* 헤더 높이만큼 빼기 */
}

</style>
