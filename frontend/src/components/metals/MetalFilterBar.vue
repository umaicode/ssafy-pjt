<template>
  <div class="filter-bar">
    <div class="filter-card">
      <!-- Date Range -->
      <div class="filter-group">
        <label class="filter-label">기간 설정</label>
        <div class="date-inputs">
          <div class="date-input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <input type="date" v-model="start" class="date-input" />
          </div>
          <span class="date-separator">~</span>
          <div class="date-input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <input type="date" v-model="end" class="date-input" />
          </div>
        </div>
      </div>

      <!-- Date Buttons -->
      <div class="filter-group">
        <div class="action-buttons">
          <button class="btn btn-primary" @click="applyDates">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            조회
          </button>
          <button class="btn btn-secondary" @click="store.resetDates">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
            </svg>
            전체
          </button>
        </div>
      </div>

      <!-- Metal Toggle -->
      <div class="filter-group">
        <label class="filter-label">귀금속 선택</label>
        <div class="metal-toggle">
          <button
            class="metal-btn"
            :class="{ active: store.metal === 'gold' }"
            @click="store.setMetal('gold')"
          >
            <span class="metal-icon gold">Au</span>
            금
          </button>

          <button
            class="metal-btn"
            :class="{ active: store.metal === 'silver' }"
            @click="store.setMetal('silver')"
          >
            <span class="metal-icon silver">Ag</span>
            은
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMetalsStore } from '@/stores/metals'

const store = useMetalsStore()

const start = ref(store.startDate)
const end = ref(store.endDate)

const applyDates = () => {
  store.setDates(start.value, end.value)
}
</script>

<style scoped>
.filter-bar {
  margin-bottom: 0;
}

.filter-card {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: flex-end;
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #71717a;
}

/* Date Inputs */
.date-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  width: 16px;
  height: 16px;
  color: #a1a1aa;
  pointer-events: none;
}

.date-input {
  padding: 12px 12px 12px 40px;
  font-size: 0.875rem;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.date-input:focus {
  outline: none;
  border-color: #f59e0b;
  box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.1);
}

.date-separator {
  font-size: 0.875rem;
  color: #71717a;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 8px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn svg {
  width: 16px;
  height: 16px;
}

.btn-primary {
  color: white;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(245, 158, 11, 0.35);
}

.btn-secondary {
  color: #52525b;
  background: white;
  border: 2px solid #e4e4e7;
}

.btn-secondary:hover {
  border-color: #f59e0b;
  color: #f59e0b;
}

/* Metal Toggle */
.metal-toggle {
  display: flex;
  gap: 8px;
}

.metal-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #52525b;
  background: white;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.metal-btn:hover {
  border-color: #d97706;
}

.metal-btn.active {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-color: #d97706;
  color: white;
}

.metal-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 800;
}

.metal-icon.gold {
  background: #fef3c7;
  color: #b45309;
}

.metal-btn.active .metal-icon.gold {
  background: rgba(255, 255, 255, 0.25);
  color: white;
}

.metal-icon.silver {
  background: #f4f4f5;
  color: #52525b;
}

.metal-btn.active .metal-icon.silver {
  background: rgba(255, 255, 255, 0.25);
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-card {
    flex-direction: column;
    align-items: stretch;
    gap: 20px;
    padding: 20px;
  }

  .date-inputs {
    flex-direction: column;
    align-items: stretch;
  }

  .date-separator {
    text-align: center;
  }

  .action-buttons {
    width: 100%;
  }

  .btn {
    flex: 1;
    justify-content: center;
  }

  .metal-toggle {
    width: 100%;
  }

  .metal-btn {
    flex: 1;
    justify-content: center;
  }
}

/* Dark Mode */
[data-theme="dark"] .filter-card {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .filter-label {
  color: #a1a1aa;
}

[data-theme="dark"] .date-input {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .date-input:focus {
  border-color: #f59e0b;
}

[data-theme="dark"] .date-separator {
  color: #a1a1aa;
}

[data-theme="dark"] .btn-secondary {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .btn-secondary:hover {
  border-color: #f59e0b;
  color: #f59e0b;
}

[data-theme="dark"] .metal-btn {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .metal-btn:hover {
  border-color: #d97706;
}

[data-theme="dark"] .metal-icon.gold {
  background: #422006;
  color: #fbbf24;
}

[data-theme="dark"] .metal-icon.silver {
  background: #27272a;
  color: #a1a1aa;
}
</style>
