import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from "axios";

export const useStocksStore = defineStore(
  "stocks",
  () => {
    const API_URL = "http://127.0.0.1:8000";

    // 토큰 가져오기 헬퍼 함수 (Pinia persist에서 가져오기)
    const getToken = () => {
      try {
        const stored = localStorage.getItem('account');
        if (stored) {
          const parsed = JSON.parse(stored);
          return parsed.token || null;
        }
        return null;
      } catch {
        return null;
      }
    };

    // State
    const popularStocks = ref([]);
    const stockList = ref([]);  // 종목 목록 (국내/해외/북마크)
    const krStocks = ref([]);   // 국내 주식 목록
    const usStocks = ref([]);   // 해외 주식 목록
    const bookmarkedStocks = ref([]);  // 북마크한 주식 목록
    const searchResults = ref([]);
    const selectedStock = ref(null);
    const chartData = ref(null);
    const stockNews = ref([]);
    const marketIndices = ref([]);  // 주요 지표 (나스닥, S&P500, 환율)

    const loading = ref(false);
    const listLoading = ref(false);
    const chartLoading = ref(false);
    const searchLoading = ref(false);
    const indicesLoading = ref(false);
    const bookmarkLoading = ref(false);
    const refreshLoading = ref(false);  // 갱신 중 상태
    const bookmarkRefreshLoading = ref(false);  // 북마크 갱신 중 상태
    const bookmarkRefreshTime = ref(null);  // 북마크 마지막 갱신 시간
    const errorMessage = ref(null);

    // 선택된 마켓 (BOOKMARK, KR, US)
    const selectedMarket = ref("KR");

    // 페이지네이션
    const currentPage = ref(1);
    const totalPages = ref(1);
    const totalCount = ref(0);
    const perPage = ref(20);  // 기본 페이지 크기

    // 갱신 상태
    const updateStatus = ref({
      KR: { last_updated: null, can_update: true, stock_count: 0 },
      US: { last_updated: null, can_update: true, stock_count: 0 },
    });

    // 차트 설정
    const chartPeriod = ref("1mo");
    const chartInterval = ref("1d");

    // Computed
    const filteredStocks = computed(() => {
      if (selectedMarket.value === "BOOKMARK") {
        return bookmarkedStocks.value;
      } else if (selectedMarket.value === "KR") {
        return krStocks.value;
      } else if (selectedMarket.value === "US") {
        return usStocks.value;
      }
      return stockList.value;
    });

    const hasSelectedStock = computed(() => selectedStock.value !== null);

    const hasChartData = computed(
      () => chartData.value && chartData.value.data?.length > 0
    );

    // Actions
    // 주요 지표 조회 (나스닥, S&P500, 환율 등)
    const fetchMarketIndices = async (period = '5d') => {
      indicesLoading.value = true;
      try {
        const response = await axios.get(`${API_URL}/api/stocks/indices/`, {
          params: { period }
        });
        marketIndices.value = response.data.indices || [];
      } catch (error) {
        console.error('주요 지표 로드 실패:', error);
        marketIndices.value = [];
      } finally {
        indicesLoading.value = false;
      }
    };

    // 갱신 상태 조회
    const fetchUpdateStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/stocks/update-status/`);
        updateStatus.value = response.data;
      } catch (error) {
        console.error('갱신 상태 조회 실패:', error);
      }
    };

    // 국내 주식 목록 조회 (DB에서, 페이지네이션)
    const fetchKrStocks = async (page = 1, size = 20) => {
      listLoading.value = true;
      errorMessage.value = null;

      try {
        const response = await axios.get(`${API_URL}/api/stocks/kr/`, {
          params: { page, size }
        });
        krStocks.value = response.data.stocks || [];
        
        if (selectedMarket.value === 'KR') {
          stockList.value = krStocks.value;
          totalCount.value = response.data.total_count || 0;
          totalPages.value = response.data.total_pages || 1;
          currentPage.value = response.data.page || 1;
        }
        
        // 데이터가 없으면 메시지 표시
        if (response.data.message) {
          errorMessage.value = response.data.message;
        }
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error ||
          "국내 주식 목록을 불러오는 중 오류가 발생했습니다.";
        krStocks.value = [];
      } finally {
        listLoading.value = false;
      }
    };

    // 해외 주식 목록 조회 (DB에서, 페이지네이션)
    const fetchUsStocks = async (page = 1, size = 20) => {
      listLoading.value = true;
      errorMessage.value = null;

      try {
        const response = await axios.get(`${API_URL}/api/stocks/us/`, {
          params: { page, size }
        });
        usStocks.value = response.data.stocks || [];
        
        if (selectedMarket.value === 'US') {
          stockList.value = usStocks.value;
          totalCount.value = response.data.total_count || 0;
          totalPages.value = response.data.total_pages || 1;
          currentPage.value = response.data.page || 1;
        }
        
        // 데이터가 없으면 메시지 표시
        if (response.data.message) {
          errorMessage.value = response.data.message;
        }
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error ||
          "해외 주식 목록을 불러오는 중 오류가 발생했습니다.";
        usStocks.value = [];
      } finally {
        listLoading.value = false;
      }
    };

    // 주식 데이터 갱신 (30분 제한)
    const refreshStocks = async (market) => {
      refreshLoading.value = true;
      errorMessage.value = null;

      try {
        const response = await axios.post(`${API_URL}/api/stocks/refresh/`, {
          market: market.toUpperCase()
        });
        
        // 갱신 성공 시 데이터 다시 로드
        if (response.data.success) {
          if (market === 'KR') {
            await fetchKrStocks(1, perPage.value);
          } else {
            await fetchUsStocks(1, perPage.value);
          }
          // 갱신 상태도 업데이트
          await fetchUpdateStatus();
        }
        
        return response.data;
      } catch (error) {
        const message = error.response?.data?.message || '갱신에 실패했습니다.';
        errorMessage.value = message;
        return { success: false, message };
      } finally {
        refreshLoading.value = false;
      }
    };

    // 북마크한 주식 목록 조회
    const fetchBookmarkedStocks = async () => {
      bookmarkLoading.value = true;
      errorMessage.value = null;

      try {
        const token = getToken();
        if (!token) {
          bookmarkedStocks.value = [];
          return;
        }

        const response = await axios.get(`${API_URL}/api/stocks/bookmarks/`, {
          headers: { Authorization: `Token ${token}` }
        });
        // 백엔드 응답 형식에 맞춰 처리 (배열 또는 {stocks: []} 형식 모두 지원)
        bookmarkedStocks.value = response.data.stocks || response.data || [];
        
        if (selectedMarket.value === 'BOOKMARK') {
          stockList.value = bookmarkedStocks.value;
          totalCount.value = bookmarkedStocks.value.length;
          totalPages.value = 1;
        }
      } catch (error) {
        console.error('북마크 목록 조회 실패:', error);
        bookmarkedStocks.value = [];
      } finally {
        bookmarkLoading.value = false;
      }
    };

    // 북마크 주식 갱신 (실시간 가격 업데이트)
    const refreshBookmarkedStocks = async () => {
      bookmarkRefreshLoading.value = true;
      errorMessage.value = null;

      try {
        const token = getToken();
        if (!token) {
          errorMessage.value = '로그인이 필요합니다.';
          return { success: false, message: '로그인이 필요합니다.' };
        }

        const response = await axios.post(
          `${API_URL}/api/stocks/bookmarks/refresh/`,
          {},
          { headers: { Authorization: `Token ${token}` } }
        );

        // 갱신 성공 시 북마크 목록 다시 조회
        if (response.data.success) {
          await fetchBookmarkedStocks();
          bookmarkRefreshTime.value = new Date().toISOString();
        }

        return response.data;
      } catch (error) {
        const message = error.response?.data?.error || '북마크 갱신에 실패했습니다.';
        errorMessage.value = message;
        return { success: false, message };
      } finally {
        bookmarkRefreshLoading.value = false;
      }
    };

    // 북마크 추가
    const addBookmark = async (symbol, name) => {
      try {
        const token = getToken();
        if (!token) {
          errorMessage.value = '로그인이 필요합니다.';
          return false;
        }

        await axios.post(
          `${API_URL}/api/stocks/bookmarks/`,
          { symbol, name },
          { headers: { Authorization: `Token ${token}` } }
        );
        
        // 북마크 목록 새로고침
        await fetchBookmarkedStocks();
        return true;
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error || '북마크 추가에 실패했습니다.';
        return false;
      }
    };

    // 북마크 삭제
    const removeBookmark = async (symbol) => {
      try {
        const token = getToken();
        if (!token) {
          errorMessage.value = '로그인이 필요합니다.';
          return false;
        }

        await axios.delete(`${API_URL}/api/stocks/bookmarks/`, {
          data: { symbol },
          headers: { Authorization: `Token ${token}` }
        });
        
        // 북마크 목록 새로고침
        await fetchBookmarkedStocks();
        return true;
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error || '북마크 삭제에 실패했습니다.';
        return false;
      }
    };

    // 북마크 여부 확인
    const checkBookmark = async (symbol) => {
      try {
        const token = getToken();
        if (!token) return false;

        const response = await axios.get(
          `${API_URL}/api/stocks/bookmarks/${symbol}/check/`,
          { headers: { Authorization: `Token ${token}` } }
        );
        return response.data.is_bookmarked;
      } catch (error) {
        return false;
      }
    };

    // 인기 종목 목록 조회 (기존 API 호환)
    const fetchStockList = async (market = "") => {
      listLoading.value = true;
      errorMessage.value = null;

      try {
        const params = { limit: 40 };
        if (market && market !== "ALL") {
          params.market = market;
        }
        const response = await axios.get(`${API_URL}/api/stocks/popular/`, { params });
        stockList.value = response.data.stocks || [];
        totalCount.value = stockList.value.length;
        totalPages.value = 1;
        currentPage.value = 1;
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error ||
          "종목 목록을 불러오는 중 오류가 발생했습니다.";
        stockList.value = [];
      } finally {
        listLoading.value = false;
      }
    };

    // 인기 종목 (실시간 가격 포함) - 기존 API 호환
    const fetchPopularStocks = async (market = "") => {
      loading.value = true;
      errorMessage.value = null;

      try {
        const params = market ? { market, limit: 20 } : { limit: 20 };
        const response = await axios.get(`${API_URL}/api/stocks/popular/`, {
          params,
        });
        popularStocks.value = response.data.stocks;
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error ||
          "인기 종목을 불러오는 중 오류가 발생했습니다.";
        popularStocks.value = [];
      } finally {
        loading.value = false;
      }
    };

    const searchStocks = async (query) => {
      if (!query || query.trim() === "") {
        searchResults.value = [];
        return;
      }

      searchLoading.value = true;
      errorMessage.value = null;

      try {
        const response = await axios.get(`${API_URL}/api/stocks/search/`, {
          params: { query: query.trim() },
        });
        searchResults.value = response.data.results || [];
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error || "검색 중 오류가 발생했습니다.";
        searchResults.value = [];
      } finally {
        searchLoading.value = false;
      }
    };

    const fetchStockDetail = async (symbol) => {
      loading.value = true;
      errorMessage.value = null;

      try {
        const response = await axios.get(`${API_URL}/api/stocks/${symbol}/`);
        selectedStock.value = response.data;

        // 차트 데이터도 함께 로드
        await fetchChartData(symbol);
        await fetchStockNews(symbol);
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error ||
          "종목 정보를 불러오는 중 오류가 발생했습니다.";
        selectedStock.value = null;
      } finally {
        loading.value = false;
      }
    };

    const fetchChartData = async (symbol, period = null, interval = null) => {
      chartLoading.value = true;

      const _period = period || chartPeriod.value;
      const _interval = interval || chartInterval.value;

      try {
        const response = await axios.get(
          `${API_URL}/api/stocks/${symbol}/chart/`,
          {
            params: {
              period: _period,
              interval: _interval,
            },
          }
        );
        chartData.value = response.data;
        chartPeriod.value = _period;
        chartInterval.value = _interval;
      } catch (error) {
        chartData.value = null;
        console.error("차트 데이터 로드 실패:", error);
      } finally {
        chartLoading.value = false;
      }
    };

    const fetchStockNews = async (symbol) => {
      try {
        const response = await axios.get(
          `${API_URL}/api/stocks/${symbol}/news/`
        );
        stockNews.value = response.data.news || [];
      } catch (error) {
        stockNews.value = [];
        console.error("뉴스 로드 실패:", error);
      }
    };

    // 기업설명 번역
    const translatedDescription = ref(null);
    const translating = ref(false);

    const translateDescription = async (text) => {
      if (!text) {
        translatedDescription.value = null;
        return;
      }

      translating.value = true;
      try {
        const response = await axios.post(`${API_URL}/api/stocks/translate/`, {
          text: text,
        });
        translatedDescription.value = response.data.translated;
      } catch (error) {
        console.error("번역 실패:", error);
        translatedDescription.value = null;
      } finally {
        translating.value = false;
      }
    };

    const setMarket = async (market) => {
      selectedMarket.value = market;
      currentPage.value = 1;  // 마켓 변경 시 페이지 초기화
      
      // 마켓 변경 시 해당 목록 API 호출
      if (market === 'BOOKMARK') {
        // 북마크는 로그인 사용자 데이터이므로 조회 필요
        await fetchBookmarkedStocks();
      } else if (market === 'KR') {
        // 항상 첫 페이지 데이터 조회 (페이지네이션 정보 포함)
        await fetchKrStocks(1, perPage.value);
      } else if (market === 'US') {
        // 항상 첫 페이지 데이터 조회 (페이지네이션 정보 포함)
        await fetchUsStocks(1, perPage.value);
      }
    };

    // 페이지 변경
    const changePage = async (page) => {
      if (page < 1 || page > totalPages.value) return;
      
      currentPage.value = page;
      
      if (selectedMarket.value === 'KR') {
        await fetchKrStocks(page, perPage.value);
      } else if (selectedMarket.value === 'US') {
        await fetchUsStocks(page, perPage.value);
      }
    };

    const setChartPeriod = async (period) => {
      if (selectedStock.value) {
        // 기간에 따른 적절한 interval 자동 설정
        let interval = "1d";
        if (period === "1d") interval = "5m";
        else if (period === "5d") interval = "15m";
        else if (["1mo", "3mo"].includes(period)) interval = "1d";
        else if (["6mo", "1y"].includes(period)) interval = "1wk";
        else interval = "1mo";

        await fetchChartData(selectedStock.value.symbol, period, interval);
      }
    };

    const clearSelectedStock = () => {
      selectedStock.value = null;
      chartData.value = null;
      stockNews.value = [];
      translatedDescription.value = null;
    };

    const clearSearchResults = () => {
      searchResults.value = [];
    };

    return {
      // State
      popularStocks,
      stockList,
      krStocks,
      usStocks,
      bookmarkedStocks,
      searchResults,
      selectedStock,
      chartData,
      stockNews,
      loading,
      listLoading,
      chartLoading,
      searchLoading,
      bookmarkLoading,
      refreshLoading,
      bookmarkRefreshLoading,
      bookmarkRefreshTime,
      errorMessage,
      selectedMarket,
      chartPeriod,
      chartInterval,
      translatedDescription,
      translating,
      currentPage,
      totalPages,
      totalCount,
      perPage,
      marketIndices,
      indicesLoading,
      updateStatus,

      // Computed
      filteredStocks,
      hasSelectedStock,
      hasChartData,

      // Actions
      fetchMarketIndices,
      fetchUpdateStatus,
      fetchKrStocks,
      fetchUsStocks,
      fetchBookmarkedStocks,
      refreshStocks,
      refreshBookmarkedStocks,
      changePage,
      addBookmark,
      removeBookmark,
      checkBookmark,
      fetchStockList,
      fetchPopularStocks,
      searchStocks,
      fetchStockDetail,
      fetchChartData,
      fetchStockNews,
      translateDescription,
      setMarket,
      setChartPeriod,
      clearSelectedStock,
      clearSearchResults,
    };
  },
  { persist: true }
);
