<template>
  <article class="card">
    <img v-if="thumb" :src="thumb" class="thumb" alt="thumbnail" />

    <div class="body">
      <h4 class="title" :title="title">{{ title }}</h4>
      <p class="channel" :title="channel">{{ channel }}</p>

      <RouterLink
        v-if="videoId"
        class="btn"
        :to="{ name: 'YoutubeVideoDetailView', params: { id: videoId } }"
      >
        상세보기
      </RouterLink>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  item: { type: Object, required: true },
})

const videoId = computed(() => props.item?.id?.videoId)
const title = computed(() => props.item?.snippet?.title ?? '')
const channel = computed(() => props.item?.snippet?.channelTitle ?? '')
const thumb = computed(() =>
  props.item?.snippet?.thumbnails?.medium?.url
  ?? props.item?.snippet?.thumbnails?.default?.url
  ?? ''
)
</script>

<style scoped>
.card {
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  overflow: hidden;
  background: #fff;
  display: flex;
  flex-direction: column;
  min-height: 240px;
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
  flex: 1;
  flex-direction: column;
  gap: 8px;
}

.title {
  font-size: 14px;
  margin: 0;
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

.btn {
  margin-top: auto;
  text-decoration: none;
  border: 1px solid #333;
  border-radius: 10px;
  padding: 8px 10px;
  text-align: center;
  color: inherit;
}
</style>
