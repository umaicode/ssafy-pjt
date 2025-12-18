<template>
    <div>
        <!-- 1) 탭 -->
        <div class="tab">
            <button @click="active = 'deposits'">예금</button>
            <button @click="active = 'savings'">적금</button>
        </div>

        <!-- 2) 필터/검색 -->
        <div class="search-bar">
            <!-- 은행 -->
            <label>
                은행:
                <select v-model="selectedBank">
                    <option value="">전체</option>
                    <option v-for="bank in bankOptions" :key="bank" :value="bank">
                        {{ bank }}
                    </option>
                </select>
            </label>

            <!-- 기간 -->
            <label>
                기간(개월):
                <select v-model.number="selectedTerm">
                    <option :value="0">전체</option>
                    <option v-for=" term in termOptions" :key="term" :value="term">
                        {{ term }}개월
                    </option>
                </select>
            </label>

            <!-- 키워드 -->
            <label>
                검색:
                <input v-model.trim="keyword" type="text" placeholder="은행명,상품명 키워드" />
            </label>

            <button @click="resetFilter">초기화</button>
        </div>

        <!-- 3) 리스트 (기존 방식 유지: type을 꼭 넘긴다) -->
        <ProductList v-if="active === 'deposits'" :items="filteredItems" type="deposit" />
        <ProductList v-else :items="filteredItems" type="saving" />
    </div>
</template>

<script setup>
    import { onMounted, ref, computed } from 'vue'
    import { useProductStore } from '@/stores/products'
    import ProductList from '@/components/ProductList.vue'

    const store = useProductStore()
    const active = ref('deposits')

    // 필터 상태
    const selectedBank = ref('')
    const selectedTerm = ref(0)
    const keyword = ref('')

    onMounted(() => {
        store.getDeposits()
        store.getSavings()
    })

    // 현재 탭 원본 목록
    const currentItems = computed(() => {
        return active.value === 'deposits' ? store.deposits : store.savings
    })

    /** 옵션에서 기간 뽑기 (옵션 필드명이 save_trm이라고 가정) */
    const getTerm = (opt) => {
        const n = Number(opt?.save_trm)
        return Number.isNaN(n) ? null : n
    }

    // 은행 옵션(중복 제거)
    const bankOptions = computed(() => {
        const banks = currentItems.value.map(item => item.kor_co_nm).filter(Boolean)
        return [...new Set(banks)]
    })

    // 기간 옵션(중복 제거) - options 배열에서 뽑음
    const termOptions = computed(() => {
        const terms = currentItems.value
            .flatMap(item => (item.options ?? []).map(getTerm))
            .filter(n => n !== null)
        return [...new Set(terms)].sort((a, b) => a - b)
    })

    // 필터링 결과(상품 단위)
    const filteredItems = computed(() => {
        let result = currentItems.value

        // (1) 은행
        if (selectedBank.value) {
            result = result.filter(item => item.kor_co_nm === selectedBank.value)
        }

        // (2) 기간: options 중 하나라도 해당 기간이면 통과
        if (selectedTerm.value !== 0) {
            result = result.filter(item =>
                (item.options ?? []).some(opt => getTerm(opt) === selectedTerm.value)
            )
        }

        // (3) 키워드(상품명)
        if (keyword.value) {
            const k = keyword.value.toLowerCase()
            result = result.filter(item => {
                const productName = (item.fin_prdt_nm || '').toLowerCase()
                const companyName = (item.kor_co_nm || '').toLowerCase()

                return productName.includes(k) || companyName.includes(k)
            })
        }

        return result
    })

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
    flex-wrap: wrap;
}

.search-bar input {
    padding: 6px 10px;
}
</style>
