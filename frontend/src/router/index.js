import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProductView from '@/views/ProductView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
// import ProfileView from '@/views/ProfileView.vue'

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
    }
    // {
    //   path: '/user/:nickname',
    //   name: 'ProfileView',
    //   component: ProfileView,
    // },
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
})

export default router
