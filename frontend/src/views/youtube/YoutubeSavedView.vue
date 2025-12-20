<template>
  <section>
    <div class="header">
      <h3>저장된 비디오</h3>
      <button class="btn" @click="videoStore.clearVideos" :disabled="!videoStore.savedVideos.length">
        전체 삭제
      </button>
    </div>

    <p v-if="!videoStore.savedVideos.length" class="empty">등록된 비디오 없음</p>

    <div v-else class="grid">
      <article class="card" v-for="v in videoStore.savedVideos" :key="v.id">
        <img v-if="v.thumbnail" :src="v.thumbnail" class="thumb" alt="thumbnail" />

        <div class="body">
          <h4 class="title">{{ v.title }}</h4>
          <p class="channel">{{ v.channelTitle }}</p>

          <div class="actions">
            <RouterLink
              class="btn"
              :to="{ name: 'YoutubeVideoDetailView', params: { id: v.id } }"
            >
              보기
            </RouterLink>

            <button class="btn danger" @click="videoStore.removeVideo(v.id)">삭제</button>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useVideoStore } from '@/stores/youtube/videos'

const videoStore = useVideoStore()
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
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

.card {
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

.body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.title {
  margin: 0;
  font-size: 14px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.channel {
  margin: 0;
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.actions {
  margin-top: auto;
  display: flex;
  gap: 8px;
}

.btn {
  border: 1px solid #333;
  background: #fff;
  border-radius: 10px;
  padding: 8px 10px;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  text-align: center;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.danger {
  border-color: #c0392b;
}
.empty {
  color: #777;
}
</style>
