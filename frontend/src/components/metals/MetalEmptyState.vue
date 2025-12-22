<template>
  <div class="empty-state">
    <div class="empty-card">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 6v6l4 2"/>
        </svg>
      </div>
      <p class="empty-title">데이터가 없습니다</p>
      <span class="empty-text">{{ message || '조건에 해당하는 데이터가 없습니다.' }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: String,
})
</script>

<style scoped>
.empty-state {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.empty-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 40px;
  text-align: center;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  max-width: 400px;
}

.empty-icon {
  width: 72px;
  height: 72px;
  background: #fef3c7;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.empty-icon svg {
  width: 36px;
  height: 36px;
  color: #f59e0b;
}

.empty-title {
  font-size: 1.0625rem;
  font-weight: 600;
  color: #18181b;
  margin: 0 0 8px;
}

.empty-text {
  font-size: 0.875rem;
  color: #71717a;
  line-height: 1.5;
}
</style>
