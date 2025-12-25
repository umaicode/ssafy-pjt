<template>
  <section class="saved-channels">
    <!-- Header -->
    <div class="section-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 00-3-3.87"/>
            <path d="M16 3.13a4 4 0 010 7.75"/>
          </svg>
        </div>
        <div>
          <h3 class="section-title">저장된 채널</h3>
          <span class="section-count">{{ channelStore.savedChannels.length }}개의 채널</span>
        </div>
      </div>
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

    <!-- Empty State -->
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
      <span class="empty-text">비디오 상세에서 마음에 드는 채널을 저장해보세요</span>
      <RouterLink class="search-link" :to="{ name: 'YoutubeSearchView' }">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        비디오 검색하기
      </RouterLink>
    </div>

    <!-- Channel List -->
    <ul v-else class="channel-list">
      <li class="channel-item" v-for="c in channelStore.savedChannels" :key="c.id">
        <div class="channel-avatar">
          {{ (c.name || 'C').charAt(0).toUpperCase() }}
        </div>
        <div class="channel-info">
          <span class="channel-name">{{ c.name }}</span>
          <span class="channel-id">{{ c.id }}</span>
        </div>
        <button class="delete-btn" @click="channelStore.removeChannel(c.id)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
          </svg>
          삭제
        </button>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { useChannelStore } from '@/stores/youtube/channels'
const channelStore = useChannelStore()
</script>

<style scoped>
.saved-channels {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Section Header */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon svg {
  width: 22px;
  height: 22px;
  color: white;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.section-count {
  font-size: 0.8125rem;
  color: #71717a;
}

.clear-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
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
  width: 16px;
  height: 16px;
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
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.empty-icon {
  width: 72px;
  height: 72px;
  background: rgba(116, 105, 182, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.empty-icon svg {
  width: 36px;
  height: 36px;
  color: #7469B6;
}

.empty-title {
  font-size: 1.0625rem;
  font-weight: 600;
  color: #18181b;
  margin: 0 0 6px;
}

.empty-text {
  font-size: 0.875rem;
  color: #71717a;
  margin-bottom: 20px;
}

.search-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
}

.search-link svg {
  width: 18px;
  height: 18px;
}

.search-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.35);
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
  padding: 16px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.channel-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.channel-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
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
  font-size: 1rem;
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

.delete-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #dc2626;
  background: white;
  border: 1px solid #fecaca;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn svg {
  width: 14px;
  height: 14px;
}

.delete-btn:hover {
  background: #fef2f2;
  border-color: #dc2626;
}

/* Responsive */
@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }

  .clear-btn {
    justify-content: center;
  }

  .channel-item {
    flex-wrap: wrap;
  }

  .delete-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
