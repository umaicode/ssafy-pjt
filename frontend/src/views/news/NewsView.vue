<template>
  <div class="news-page">
    <NewsHeader />
    <main class="news-container">
      <div class="news-layout">
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
.news-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 50%, #FAFAFA 100%);
}

.news-container {
  padding: 24px;
}

.news-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
  height: calc(100vh - 160px);
  max-width: 1400px;
  margin: 0 auto;
}

@media (max-width: 900px) {
  .news-layout {
    grid-template-columns: 1fr;
    height: auto;
  }
}

/* Dark Mode */
[data-theme="dark"] .news-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #18181b 50%, #0f0f0f 100%);
}
</style>
