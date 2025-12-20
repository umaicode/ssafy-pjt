<template>
  <div class="empty">
    {{ message || '조건에 해당하는 데이터가 없습니다.' }}
  </div>
</template>

<script setup>
defineProps({
  message: String,
})
</script>

<style scoped>
.empty {
  padding: 20px;
  color: #666;
  text-align: center;
}
</style>
