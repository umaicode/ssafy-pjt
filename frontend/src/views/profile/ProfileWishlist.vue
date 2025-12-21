<template>
  <div>
    <h3>좋아요 목록</h3>

    <div class="tabs">
      <button
        class="tab"
        :class="{ active: activeTab === 'products' }"
        @click="activeTab = 'products'"
        type="button"
      >
        금융상품
      </button>

      <button
        class="tab"
        :class="{ active: activeTab === 'news' }"
        @click="activeTab = 'news'"
        type="button"
      >
        뉴스
      </button>

      <button
        class="tab"
        :class="{ active: activeTab === 'youtube' }"
        @click="activeTab = 'youtube'"
        type="button"
      >
        유튜브
      </button>
    </div>

    <!-- 1) ✅ 금융상품 좋아요 -->
    <section v-if="activeTab === 'products'">
      <p v-if="!wishlistStore.wishlist.length">아직 좋아요한 상품이 없어요.</p>

      <div v-else>
        <ProductListItem
          v-for="item in wishlistStore.wishlist"
          :key="item.product_type + '_' + item.fin_prdt_cd"
          :product="item"
          :type="item.product_type"
        />
      </div>
    </section>

    <section v-else-if="activeTab === 'news'" class="panel">
      <div class="news-two-col">
        <NewsList />
        <NewsDetail />
      </div>
    </section>

    <!-- 3) ✅ 유튜브 저장됨 레이아웃 -->
    <section v-else class="panel">
      <YoutubeSavedLayoutView />
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'

import { useWishlistStore } from '@/stores/wishlist'
import ProductListItem from '@/components/products/ProductListItem.vue'

import { useNewsStore } from '@/stores/news'
import NewsList from '@/components/news/NewsList.vue'
import NewsDetail from '@/components/news/NewsDetail.vue'

import YoutubeSavedLayoutView from '@/views/youtube/YoutubeSavedLayoutView.vue'


const wishlistStore = useWishlistStore()
const newsStore = useNewsStore()

// ✅ 첫 탭이 기본
const activeTab = ref('products')

onMounted(() => {
  // 첫번째 탭(상품) 들어왔을 때 목록 불러오기
  wishlistStore.getWishlist()
})

// ✅ 탭 전환 시 필요한 데이터만 로드 (lazy load)
watch(activeTab, (tab) => {
  if (tab === 'news') {
    // NewsBookmarkView와 같은 효과: bookmark 모드로 바꾸고 목록 로드
    // ⚠️ mode가 ref면 직접 대입하지 말고(이전에 오류 났던 포인트)
    // store에 setModeOnly가 있다면 그걸 쓰는 게 안전
    if (typeof newsStore.setModeOnly === 'function') {
      newsStore.setModeOnly('bookmark')
    } else {
      // setModeOnly 없으면 setMode를 사용(로그인 체크 포함)
      newsStore.setMode('bookmark')
      return
    }

    newsStore.clearDetail()
    newsStore.getNewsList()
  }

  // 유튜브 탭은 YoutubeSavedLayoutView 내부 로직에 맡김
})
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 8px;
  margin: 12px 0 16px;
}

.tab {
  padding: 8px 14px;
  border: 1px solid #ccc;
  border-radius: 18px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
}

.tab.active {
  background: #f5dfdf;
  color: #0a0a0a;
  border-color: #333;
}

.panel {
  margin-top: 10px;
}
.news-two-col {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 14px;
  height: 70vh;
}

</style>
