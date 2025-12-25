import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from "axios";

export const useStocksStore = defineStore(
  "stocks",
  () => {
    const API_URL = "http://127.0.0.1:8000";

    // State
    const popularStocks = ref([]);
    const stockList = ref([]);  // 인기 종목 목록
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
    const errorMessage = ref(null);

    // 선택된 마켓 (KR, US, ALL)
    const selectedMarket = ref("ALL");

    // 페이지네이션
    const currentPage = ref(1);
    const totalPages = ref(1);
    const totalCount = ref(0);
    const perPage = ref(30);

    // 차트 설정
    const chartPeriod = ref("1mo");
    const chartInterval = ref("1d");

    // Computed
    const filteredStocks = computed(() => {
      if (selectedMarket.value === "ALL") {
        return stockList.value;
      }
      const marketFilter = selectedMarket.value === "KR" ? ["KOSPI", "KOSDAQ"] : ["US"];
      return stockList.value.filter(
        (stock) => marketFilter.includes(stock.market)
      );
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

    // 인기 종목 목록 조회 (yfinance 실시간)
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

    // 인기 종목 (실시간 가격 포함)
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

    const setMarket = (market) => {
      selectedMarket.value = market;
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
      searchResults,
      selectedStock,
      chartData,
      stockNews,
      loading,
      listLoading,
      chartLoading,
      searchLoading,
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

      // Computed
      filteredStocks,
      hasSelectedStock,
      hasChartData,

      // Actions
      fetchMarketIndices,
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
