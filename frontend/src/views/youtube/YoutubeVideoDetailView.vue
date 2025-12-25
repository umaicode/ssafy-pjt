<template>
  <section class="video-detail-page">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>불러오는 중...</p>
    </div>

    <!-- Not Found -->
    <div v-else-if="!video" class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="2" y="4" width="20" height="16" rx="2"/>
          <path d="M10 9l5 3-5 3V9z"/>
        </svg>
      </div>
      <p class="empty-title">영상을 찾을 수 없어요</p>
      <RouterLink class="back-link" :to="{ name: 'YoutubeSearchView' }">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"/>
          <polyline points="12 19 5 12 12 5"/>
        </svg>
        검색으로 돌아가기
      </RouterLink>
    </div>

    <!-- Video Content -->
    <div v-else class="video-content">
      <!-- Video Player -->
      <div class="player-section">
        <div class="player-wrapper">
          <iframe
            :src="embedUrl"
            title="YouTube"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          />
        </div>
      </div>

      <!-- Video Info -->
      <div class="info-section">
        <h1 class="video-title">{{ decodedTitle }}</h1>

        <div class="video-meta">
          <div class="channel-badge">
            <div class="channel-avatar">
              {{ (decodedChannelTitle || 'C').charAt(0).toUpperCase() }}
            </div>
            <span class="channel-name">{{ decodedChannelTitle }}</span>
          </div>

          <div class="action-buttons">
            <button class="action-btn" :class="{ active: videoStore.isSaved(id) }" @click="toggleVideo">
              <svg v-if="videoStore.isSaved(id)" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
              </svg>
              {{ videoStore.isSaved(id) ? '저장됨' : '저장하기' }}
            </button>

            <button class="action-btn" :class="{ active: channelStore.isSaved(channelId) }" @click="toggleChannel">
              <svg v-if="channelStore.isSaved(channelId)" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              {{ channelStore.isSaved(channelId) ? '채널 저장됨' : '채널 저장' }}
            </button>
          </div>
        </div>

        <div class="description-card">
          <h3 class="description-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="17" y1="10" x2="3" y2="10"/>
              <line x1="21" y1="6" x2="3" y2="6"/>
              <line x1="21" y1="14" x2="3" y2="14"/>
              <line x1="17" y1="18" x2="3" y2="18"/>
            </svg>
            설명
          </h3>
          <p class="description-text">{{ decodedDescription || '설명이 없습니다.' }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { fetchVideoDetail } from '@/stores/youtube/youtube'
import { useVideoStore } from '@/stores/youtube/videos'
import { useChannelStore } from '@/stores//youtube/channels'
import { useAccountStore } from '@/stores/accounts' 

const props = defineProps({
  id: String,
})

const videoStore = useVideoStore()
const channelStore = useChannelStore()
const accountStore = useAccountStore()  

const video = ref(null)
const loading = ref(false)

// HTML 엔티티 디코딩 함수
const decodeHtmlEntities = (text) => {
  if (!text) return ''
  const textarea = document.createElement('textarea')
  textarea.innerHTML = text
  return textarea.value
}

const embedUrl = computed(() => `https://www.youtube.com/embed/${props.id}`)
const channelId = computed(() => video.value?.snippet?.channelId ?? '')
const decodedTitle = computed(() => decodeHtmlEntities(video.value?.snippet?.title ?? ''))
const decodedChannelTitle = computed(() => decodeHtmlEntities(video.value?.snippet?.channelTitle ?? ''))
const decodedDescription = computed(() => decodeHtmlEntities(video.value?.snippet?.description ?? ''))

async function load() {
  loading.value = true
  try {
    video.value = await fetchVideoDetail(props.id)
  } finally {
    loading.value = false
  }
}

// 로그인체크
function toggleVideo() {
  if (!accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return
  }

  if (!video.value) return
  videoStore.toggleVideo({
    id: props.id,
    title: decodeHtmlEntities(video.value.snippet.title),
    channelTitle: decodeHtmlEntities(video.value.snippet.channelTitle),
    thumbnail:
      video.value.snippet.thumbnails?.medium?.url ??
      video.value.snippet.thumbnails?.default?.url ??
      '',
  })
}

function toggleChannel() {
  if (!accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return
  }

  if (!video.value) return
  channelStore.toggleChannel({
    id: video.value.snippet.channelId,
    name: decodeHtmlEntities(video.value.snippet.channelTitle),
  })
}

onMounted(load)
watch(() => props.id, load)
</script>

<style scoped>
.video-detail-page {
  min-height: calc(100vh - 200px);
  background: linear-gradient(180deg, #18181b 0%, #27272a 30%, #fafafa 30%);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120px 24px;
  color: #71717a;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e4e4e7;
  border-top-color: #7469B6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120px 24px;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: rgba(116, 105, 182, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #7469B6;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #18181b;
  margin: 0 0 16px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #7469B6;
  background: rgba(116, 105, 182, 0.1);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
}

.back-link svg {
  width: 18px;
  height: 18px;
}

.back-link:hover {
  background: #7469B6;
  color: white;
}

/* Video Content */
.video-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px 60px;
}

/* Player Section */
.player-section {
  padding-top: 24px;
}

.player-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.player-wrapper iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

/* Info Section */
.info-section {
  margin-top: 32px;
}

.video-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  line-height: 1.4;
  margin: 0 0 20px;
}

.video-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.channel-badge {
  display: flex;
  align-items: center;
  gap: 12px;
}

.channel-avatar {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
}

.channel-name {
  font-size: 1rem;
  font-weight: 600;
  color: #18181b;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #3f3f46;
  background: white;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn:hover {
  border-color: #7469B6;
  color: #7469B6;
}

.action-btn.active {
  background: #7469B6;
  border-color: #7469B6;
  color: white;
}

/* Description Card */
.description-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.description-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 16px;
}

.description-title svg {
  width: 20px;
  height: 20px;
  color: #7469B6;
}

.description-text {
  font-size: 0.9375rem;
  color: #52525b;
  line-height: 1.7;
  margin: 0;
  white-space: pre-wrap;
}

/* Responsive */
@media (max-width: 768px) {
  .video-content {
    padding: 0 16px 40px;
  }

  .player-wrapper {
    border-radius: 16px;
  }

  .video-title {
    font-size: 1.25rem;
  }

  .video-meta {
    flex-direction: column;
    align-items: stretch;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-btn {
    justify-content: center;
  }
}

/* Dark Mode */
[data-theme="dark"] .video-detail-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #0f0f0f 30%, #0a0a0a 30%);
}

[data-theme="dark"] .loading-state {
  color: #a1a1aa;
}

[data-theme="dark"] .loading-spinner {
  border-color: #3f3f46;
  border-top-color: #7469B6;
}

[data-theme="dark"] .empty-icon {
  background: rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .empty-title {
  color: #e4e4e7;
}

[data-theme="dark"] .back-link {
  background: rgba(116, 105, 182, 0.2);
  color: #E1AFD1;
}

[data-theme="dark"] .back-link:hover {
  background: #7469B6;
  color: white;
}

[data-theme="dark"] .video-title {
  color: #e4e4e7;
}

[data-theme="dark"] .channel-name {
  color: #e4e4e7;
}

[data-theme="dark"] .action-btn {
  background: #18181b;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .action-btn:hover {
  border-color: #7469B6;
  color: #E1AFD1;
}

[data-theme="dark"] .action-btn.active {
  background: #7469B6;
  border-color: #7469B6;
  color: white;
}

[data-theme="dark"] .description-card {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .description-title {
  color: #e4e4e7;
}

[data-theme="dark"] .description-text {
  color: #a1a1aa;
}
</style>
