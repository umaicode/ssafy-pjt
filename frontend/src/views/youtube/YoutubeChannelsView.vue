<template>
  <section>
    <div class="header">
      <h3>저장된 채널</h3>
      <button class="btn" @click="channelStore.clearChannels" :disabled="!channelStore.savedChannels.length">
        전체 삭제
      </button>
    </div>

    <p v-if="!channelStore.savedChannels.length" class="empty">등록된 채널 없음</p>

    <ul v-else class="list">
      <li class="item" v-for="c in channelStore.savedChannels" :key="c.id">
        <div class="info">
          <div class="name">{{ c.name }}</div>
          <div class="id">{{ c.id }}</div>
        </div>

        <button class="btn danger" @click="channelStore.removeChannel(c.id)">삭제</button>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { useChannelStore } from '@/stores/youtube/channels'
const channelStore = useChannelStore()
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 10px;
}

.item {
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.info {
  display: grid;
  gap: 4px;
}

.name {
  font-weight: 700;
}

.id {
  font-size: 12px;
  color: #666;
}

.btn {
  border: 1px solid #333;
  background: #fff;
  border-radius: 10px;
  padding: 8px 10px;
  cursor: pointer;
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
