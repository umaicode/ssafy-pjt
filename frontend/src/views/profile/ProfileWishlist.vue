<template>
  <div>
    <h3>좋아요 목록</h3>

    <div class="tabs">
      <button
        class="tab"
        :class="{ active: activeTab === 'products' }"
        @click="activeTab = 'products'"
        type="button"
      >
        금융상품
      </button>

      <button
        class="tab"
        :class="{ active: activeTab === 'news' }"
        @click="activeTab = 'news'"
        type="button"
      >
        뉴스
      </button>

      <button
        class="tab"
        :class="{ active: activeTab === 'youtube' }"
        @click="activeTab = 'youtube'"
        type="button"
      >
        유튜브
      </button>
    </div>

    <!-- 1) ✅ 금융상품 좋아요 -->
    <section v-if="activeTab === 'products'">
      <p v-if="!wishlistStore.wishlist.length">아직 좋아요한 상품이 없어요.</p>

      <div v-else>
        <ProductListItem
          v-for="item in wishlistStore.wishlist"
          :key="item.product_type + '_' + item.fin_prdt_cd"
          :product="item"
          :type="item.product_type"
        />
      </div>
    </section>

    <section v-else-if="activeTab === 'news'" class="panel">
      <div class="news-two-col">
        <NewsList />
        <NewsDetail />
      </div>
    </section>

    <!-- 3) ✅ 유튜브 저장됨 -->
    <section v-else class="panel">
      <div class="youtube-tabs">
        <button
          class="yt-tab"
          :class="{ active: youtubeTab === 'videos' }"
          @click="youtubeTab = 'videos'"
          type="button"
        >
          비디오
        </button>
        <button
          class="yt-tab"
          :class="{ active: youtubeTab === 'channels' }"
          @click="youtubeTab = 'channels'"
          type="button"
        >
          채널
        </button>
      </div>

      <!-- 저장된 비디오 -->
      <div v-if="youtubeTab === 'videos'" class="youtube-content">
        <div class="youtube-header">
          <h4>저장된 비디오</h4>
          <button class="btn-clear" @click="videoStore.clearVideos" :disabled="!videoStore.savedVideos.length">
            전체 삭제
          </button>
        </div>

        <p v-if="!videoStore.savedVideos.length" class="empty">저장된 비디오가 없습니다.</p>

        <div v-else class="video-grid">
          <article class="video-card" v-for="v in videoStore.savedVideos" :key="v.id">
            <img v-if="v.thumbnail" :src="v.thumbnail" class="thumb" alt="thumbnail" />

            <div class="video-body">
              <h5 class="video-title">{{ v.title }}</h5>
              <p class="video-channel">{{ v.channelTitle }}</p>

              <div class="video-actions">
                <RouterLink
                  class="btn-action"
                  :to="{ name: 'YoutubeVideoDetailView', params: { id: v.id } }"
                >
                  보기
                </RouterLink>

                <button class="btn-action btn-danger" @click="videoStore.removeVideo(v.id)">삭제</button>
              </div>
            </div>
          </article>
        </div>
      </div>

      <!-- 저장된 채널 -->
      <div v-else class="youtube-content">
        <div class="youtube-header">
          <h4>저장된 채널</h4>
          <button class="btn-clear" @click="channelStore.clearChannels" :disabled="!channelStore.savedChannels.length">
            전체 삭제
          </button>
        </div>

        <p v-if="!channelStore.savedChannels.length" class="empty">저장된 채널이 없습니다.</p>

        <ul v-else class="channel-list">
          <li class="channel-item" v-for="c in channelStore.savedChannels" :key="c.id">
            <div class="channel-info">
              <div class="channel-name">{{ c.name }}</div>
              <div class="channel-id">{{ c.id }}</div>
            </div>

            <button class="btn-action btn-danger" @click="channelStore.removeChannel(c.id)">삭제</button>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'

import { useWishlistStore } from '@/stores/wishlist'
import ProductListItem from '@/components/products/ProductListItem.vue'

import { useNewsStore } from '@/stores/news'
import NewsList from '@/components/news/NewsList.vue'
import NewsDetail from '@/components/news/NewsDetail.vue'

import { useVideoStore } from '@/stores/youtube/videos'
import { useChannelStore } from '@/stores/youtube/channels'


const wishlistStore = useWishlistStore()
const newsStore = useNewsStore()
const videoStore = useVideoStore()
const channelStore = useChannelStore()

// ✅ 첫 탭이 기본
const activeTab = ref('products')
const youtubeTab = ref('videos')

onMounted(() => {
  // 첫번째 탭(상품) 들어왔을 때 목록 불러오기
  wishlistStore.getWishlist()
})

// ✅ 탭 전환 시 필요한 데이터만 로드
watch(activeTab, (tab) => {
  if (tab === 'news') {
    // 북마크 모드로 전환하고 북마크한 뉴스 목록 로드
    newsStore.setMode('bookmark')
    newsStore.clearDetail()
  }
  // 유튜브 탭은 YoutubeSavedLayoutView 내부 로직에 맡김
})
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 8px;
  margin: 12px 0 16px;
}

.tab {
  padding: 8px 14px;
  border: 1px solid #ccc;
  border-radius: 18px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
}

.tab.active {
  background: #f5dfdf;
  color: #0a0a0a;
  border-color: #333;
}

.panel {
  margin-top: 10px;
}

.news-two-col {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 14px;
  height: 70vh;
}

/* 유튜브 섹션 스타일 */
.youtube-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.yt-tab {
  padding: 8px 14px;
  border: 1px solid #ccc;
  border-radius: 18px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
}

.yt-tab.active {
  background: #f5dfdf;
  color: #0a0a0a;
  border-color: #333;
}

.youtube-content {
  margin-top: 12px;
}

.youtube-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.youtube-header h4 {
  margin: 0;
  font-size: 16px;
}

.btn-clear {
  padding: 6px 12px;
  border: 1px solid #333;
  background: #fff;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
}

.btn-clear:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.empty {
  color: #777;
  font-size: 14px;
  padding: 20px 0;
}

/* 비디오 그리드 */
.video-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

@media (min-width: 768px) {
  .video-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 1024px) {
  .video-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.video-card {
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  overflow: hidden;
  background: #fff;
  display: flex;
  flex-direction: column;
}

.thumb {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  background: #f3f3f3;
}

.video-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.video-title {
  margin: 0;
  font-size: 14px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-channel {
  margin: 0;
  font-size: 12px;
  color: #666;
}

.video-actions {
  display: flex;
  gap: 6px;
  margin-top: 4px;
}

.btn-action {
  padding: 6px 12px;
  border: 1px solid #333;
  background: #fff;
  border-radius: 10px;
  cursor: pointer;
  font-size: 12px;
  text-decoration: none;
  color: inherit;
  display: inline-block;
}

.btn-danger {
  border-color: #c0392b;
  color: #c0392b;
}

/* 채널 리스트 */
.channel-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 10px;
}

.channel-item {
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  background: #fff;
}

.channel-info {
  display: grid;
  gap: 4px;
}

.channel-name {
  font-weight: 700;
  font-size: 14px;
}

.channel-id {
  font-size: 12px;
  color: #666;
}
</style>
