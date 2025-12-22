<template>
  <div class="product-detail">
    <h1>금융 상품 상세 정보</h1>

    <div v-if="product">
      <p>은행 : {{ product.kor_co_nm }}</p>
      <p>상품명 : {{ product.fin_prdt_nm }}</p>
      <p>가입 제한 여부 : {{ joinDenyText }}</p>
      <p>가입 대상 : {{ product.join_member }}</p>
      <p>가입 방법 : {{ product.join_way }}</p>
      <p>우대조건 : {{ product.spcl_cnd }}</p>
      <p>기타 사항 : {{ product.etc_note }}</p>
    </div>

    <div v-if="options.length">
      <h3>옵션</h3>
      <table>
        <thead>
          <tr>
            <th>기간</th><th>금리유형</th><th>기본</th><th>최고</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="option in options" :key="option.id">
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ✅ 좋아요 영역 (community랑 같은 스타일: ❤️/🤍 + count) -->
    <div class="action-buttons">
      <button
        @click="toggleLike"
        class="like-btn"
        :class="{ liked: likeStore.liked }"
        type="button"
      >
        {{ likeStore.liked ? '❤️' : '🤍' }}
        좋아요 {{ likeStore.likesCount ?? 0 }}
      </button>

      <!-- 좋아요 상태일 때만 지도 버튼 노출 (기존 로직 유지) -->
      <button
        v-if="likeStore.liked && product"
        @click="toggleMap"
        class="map-btn"
        type="button"
      >
        {{ showMap ? '🗺️ 지도 닫기' : '🗺️ 은행 위치 찾기' }}
      </button>
    </div>

    <!-- 좋아요 상태일 때만 지도 표시 -->
    <ProductBankMap
      v-if="showMap && product"
      :bank-name="product.kor_co_nm"
      @close="showMap = false"
    />

    <hr>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { useLikeStore } from '@/stores/like'   // ✅ wishlist → like로 변경
import { useAccountStore } from '@/stores/accounts'
import ProductBankMap from '@/components/products/ProductBankMap.vue'

const store = useProductStore()
const likeStore = useLikeStore()              // ✅ wishlistStore → likeStore
const accountStore = useAccountStore()
const route = useRoute()

const product = ref(null)
const options = ref([])
const showMap = ref(false)

const joinDenyText = computed(() => {
  if (!product.value) return ''
  const map = { 1: '제한 없음', 2: '서민 전용', 3: '일부 제한' }
  return map[product.value.join_deny]
})

// ✅ 좋아요 버튼 클릭
const toggleLike = function () {
  const payload = {
    fin_prdt_cd: route.params.fin_prdt_cd,
    product_type: route.params.type, // deposit / saving
  }

  // ✅ then/catch 스타일로 동일하게
  likeStore.toggleLike(payload)
    .then(() => {})
    .catch((err) => {
      console.log(err)
      alert('좋아요 처리에 실패했습니다.')
    })
}

// 지도 토글
const toggleMap = () => {
  showMap.value = !showMap.value
}

// ✅ 좋아요 취소 시 지도 닫기
watch(() => likeStore.liked, (newVal) => {
  if (!newVal) showMap.value = false
})

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/products/${route.params.type}/${route.params.fin_prdt_cd}/`,
    headers: accountStore.token ? { Authorization: `Token ${accountStore.token}` } : {},
  })
    .then((res) => {
      product.value = res.data
      options.value = res.data.options

      // ✅ 서버 응답 필드명이 is_liked/likes_count 인지 liked/likes_count 인지 프로젝트마다 달라서 둘 다 대응
      likeStore.liked = res.data.is_liked ?? res.data.liked ?? false
      likeStore.likesCount = res.data.likes_count ?? 0
    })
    .catch((err) => console.log(err))
})
</script>

<style scoped>
/* 기존 스타일 그대로 + 버튼 텍스트만 동일 패턴으로 사용 */
.product-detail { max-width: 900px; margin: 0 auto; padding: 20px; }
.product-detail h1 { color: #333; border-bottom: 2px solid #e67e57; padding-bottom: 10px; }
.product-detail table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.product-detail th, .product-detail td { border: 1px solid #ddd; padding: 10px; text-align: center; }
.product-detail th { background: #f5f5f5; }

.action-buttons { display: flex; gap: 12px; margin: 20px 0; }

.like-btn {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  border: 2px solid #e67e57;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
  color: #e67e57;
}
.like-btn:hover { background: #fff5f2; }
.like-btn.liked { background: #e67e57; color: white; }

.map-btn {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  border: 2px solid #4A90E2;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  background: #4A90E2;
  color: white;
}
.map-btn:hover { background: #357ABD; }
</style>
