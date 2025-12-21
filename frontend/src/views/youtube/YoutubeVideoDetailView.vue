<template>
  <section>
    <p v-if="loading" class="muted">불러오는 중...</p>
    <p v-else-if="!video" class="muted">영상을 찾을 수 없어요.</p>

    <div v-else class="wrap">
      <div class="player">
        <iframe
          :src="embedUrl"
          title="YouTube"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        />
      </div>

      <h3 class="title">{{ video.snippet.title }}</h3>

      <div class="meta">
        <span class="badge">{{ video.snippet.channelTitle }}</span>

        <button class="btn"
          @click="toggleVideo"
        >
          {{ videoStore.isSaved(id) ? '저장 취소' : '나중에 볼 영상 저장' }}
        </button>

        <button class="btn"
          @click="toggleChannel"
        >
          {{ channelStore.isSaved(channelId) ? '채널 저장 취소' : '채널 저장' }}
        </button>
      </div>

      <p class="desc">{{ video.snippet.description }}</p>
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

const embedUrl = computed(() => `https://www.youtube.com/embed/${props.id}`)
const channelId = computed(() => video.value?.snippet?.channelId ?? '')

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
    title: video.value.snippet.title,
    channelTitle: video.value.snippet.channelTitle,
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
    name: video.value.snippet.channelTitle,
  })
}

onMounted(load)
watch(() => props.id, load)
</script>

<style scoped>
.muted {
  color: #777;
}

.wrap {
  display: grid;
  gap: 12px;
}

.player {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #f3f3f3;
  border-radius: 14px;
  overflow: hidden;
}

.player iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

.title {
  margin: 0;
  line-height: 1.35;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.badge {
  border: 1px solid #ddd;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
}

.btn {
  border: 1px solid #333;
  background: #fff;
  border-radius: 10px;
  padding: 8px 10px;
  cursor: pointer;
}

.desc {
  white-space: pre-wrap;
  margin: 0;
}
</style>
