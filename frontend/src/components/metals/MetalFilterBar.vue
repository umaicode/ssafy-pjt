<template>
  <div class="filter">
    <input type="date" v-model="start" />
    <input type="date" v-model="end" />

    <button @click="applyDates">조회</button>
    <button @click="store.resetDates">전체</button>

    <button
      :class="{ active: store.metal === 'gold' }"
      @click="store.setMetal('gold')"
    >
      금
    </button>

    <button
      :class="{ active: store.metal === 'silver' }"
      @click="store.setMetal('silver')"
    >
      은
    </button>
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
.filter {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.active {
  font-weight: bold;
}
</style>
