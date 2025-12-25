/**
 * @파일명 locale.js
 * @설명 다국어(i18n) 지원 스토어
 * @기능
 *   - 한국어/영어 언어 전환
 *   - 번역 텍스트 조회 (t 함수)
 *   - 언어 설정 localStorage 저장
 * @사용법
 *   - t('nav.products') → '금융상품' (한국어) / 'Products' (영어)
 *   - toggleLocale() → 언어 전환
 * @저장 localStorage에 'locale' 키로 저장
 */

import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

// ========================================
// 번역 데이터 (Translations)
// ========================================
const translations = {
  ko: {
    // Navigation
    nav: {
      products: '금융상품',
      analysis: 'AI 분석',
      news: '뉴스',
      youtube: '유튜브',
      metals: '현물',
      bankFinder: '은행찾기',
      community: '커뮤니티',
      login: '로그인',
      logout: '로그아웃',
      signup: '회원가입',
      mypage: '마이페이지'
    },
    // Home
    home: {
      hero: {
        title: 'AI가 분석하는\n나만의 맞춤 금융',
        subtitle: '복잡한 금융 상품, 이제 F!NK가 당신에게 딱 맞는 상품을 찾아드립니다',
        cta: 'AI 분석 시작하기',
        ctaSecondary: '상품 둘러보기'
      },
      features: {
        title: '스마트한 자산관리의 시작',
        subtitle: 'F!NK만의 특별한 기능들'
      },
      stats: {
        users: '누적 사용자',
        products: '분석 상품',
        satisfaction: '만족도'
      }
    },
    // Products
    products: {
      title: '금융상품',
      subtitle: '예금 · 적금 상품을 비교해보세요',
      deposit: '예금',
      saving: '적금',
      all: '전체',
      bank: '은행',
      search: '검색',
      searchPlaceholder: '상품명 검색...',
      sortBy: '정렬',
      sortOptions: {
        rate: '금리순',
        name: '이름순'
      },
      rate: '금리',
      baseRate: '기본금리',
      maxRate: '최고금리',
      period: '기간',
      months: '개월',
      findBank: '은행 위치 찾기',
      noResults: '검색 결과가 없습니다',
      loading: '상품을 불러오는 중...'
    },
    // Analysis
    analysis: {
      title: 'AI 금융 분석',
      subtitle: '당신에게 맞는 최적의 금융 상품을 찾아드립니다',
      startAnalysis: '분석 시작하기',
      purpose: '목적',
      purposeOptions: {
        housing: '주거 마련',
        savings: '저축/투자',
        retirement: '노후 준비',
        travel: '여행'
      },
      period: '기간',
      amount: '목표 금액',
      result: '분석 결과',
      recommended: '추천 상품',
      retry: '다시 분석하기'
    },
    // News
    news: {
      title: '금융 뉴스',
      subtitle: '최신 금융 소식을 확인하세요',
      bookmark: '북마크',
      bookmarked: '북마크됨',
      share: '공유',
      noNews: '뉴스가 없습니다',
      loading: '뉴스를 불러오는 중...'
    },
    // YouTube
    youtube: {
      title: '금융 유튜브',
      subtitle: '금융 전문가들의 영상을 만나보세요',
      search: '검색',
      searchPlaceholder: '검색어를 입력하세요',
      saved: '저장된 영상',
      channels: '채널',
      noResults: '검색 결과가 없습니다',
      loading: '영상을 불러오는 중...'
    },
    // Metals
    metals: {
      title: '현물 시세',
      subtitle: '금/은 실시간 시세를 확인하세요',
      gold: '금',
      silver: '은',
      price: '가격',
      change: '변동',
      period: {
        day: '1일',
        week: '1주',
        month: '1개월',
        month3: '3개월',
        month6: '6개월',
        year: '1년'
      },
      highPrice: '최고가',
      lowPrice: '최저가',
      avgPrice: '평균가',
      loading: '시세를 불러오는 중...'
    },
    // Bank Finder
    bankFinder: {
      title: '은행 찾기',
      subtitle: '가까운 은행 지점을 검색해보세요',
      origin: '출발지',
      originPlaceholder: '출발지 검색',
      currentLocation: '현재 위치로 설정',
      region: '지역 선택',
      city: '광역시/도 선택',
      district: '시/군/구 선택',
      bank: '은행 선택',
      selectBank: '은행을 선택하세요',
      search: '은행 찾기',
      results: '검색 결과',
      distance: '거리',
      info: '지도를 클릭하면 해당 위치의 상세 정보를 확인할 수 있습니다.'
    },
    // Community
    community: {
      title: '커뮤니티',
      subtitle: '금융 정보를 나눠보세요',
      write: '글쓰기',
      writeTitle: '제목',
      writeContent: '내용',
      titlePlaceholder: '제목을 입력하세요',
      contentPlaceholder: '내용을 입력하세요',
      submit: '등록',
      cancel: '취소',
      edit: '수정',
      delete: '삭제',
      like: '좋아요',
      views: '조회',
      comments: '댓글',
      noComments: '댓글이 없습니다',
      writeComment: '댓글을 입력하세요',
      submitComment: '등록',
      noPosts: '게시글이 없습니다'
    },
    // Profile
    profile: {
      title: '마이페이지',
      info: '내 정보',
      nickname: '닉네임',
      email: '이메일',
      age: '나이',
      income: '연소득',
      assets: '자산',
      edit: '수정',
      save: '저장',
      myProducts: '내 상품',
      wishlist: '관심상품',
      noProducts: '관심 상품이 없습니다',
      savedVideos: '저장된 영상',
      noVideos: '저장된 영상이 없습니다'
    },
    // Auth
    auth: {
      login: '로그인',
      signup: '회원가입',
      username: '아이디',
      password: '비밀번호',
      passwordConfirm: '비밀번호 확인',
      email: '이메일',
      nickname: '닉네임',
      loginBtn: '로그인',
      signupBtn: '회원가입',
      noAccount: '계정이 없으신가요?',
      hasAccount: '이미 계정이 있으신가요?',
      goToSignup: '회원가입하기',
      goToLogin: '로그인하기'
    },
    // Common
    common: {
      loading: '로딩 중...',
      error: '오류가 발생했습니다',
      retry: '다시 시도',
      confirm: '확인',
      cancel: '취소',
      save: '저장',
      delete: '삭제',
      edit: '수정',
      back: '뒤로',
      more: '더보기',
      close: '닫기',
      search: '검색',
      noData: '데이터가 없습니다',
      unit: {
        won: '원',
        percent: '%',
        year: '년',
        month: '개월'
      }
    },
    // Settings
    settings: {
      theme: '테마',
      darkMode: '다크 모드',
      lightMode: '라이트 모드',
      language: '언어',
      korean: '한국어',
      english: 'English'
    },
    // Footer
    footer: {
      tagline: '당신의 금융을 더 스마트하게',
      terms: '이용약관',
      privacy: '개인정보처리방침',
      support: '고객센터',
      copyright: '© 2024 F!NK. All rights reserved.'
    }
  },
  en: {
    // Navigation
    nav: {
      products: 'Products',
      analysis: 'AI Analysis',
      news: 'News',
      youtube: 'YouTube',
      metals: 'Metals',
      bankFinder: 'Find Bank',
      community: 'Community',
      login: 'Login',
      logout: 'Logout',
      signup: 'Sign Up',
      mypage: 'My Page'
    },
    // Home
    home: {
      hero: {
        title: 'AI-Powered\nPersonalized Finance',
        subtitle: 'F!NK finds the perfect financial products tailored just for you',
        cta: 'Start AI Analysis',
        ctaSecondary: 'Browse Products'
      },
      features: {
        title: 'Smart Asset Management',
        subtitle: 'Exclusive Features of F!NK'
      },
      stats: {
        users: 'Total Users',
        products: 'Analyzed Products',
        satisfaction: 'Satisfaction'
      }
    },
    // Products
    products: {
      title: 'Financial Products',
      subtitle: 'Compare deposits and savings products',
      deposit: 'Deposit',
      saving: 'Saving',
      all: 'All',
      bank: 'Bank',
      search: 'Search',
      searchPlaceholder: 'Search products...',
      sortBy: 'Sort by',
      sortOptions: {
        rate: 'Interest Rate',
        name: 'Name'
      },
      rate: 'Rate',
      baseRate: 'Base Rate',
      maxRate: 'Max Rate',
      period: 'Period',
      months: 'months',
      findBank: 'Find Bank Location',
      noResults: 'No results found',
      loading: 'Loading products...'
    },
    // Analysis
    analysis: {
      title: 'AI Financial Analysis',
      subtitle: 'Find the optimal financial products for you',
      startAnalysis: 'Start Analysis',
      purpose: 'Purpose',
      purposeOptions: {
        housing: 'Housing',
        savings: 'Savings/Investment',
        retirement: 'Retirement',
        travel: 'Travel'
      },
      period: 'Period',
      amount: 'Target Amount',
      result: 'Analysis Result',
      recommended: 'Recommended',
      retry: 'Try Again'
    },
    // News
    news: {
      title: 'Financial News',
      subtitle: 'Stay updated with the latest financial news',
      bookmark: 'Bookmark',
      bookmarked: 'Bookmarked',
      share: 'Share',
      noNews: 'No news available',
      loading: 'Loading news...'
    },
    // YouTube
    youtube: {
      title: 'Finance YouTube',
      subtitle: 'Watch videos from financial experts',
      search: 'Search',
      searchPlaceholder: 'Enter search keyword',
      saved: 'Saved Videos',
      channels: 'Channels',
      noResults: 'No results found',
      loading: 'Loading videos...'
    },
    // Metals
    metals: {
      title: 'Metal Prices',
      subtitle: 'Check real-time gold/silver prices',
      gold: 'Gold',
      silver: 'Silver',
      price: 'Price',
      change: 'Change',
      period: {
        day: '1D',
        week: '1W',
        month: '1M',
        month3: '3M',
        month6: '6M',
        year: '1Y'
      },
      highPrice: 'High',
      lowPrice: 'Low',
      avgPrice: 'Average',
      loading: 'Loading prices...'
    },
    // Bank Finder
    bankFinder: {
      title: 'Find Bank',
      subtitle: 'Search for nearby bank branches',
      origin: 'Origin',
      originPlaceholder: 'Search origin',
      currentLocation: 'Use Current Location',
      region: 'Select Region',
      city: 'Select City/Province',
      district: 'Select District',
      bank: 'Select Bank',
      selectBank: 'Choose a bank',
      search: 'Find Bank',
      results: 'Search Results',
      distance: 'Distance',
      info: 'Click on the map to see detailed location information.'
    },
    // Community
    community: {
      title: 'Community',
      subtitle: 'Share financial information',
      write: 'Write',
      writeTitle: 'Title',
      writeContent: 'Content',
      titlePlaceholder: 'Enter title',
      contentPlaceholder: 'Enter content',
      submit: 'Submit',
      cancel: 'Cancel',
      edit: 'Edit',
      delete: 'Delete',
      like: 'Like',
      views: 'Views',
      comments: 'Comments',
      noComments: 'No comments',
      writeComment: 'Write a comment',
      submitComment: 'Submit',
      noPosts: 'No posts available'
    },
    // Profile
    profile: {
      title: 'My Page',
      info: 'My Info',
      nickname: 'Nickname',
      email: 'Email',
      age: 'Age',
      income: 'Annual Income',
      assets: 'Assets',
      edit: 'Edit',
      save: 'Save',
      myProducts: 'My Products',
      wishlist: 'Wishlist',
      noProducts: 'No products in wishlist',
      savedVideos: 'Saved Videos',
      noVideos: 'No saved videos'
    },
    // Auth
    auth: {
      login: 'Login',
      signup: 'Sign Up',
      username: 'Username',
      password: 'Password',
      passwordConfirm: 'Confirm Password',
      email: 'Email',
      nickname: 'Nickname',
      loginBtn: 'Login',
      signupBtn: 'Sign Up',
      noAccount: "Don't have an account?",
      hasAccount: 'Already have an account?',
      goToSignup: 'Sign up',
      goToLogin: 'Login'
    },
    // Common
    common: {
      loading: 'Loading...',
      error: 'An error occurred',
      retry: 'Retry',
      confirm: 'Confirm',
      cancel: 'Cancel',
      save: 'Save',
      delete: 'Delete',
      edit: 'Edit',
      back: 'Back',
      more: 'More',
      close: 'Close',
      search: 'Search',
      noData: 'No data available',
      unit: {
        won: 'KRW',
        percent: '%',
        year: 'years',
        month: 'months'
      }
    },
    // Settings
    settings: {
      theme: 'Theme',
      darkMode: 'Dark Mode',
      lightMode: 'Light Mode',
      language: 'Language',
      korean: '한국어',
      english: 'English'
    },
    // Footer
    footer: {
      tagline: 'Making your finances smarter',
      terms: 'Terms of Service',
      privacy: 'Privacy Policy',
      support: 'Support',
      copyright: '© 2024 F!NK. All rights reserved.'
    }
  }
}

export const useLocaleStore = defineStore('locale', () => {
  // 저장된 언어 불러오기 또는 브라우저 언어 확인
  const getInitialLocale = () => {
    const saved = localStorage.getItem('locale')
    if (saved) return saved
    const browserLang = navigator.language.toLowerCase()
    return browserLang.startsWith('ko') ? 'ko' : 'en'
  }

  const locale = ref(getInitialLocale())
  const isKorean = computed(() => locale.value === 'ko')

  // 언어 토글
  const toggleLocale = () => {
    locale.value = locale.value === 'ko' ? 'en' : 'ko'
  }

  // 특정 언어로 설정
  const setLocale = (newLocale) => {
    locale.value = newLocale
  }

  // 번역 텍스트 가져오기
  const t = (key) => {
    const keys = key.split('.')
    let result = translations[locale.value]
    for (const k of keys) {
      if (result && result[k]) {
        result = result[k]
      } else {
        // 키가 없으면 한국어로 폴백
        result = translations['ko']
        for (const k of keys) {
          if (result && result[k]) {
            result = result[k]
          } else {
            return key // 그래도 없으면 키 반환
          }
        }
        break
      }
    }
    return result
  }

  // 언어 변경 시 localStorage 업데이트
  watch(locale, (newLocale) => {
    localStorage.setItem('locale', newLocale)
    document.documentElement.setAttribute('lang', newLocale)
  }, { immediate: true })

  return {
    locale,
    isKorean,
    toggleLocale,
    setLocale,
    t
  }
})
