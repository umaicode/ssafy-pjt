<template>
  <div class="wishlist-section">
    <div class="section-header">
      <div class="header-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </div>
      <div class="header-text">
        <h2 class="section-title">좋아요 목록</h2>
        <p class="section-description">관심있는 상품과 콘텐츠를 모아보세요</p>
      </div>
    </div>

    <!-- Category Tabs -->
    <div class="category-tabs">
      <button
        class="category-tab"
        :class="{ active: activeTab === 'products' }"
        @click="activeTab = 'products'"
        type="button"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <path d="M3 9h18"/>
          <path d="M9 21V9"/>
        </svg>
        금융상품
      </button>

      <button
        class="category-tab"
        :class="{ active: activeTab === 'stocks' }"
        @click="activeTab = 'stocks'"
        type="button"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
          <polyline points="16 7 22 7 22 13"/>
        </svg>
        주식
      </button>

      <button
        class="category-tab"
        :class="{ active: activeTab === 'news' }"
        @click="activeTab = 'news'"
        type="button"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/>
          <path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/>
        </svg>
        뉴스
      </button>

      <button
        class="category-tab"
        :class="{ active: activeTab === 'youtube' }"
        @click="activeTab = 'youtube'"
        type="button"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="4" width="20" height="16" rx="2"/>
          <path d="M10 9l5 3-5 3V9z"/>
        </svg>
        유튜브
      </button>
    </div>

    <!-- Products Section -->
    <section v-if="activeTab === 'products'" class="content-section">
      <div v-if="!likeStore.likes.length" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </div>
        <p class="empty-title">아직 좋아요한 상품이 없어요</p>
        <span class="empty-text">금융상품 페이지에서 마음에 드는 상품을 찾아보세요</span>
      </div>

      <div v-else class="product-grid">
        <ProductListItem
          v-for="item in likeStore.likes"
          :key="item.product_type + '_' + item.fin_prdt_cd"
          :product="item"
          :type="item.product_type"
        />
      </div>
    </section>

    <!-- Stocks Section -->
    <section v-else-if="activeTab === 'stocks'" class="content-section">
      <div v-if="stocksLoading" class="loading-state">
        <div class="spinner"></div>
      </div>

      <div v-else-if="!stockStore.bookmarkedStocks.length" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
            <polyline points="16 7 22 7 22 13"/>
          </svg>
        </div>
        <p class="empty-title">아직 북마크한 주식이 없어요</p>
        <span class="empty-text">주식 페이지에서 관심있는 종목을 북마크해보세요</span>
        <RouterLink :to="{ name: 'StockView' }" class="action-link">
          주식 살펴보기
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </RouterLink>
      </div>

      <div v-else class="stock-grid">
        <div 
          v-for="stock in stockStore.bookmarkedStocks" 
          :key="stock.symbol"
          class="stock-card"
          @click="goToStock(stock.symbol)"
        >
          <div class="stock-card-header">
            <div class="stock-badge" :class="stock.market === 'KR' ? 'kr' : 'us'">
              {{ stock.market === 'KR' ? 'KRX' : 'US' }}
            </div>
            <button 
              class="remove-bookmark-btn"
              @click.stop="removeStockBookmark(stock.symbol)"
            >
              <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
              </svg>
            </button>
          </div>
          <div class="stock-card-body">
            <h4 class="stock-card-name">{{ stock.name }}</h4>
            <span class="stock-card-symbol">{{ stock.code || stock.symbol }}</span>
          </div>
          <div class="stock-card-footer">
            <span class="stock-card-price">{{ formatPrice(stock.current_price, stock.market) }}</span>
            <span :class="['stock-card-change', getChangeClass(stock.change_percent)]">
              {{ formatChangePercent(stock.change_percent) }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- News Section -->
    <section v-else-if="activeTab === 'news'" class="content-section">
      <div class="news-layout">
        <NewsList />
        <NewsDetail />
      </div>
    </section>

    <!-- YouTube Section -->
    <section v-else class="content-section">
      <div class="sub-tabs">
        <button
          class="sub-tab"
          :class="{ active: youtubeTab === 'videos' }"
          @click="youtubeTab = 'videos'"
          type="button"
        >
          비디오
        </button>
        <button
          class="sub-tab"
          :class="{ active: youtubeTab === 'channels' }"
          @click="youtubeTab = 'channels'"
          type="button"
        >
          채널
        </button>
      </div>

      <!-- Saved Videos -->
      <div v-if="youtubeTab === 'videos'" class="youtube-content">
        <div class="content-header">
          <span class="content-count">{{ videoStore.savedVideos.length }}개의 비디오</span>
          <button 
            class="clear-btn" 
            @click="videoStore.clearVideos" 
            :disabled="!videoStore.savedVideos.length"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
            </svg>
            전체 삭제
          </button>
        </div>

        <div v-if="!videoStore.savedVideos.length" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="2" y="4" width="20" height="16" rx="2"/>
              <path d="M10 9l5 3-5 3V9z"/>
            </svg>
          </div>
          <p class="empty-title">저장된 비디오가 없습니다</p>
          <span class="empty-text">유튜브 검색에서 마음에 드는 영상을 저장해보세요</span>
        </div>

        <div v-else class="video-grid">
          <article class="video-card" v-for="v in videoStore.savedVideos" :key="v.id">
            <div class="video-thumb-wrapper">
              <img v-if="v.thumbnail" :src="v.thumbnail" class="video-thumb" alt="thumbnail" />
              <div class="video-overlay">
                <RouterLink 
                  :to="{ name: 'YoutubeVideoDetailView', params: { id: v.id } }"
                  class="play-btn"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </RouterLink>
              </div>
            </div>

            <div class="video-info">
              <h4 class="video-title">{{ v.title }}</h4>
              <p class="video-channel">{{ v.channelTitle }}</p>

              <div class="video-actions">
                <RouterLink 
                  class="action-btn view-btn" 
                  :to="{ name: 'YoutubeVideoDetailView', params: { id: v.id } }"
                >
                  보기
                </RouterLink>
                <button class="action-btn remove-btn" @click="videoStore.removeVideo(v.id)">
                  삭제
                </button>
              </div>
            </div>
          </article>
        </div>
      </div>

      <!-- Saved Channels -->
      <div v-else class="youtube-content">
        <div class="content-header">
          <span class="content-count">{{ channelStore.savedChannels.length }}개의 채널</span>
          <button 
            class="clear-btn" 
            @click="channelStore.clearChannels" 
            :disabled="!channelStore.savedChannels.length"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
            </svg>
            전체 삭제
          </button>
        </div>

        <div v-if="!channelStore.savedChannels.length" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 00-3-3.87"/>
              <path d="M16 3.13a4 4 0 010 7.75"/>
            </svg>
          </div>
          <p class="empty-title">저장된 채널이 없습니다</p>
          <span class="empty-text">유튜브에서 즐겨보는 채널을 저장해보세요</span>
        </div>

        <ul v-else class="channel-list">
          <li class="channel-item" v-for="c in channelStore.savedChannels" :key="c.id">
            <div class="channel-avatar">
              {{ (c.name || 'C').charAt(0).toUpperCase() }}
            </div>
            <div class="channel-info">
              <span class="channel-name">{{ c.name }}</span>
              <span class="channel-id">{{ c.id }}</span>
            </div>
            <button class="action-btn remove-btn" @click="channelStore.removeChannel(c.id)">
              삭제
            </button>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { useLikeStore } from '@/stores/like'
import ProductListItem from '@/components/products/ProductListItem.vue'

import { useNewsStore } from '@/stores/news'
import NewsList from '@/components/news/NewsList.vue'
import NewsDetail from '@/components/news/NewsDetail.vue'

import { useVideoStore } from '@/stores/youtube/videos'
import { useChannelStore } from '@/stores/youtube/channels'

import { useStocksStore } from '@/stores/stocks'

const router = useRouter()
const likeStore = useLikeStore()
const newsStore = useNewsStore()
const videoStore = useVideoStore()
const channelStore = useChannelStore()
const stockStore = useStocksStore()

const activeTab = ref('products')
const youtubeTab = ref('videos')
const stocksLoading = ref(false)

onMounted(() => {
  likeStore.getLikes()
})

watch(activeTab, async (tab) => {
  if (tab === 'news') {
    newsStore.setMode('bookmark')
    newsStore.clearDetail()
  } else if (tab === 'stocks') {
    stocksLoading.value = true
    await stockStore.fetchBookmarkedStocks()
    stocksLoading.value = false
  }
})

// 주식 관련 함수
const goToStock = (symbol) => {
  router.push({ name: 'StockView' })
  stockStore.fetchStockDetail(symbol)
}

const removeStockBookmark = async (symbol) => {
  await stockStore.removeBookmark(symbol)
}

const formatPrice = (price, market) => {
  if (!price) return '-'
  if (market === 'KR') {
    return new Intl.NumberFormat('ko-KR').format(price) + '원'
  }
  return '$' + new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(price)
}

const formatChangePercent = (percent) => {
  if (percent === null || percent === undefined) return '-'
  const numPercent = Number(percent)
  const prefix = numPercent > 0 ? '+' : ''
  return prefix + numPercent.toFixed(2) + '%'
}

const getChangeClass = (change) => {
  if (change > 0) return 'up'
  if (change < 0) return 'down'
  return ''
}
</script>

<style scoped>
.wishlist-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  margin: 0;
}

.section-description {
  font-size: 0.9375rem;
  color: #71717a;
  margin: 0;
}

/* Category Tabs */
.category-tabs {
  display: flex;
  gap: 8px;
  background: #f4f4f5;
  padding: 6px;
  border-radius: 16px;
  width: fit-content;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #71717a;
  background: transparent;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-tab svg {
  width: 16px;
  height: 16px;
}

.category-tab:hover {
  color: #52525b;
}

.category-tab.active {
  color: #7469B6;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Sub Tabs */
.sub-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.sub-tab {
  padding: 8px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #71717a;
  background: white;
  border: 2px solid #e4e4e7;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.sub-tab:hover {
  border-color: #7469B6;
  color: #7469B6;
}

.sub-tab.active {
  background: #7469B6;
  border-color: #7469B6;
  color: white;
}

/* Content Section */
.content-section {
  padding: 24px;
  background: #fafafa;
  border-radius: 20px;
}

/* Content Header */
.content-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.content-count {
  font-size: 0.875rem;
  font-weight: 600;
  color: #71717a;
}

.clear-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #dc2626;
  background: white;
  border: 1px solid #fecaca;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn svg {
  width: 14px;
  height: 14px;
}

.clear-btn:hover:not(:disabled) {
  background: #fef2f2;
  border-color: #dc2626;
}

.clear-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 24px;
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  background: rgba(116, 105, 182, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.empty-icon svg {
  width: 32px;
  height: 32px;
  color: #7469B6;
}

.empty-title {
  font-size: 1rem;
  font-weight: 600;
  color: #18181b;
  margin: 0 0 6px;
}

.empty-text {
  font-size: 0.875rem;
  color: #71717a;
}

/* Product Grid */
.product-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

/* News Layout */
.news-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
  height: 500px;
}

@media (max-width: 900px) {
  .news-layout {
    grid-template-columns: 1fr;
    height: auto;
  }
}

/* Video Grid */
.video-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.video-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.video-thumb-wrapper {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.video-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.video-card:hover .video-overlay {
  opacity: 1;
}

.play-btn {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7469B6;
  transition: transform 0.2s;
}

.play-btn:hover {
  transform: scale(1.1);
}

.play-btn svg {
  width: 24px;
  height: 24px;
  margin-left: 4px;
}

.video-info {
  padding: 16px;
}

.video-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #18181b;
  line-height: 1.4;
  margin: 0 0 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-channel {
  font-size: 0.8125rem;
  color: #71717a;
  margin: 0 0 12px;
}

.video-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.view-btn {
  background: rgba(116, 105, 182, 0.1);
  color: #7469B6;
  border: none;
}

.view-btn:hover {
  background: #7469B6;
  color: white;
}

.remove-btn {
  background: white;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.remove-btn:hover {
  background: #fef2f2;
  border-color: #dc2626;
}

/* Channel List */
.channel-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

.channel-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.channel-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.channel-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.channel-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #18181b;
}

.channel-id {
  font-size: 0.75rem;
  color: #a1a1aa;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Responsive */
@media (max-width: 768px) {
  .category-tabs {
    width: 100%;
    overflow-x: auto;
  }

  .category-tab {
    flex-shrink: 0;
  }

  .video-grid {
    grid-template-columns: 1fr;
  }
}

/* Dark Mode */
[data-theme="dark"] .section-title {
  color: #e4e4e7;
}

[data-theme="dark"] .section-description {
  color: #71717a;
}

[data-theme="dark"] .category-tabs {
  background: #27272a;
}

[data-theme="dark"] .category-tab {
  color: #a1a1aa;
}

[data-theme="dark"] .category-tab:hover {
  color: #e4e4e7;
}

[data-theme="dark"] .category-tab.active {
  color: #E1AFD1;
  background: #18181b;
}

[data-theme="dark"] .sub-tab {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .sub-tab:hover {
  border-color: #7469B6;
  color: #E1AFD1;
}

[data-theme="dark"] .sub-tab.active {
  background: #7469B6;
  border-color: #7469B6;
  color: white;
}

[data-theme="dark"] .content-section {
  background: #0f0f0f;
}

[data-theme="dark"] .content-count {
  color: #71717a;
}

[data-theme="dark"] .clear-btn {
  background: #27272a;
  border-color: rgba(220, 38, 38, 0.3);
}

[data-theme="dark"] .clear-btn:hover:not(:disabled) {
  background: rgba(220, 38, 38, 0.1);
}

[data-theme="dark"] .empty-icon {
  background: rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .empty-title {
  color: #e4e4e7;
}

[data-theme="dark"] .empty-text {
  color: #71717a;
}

[data-theme="dark"] .video-card {
  background: #18181b;
}

[data-theme="dark"] .video-title {
  color: #e4e4e7;
}

[data-theme="dark"] .video-channel {
  color: #71717a;
}

[data-theme="dark"] .view-btn {
  background: rgba(116, 105, 182, 0.2);
  color: #E1AFD1;
}

[data-theme="dark"] .remove-btn {
  background: #27272a;
  border-color: rgba(220, 38, 38, 0.3);
}

[data-theme="dark"] .remove-btn:hover {
  background: rgba(220, 38, 38, 0.1);
}

[data-theme="dark"] .channel-item {
  background: #18181b;
}

[data-theme="dark"] .channel-name {
  color: #e4e4e7;
}

[data-theme="dark"] .channel-id {
  color: #71717a;
}

/* Stock Grid */
.stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.stock-card {
  background: white;
  border-radius: 16px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #f0f0f0;
}

.stock-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stock-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.stock-badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
}

.stock-badge.kr {
  background: rgba(116, 105, 182, 0.1);
  color: #7469B6;
}

.stock-badge.us {
  background: rgba(74, 144, 217, 0.1);
  color: #4a90d9;
}

.remove-bookmark-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-bookmark-btn svg {
  width: 18px;
  height: 18px;
  color: #7469B6;
}

.remove-bookmark-btn:hover {
  background: rgba(116, 105, 182, 0.1);
}

.stock-card-body {
  margin-bottom: 14px;
}

.stock-card-name {
  font-size: 1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stock-card-symbol {
  font-size: 0.8125rem;
  color: #888;
}

.stock-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stock-card-price {
  font-size: 1.125rem;
  font-weight: 800;
  color: #1a1a1a;
}

.stock-card-change {
  font-size: 0.875rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 8px;
}

.stock-card-change.up {
  background: rgba(229, 91, 91, 0.1);
  color: #e55b5b;
}

.stock-card-change.down {
  background: rgba(74, 144, 217, 0.1);
  color: #4a90d9;
}

/* Action Link */
.action-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 16px;
  padding: 10px 18px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.2s;
}

.action-link svg {
  width: 16px;
  height: 16px;
}

.action-link:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

/* Loading State */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 48px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f0f0f0;
  border-top-color: #7469B6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Dark Mode for Stock */
[data-theme="dark"] .stock-card {
  background: #18181b;
  border-color: #27272a;
}

[data-theme="dark"] .stock-card-name {
  color: #e4e4e7;
}

[data-theme="dark"] .stock-card-price {
  color: #e4e4e7;
}
</style>
