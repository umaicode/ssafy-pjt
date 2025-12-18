<template>
  <div>
    <!-- =========================
      1) 예금/적금 탭(수업시간에 배운 버튼 + ref)
    ========================== -->
    <div class="tab">
      <button @click="active = 'deposits'">예금</button>
      <button @click="active = 'savings'">적금</button>
    </div>

    <!-- =========================
      2) 검색바(필터 폼)
      - 은행 선택, 기간 선택, 키워드 검색(상품명 등)
      - v-model 로 입력값을 상태로 저장
    ========================== -->
    <div class="search-bar">
      <!-- 은행 필터 -->
      <label>
        은행:
        <select v-model="selectedBank">
          <option value="">전체</option>
          <!-- 은행 옵션은 computed로 "현재 active 목록"에서 뽑아냄 -->
          <option v-for="bank in bankOptions" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </label>

      <!-- 기간 필터 -->
      <label>
        기간(개월):
        <select v-model.number="selectedTerm">
          <option :value="0">전체</option>
          <!-- 기간 옵션도 마찬가지로 현재 active 목록에서 뽑아냄 -->
          <option v-for="t in termOptions" :key="t" :value="t">
            {{ t }}개월
          </option>
        </select>
      </label>

      <!-- 키워드 검색(검색바) -->
      <label>
        검색:
        <input
          v-model.trim="keyword"
          type="text"
          placeholder="상품명 등 키워드 입력"
        />
      </label>

      <!-- 필터 초기화 버튼 -->
      <button @click="resetFilter">초기화</button>
    </div>

    <!-- =========================
      3) 결과 리스트 출력
      - 무조건 computed로 만든 filteredItems를 ProductList에 전달
    ========================== -->
    <ProductList :items="filteredItems" />
  </div>
</template>

<script setup>
/*
  목표:
  - active: 예금/적금 선택
  - selectedBank: 은행 필터
  - selectedTerm: 기간 필터
  - keyword: 검색바 키워드
  - filteredItems: 위 조건으로 걸러낸 결과(computed)
*/

import { onMounted, ref, computed } from 'vue'
import { useProductStore } from '@/stores/products'
import ProductList from '@/components/ProductList.vue'

const store = useProductStore()

// 현재 선택 탭: 'deposits' or 'savings'
const active = ref('deposits')

// 필터 상태들
const selectedBank = ref('')   // '' 이면 전체
const selectedTerm = ref(0)    // 0 이면 전체
const keyword = ref('')        // '' 이면 키워드 필터 없음

onMounted(() => {
  // 처음 로딩 시 원본 데이터 가져오기
  store.getDeposits()
  store.getSavings()
})

/* -----------------------------------
  1) 현재 active에 해당하는 "원본 목록" 선택
  - 예금이면 store.deposits, 적금이면 store.savings
----------------------------------- */
const currentItems = computed(() => {
  return active.value === 'deposits' ? store.deposits : store.savings
})

/* -----------------------------------
  2) 은행 옵션 목록 만들기(중복 제거)
  - 수업에서 배운: map + Set + 배열로 변환
  - bank 이름 필드는 너희 API/데이터에 맞게 수정 필요
    예: item.kor_co_nm / item.bankName 등
----------------------------------- */
const bankOptions = computed(() => {
  const banks = currentItems.value.map((item) => item.kor_co_nm) // ✅ 여기 필드명 확인!
  return [...new Set(banks)].filter(Boolean)
})

/* -----------------------------------
  3) 기간 옵션 목록 만들기(중복 제거)
  - 기간 필드도 데이터에 맞게 수정 필요
    예: item.save_trm (문자열 "12") / item.term 등
----------------------------------- */
const termOptions = computed(() => {
  const terms = currentItems.value
    .map((item) => Number(item.save_trm)) // ✅ 여기 필드명 확인!
    .filter((n) => !Number.isNaN(n))

  // 오름차순 정렬(보기 좋게)
  return [...new Set(terms)].sort((a, b) => a - b)
})

/* -----------------------------------
  4) 핵심: 필터링 결과 (computed)
  - 조건을 하나씩 적용하면서 걸러냄
----------------------------------- */
const filteredItems = computed(() => {
  let result = currentItems.value

  // (1) 은행 필터
  if (selectedBank.value) {
    result = result.filter((item) => item.kor_co_nm === selectedBank.value) // ✅ 필드명 확인!
  }

  // (2) 기간 필터
  if (selectedTerm.value !== 0) {
    result = result.filter((item) => Number(item.options.save_trm) === selectedTerm.value) // ✅ 필드명 확인!
  }

  // (3) 키워드 검색 (상품명 등에 포함되는지)
  // - includes로 간단히 처리(수업 난이도)
  if (keyword.value) {
    const k = keyword.value.toLowerCase()
    result = result.filter((item) => {
      const name = (item.fin_prdt_nm || '').toLowerCase() // ✅ 상품명 필드 확인! 
      return name.includes(k)
    })
  }

  return result
})

/* -----------------------------------
  5) 초기화 함수
----------------------------------- */
const resetFilter = () => {
  selectedBank.value = ''
  selectedTerm.value = 0
  keyword.value = ''
}
</script>

<style scoped>
.tab {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 16px;
}

.search-bar input {
  padding: 6px 10px;
}
</style>
