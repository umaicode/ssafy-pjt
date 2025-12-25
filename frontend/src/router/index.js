/**
 * @파일명 router/index.js
 * @설명 Vue Router 설정 파일
 * 
 * @라우트구조
 *   - / : 홈 (HomeView)
 *   - /signup, /login : 인증
 *   - /products : 금융 상품 목록/상세
 *   - /profile/* : 프로필 (인증 필요)
 *   - /analysis/* : AI 분석 (인증 필요)
 *   - /kakaomap : 카카오맵
 *   - /news : 뉴스
 *   - /youtube/* : 유튜브
 *   - /metals : 금/은 시세
 *   - /stocks : 주식
 *   - /community/* : 커뮤니티
 * 
 * @네비게이션가드
 *   - requiresAuth: true인 라우트는 로그인 필요
 */

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
import ProfileView from '@/views/profile/ProfileView.vue'
import ProfileModify from '@/views/profile/ProfileModify.vue'
import ProfileMyProduct from '@/views/profile/ProfileMyProduct.vue'
import ProfileWishlist from '@/views/profile/ProfileWishlist.vue'

// 카카오맵
import KakaoMapView from '@/views/kakaomap/KakaoMapView.vue'

// NEWS
import NewsView from '@/views/news/NewsView.vue'

// Youtube
import YoutubeChannelsView from '@/views/youtube/YoutubeChannelsView.vue'
import YoutubeSavedView from '@/views/youtube/YoutubeSavedView.vue'
import YoutubeSearchView from '@/views/youtube/YoutubeSearchView.vue'
import YoutubeVideoDetailView from '@/views/youtube/YoutubeVideoDetailView.vue'
import YoutubeSavedLayoutView from '@/views/youtube/YoutubeSavedLayoutView.vue'
import MetalView from '@/views/MetalView.vue'
import StockView from '@/views/StockView.vue'

// 커뮤니티
import CommunityView from '@/views/community/CommunityView.vue'
import CommunityCreateView from '@/views/community/CommunityCreateView.vue'
import CommunityDetailView from '@/views/community/CommunityDetailView.vue'

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
      meta: { requiresAuth: true },
      redirect: '/profile/myproduct',
      children: [
        { path: 'myproduct', name: 'ProfileMyProduct', component: ProfileMyProduct },
        { path: 'wishlist', name: 'ProfileWishlist', component: ProfileWishlist },
        { path: 'modify', name: 'ProfileModify', component: ProfileModify },
      ],
    },
    {
      path: '/analysis',
      name: 'AnalysisView',
      meta: { requiresAuth: true },
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
      meta: { requiresAuth: true },
      component: NewsView,
    },
    // Youtube
    {
      path: '/youtube',
      name: 'YoutubeSearchView',
      component: YoutubeSearchView,
    },
    {
      path: '/youtube/saved',
      name: 'YoutubeSavedLayoutView',
      component: YoutubeSavedLayoutView,
      meta: { requiresAuth: true },
      redirect: {name: 'YoutubeSavedView'},
      children: [
        {
          path: 'videos',
          name: 'YoutubeSavedView',
          component: YoutubeSavedView,
        },
        {
          path: 'channels',
          name: 'YoutubeChannelsView',
          component: YoutubeChannelsView,
        }
      ]
    },
    {
      path: '/youtube/video/:id',
      name: 'YoutubeVideoDetailView',
      component: YoutubeVideoDetailView,
      props: true,
    },
    // 금/은
    {
      path: '/metals',
      name: 'MetalView',
      component: MetalView,
    },
    // 주식
    {
      path: '/stocks',
      name: 'StockView',
      component: StockView,
    },
    // 커뮤니티
    { path: '/community', name: 'CommunityView', component: CommunityView },
    { path: '/community/create', name: 'CreateView', component: CommunityCreateView },
    { path: '/community/:id', name: 'DetailView', component: CommunityDetailView, props: true },
  ],
})

// 인증된 사용자는 회원가입과 로그인 페이지에 접근 제한
router.beforeEach((to) => {
  const accountStore = useAccountStore()

  if (to.matched.some(record => record.meta.requiresAuth) && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }
})

export default router
