import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProductView from '@/views/ProductView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'

import AnalysisView from '@/views/analysis/AnalysisView.vue'
import AnalysisResultView from '@/views/analysis/AnalysisResultView.vue'

// 프로필
import ProfileView from '@/views/ProfileView.vue'
import ProfileModify from '@/views/profile/ProfileModify.vue'
import ProfileMyProduct from '@/views/profile/ProfileMyProduct.vue'
import ProfileWishlist from '@/views/profile/ProfileWishlist.vue'

// 카카오맵
import KakaoMapView from '@/views/kakaomap/KakaoMapView.vue'

// NEWS
import NewsView from '@/views/news/NewsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView,
    },
    {
      path: '/products',
      name: 'ProductView',
      component: ProductView,
    },
    {
      path: '/products/:type/:fin_prdt_cd',
      name: 'ProductDetailView',
      component: ProductDetailView,
    },
    // 프로필페이지
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
      children: [
        // ✅ /mypage로 들어오면 첫 메뉴로 자동 이동
        { path: '', redirect: { name: 'ProfileMyProduct' } },

        { path: 'myproduct', name: 'ProfileMyProduct', component: ProfileMyProduct },
        { path: 'wishlist', name: 'ProfileWishlist', component: ProfileWishlist },
        { path: 'modify', name: 'ProfileModify', component: ProfileModify },
      ],
    },
        {
      path: '/analysis',
      name: 'AnalysisView',
      component: AnalysisView,
    },
    {
      path: '/analysis/:id/result',
      name: 'AnalysisResultView',
      component: AnalysisResultView,
      props: true,
    },
    {
      path: '/kakaomap',
      name: 'KakaoMapView',
      component: KakaoMapView,
    },
    //NEWS
    {
      path: '/news',
      name: 'NewsView',
      component: NewsView,
    },
    {
      path: '/news/bookmark',
      name: 'NewsBookmarkView',
      component: NewsView,
    },
  ],
})

// 인증된 사용자는 회원가입과 로그인 페이지에 접근 제한
router.beforeEach((to, from) => {
  const accountStore = useAccountStore()

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (accountStore.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    console.log('to:', to.name, 'isLogin:', accountStore.isLogin)

    return {name: 'home'}
  }

  if (to.name === 'NewsBookmarkView' && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return {name: 'LogInView'}
  }
})

export default router
