<template>
  <div>
    <h1>금융 상품 상세 정보</h1>
    <div v-if="product">
      <p>은행 : {{ product.kor_co_nm }}</p>
      <p>상품명 : {{ product.fin_prdt_nm  }}</p>
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
  </div>
  <div>
    <button @click="toggleLike">
      {{ wishlistStore.liked ? '좋아요 취소' : '좋아요' }}
    </button>
  </div>
  <hr>
</template>

<script setup>
  import axios from 'axios';
  import { onMounted, ref, computed } from 'vue';
  import { useRoute } from 'vue-router';
  import { useProductStore } from '@/stores/products';
  import { useWishlistStore } from '@/stores/wishlist';
import { useAccountStore } from '@/stores/accounts';

  const store = useProductStore()
  const wishlistStore = useWishlistStore()
  const accountStore = useAccountStore()
  const route = useRoute()

  const product = ref(null)
  const options = ref([])

  // 가입 제한 텍스트 변경
  const joinDenyText = computed(() => {
    if (!product.value)
      return ''
    const map = {
      1: '제한 없음',
      2: '서민 전용',
      3: '일부 제한',
    }

    return map[product.value.join_deny]
  })

  // 좋아요 버튼 클릭 함수
  const toggleLike = function () {
    const payload = {
      fin_prdt_cd: route.params.fin_prdt_cd,
      product_type: route.params.type,
    }
    wishlistStore.toggleWishlist(payload)
  }

  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/products/${route.params.type}/${route.params.fin_prdt_cd}/`,
      headers: accountStore.token ? { 'Authorization': `Token ${accountStore.token}` } : {} 
    })
    .then(res => {
      product.value = res.data
      options.value = res.data.options
      wishlistStore.liked = res.data.liked
    })
    .catch(err => console.log(err))
  })
</script>

<style scoped>

</style>