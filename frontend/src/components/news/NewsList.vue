<template>
  <section class="news-list">
    <p v-if="!newsStore.newsList.length" class="news-empty">
      아직 저장된 기사가 없습니다.
    </p>

    <div
      v-for="n in newsStore.newsList"
      :key="n.id"
      class="news-item"
      :class="{ selected: newsStore.newsDetail && newsStore.newsDetail.id === n.id }"
      @click="openDetail(n.id)"
    >
      <button class="star"
        @click.stop="toggleBookmark(n.id)"
        type="button">{{ n.is_bookmarked ? '★' : '☆' }}</button>
      <span class="text">{{ n.title }}</span>
    </div>
  </section>
</template>

<script setup>
import { useNewsStore } from '@/stores/news'
import { useAccountStore } from '@/stores/accounts'

const newsStore = useNewsStore()
const accountStore = useAccountStore()

const openDetail = (id) => {
  newsStore.getNewsDetail(id)
}

// 북마크버튼기능, 로그인체크
const toggleBookmark = (id) => {
  if (!accountStore.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }
  newsStore.toggleBookmark(id)
}
</script>

<style scoped>
.news-list {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 12px;

  height: 100%;
  overflow-y: auto;
}
.news-item {
  cursor: pointer;
  padding: 10px 10px;
  border-radius: 10px;
  display: flex;
  gap: 10px;
  align-items: center;
}
.news-item:hover { background: #fafafa; }
.news-item.selected { background: #fff3ee; }
.star { width: 30px; 
        color: rgb(191, 194, 33);
        padding: 2px;
}
.news-empty { color: #777; padding: 12px; }
</style>
