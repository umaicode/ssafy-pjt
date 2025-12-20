<template>
  <div class="product-bank-map">
    <div class="map-header">
      <h3>📍 {{ bankName }} 위치 찾기</h3>
      <button class="close-btn" @click="$emit('close')">✕</button>
    </div>
    
    <div class="map-content">
      <div class="search-box">
        <!-- 출발지 설정 섹션 -->
        <div class="section">
          <label>출발지</label>
          <div class="origin-section">
            <input 
              type="text" 
              v-model="kakaoMapStore.originSearchKeyword" 
              placeholder="출발지 검색"
              @keyup.enter="searchOriginAndRefresh"
              class="origin-input"
            />
            <button class="origin-search-btn" @click="searchOriginAndRefresh">검색</button>
          </div>
          <button class="current-location-btn" @click="setCurrentAndRefresh">
            📍 현재 위치로 설정
          </button>
          <div v-if="kakaoMapStore.originLocation" class="origin-display">
            ✓ {{ kakaoMapStore.originLocation.name }}
          </div>
        </div>

        <hr class="divider" />

        <!-- 은행 검색 섹션 -->
        <div class="section">
          <label>검색 지역</label>
          <select v-model="kakaoMapStore.selectedCity" @change="onCityChange">
            <option value="">광역시/도 선택</option>
            <option v-for="city in kakaoMapStore.cityOptions" :key="city" :value="city">{{ city }}</option>
          </select>

          <select v-model="kakaoMapStore.selectedDistrict">
            <option value="">시/군/구 선택</option>
            <option v-for="district in kakaoMapStore.districtOptions" :key="district" :value="district">{{ district }}</option>
          </select>

          <button class="search-btn" @click="searchByRegion">{{ bankName }} 찾기</button>
        </div>

        <!-- 검색 결과 목록 -->
        <div class="results-section" v-if="kakaoMapStore.searchResults.length">
          <label>검색 결과 ({{ kakaoMapStore.searchResults.length }})</label>
          <ul class="results-list">
            <li 
              v-for="(place, index) in kakaoMapStore.searchResults" 
              :key="index"
              @click="kakaoMapStore.selectBank(place)"
              :class="{ selected: kakaoMapStore.selectedPlace?.id === place.id }"
            >
              <div class="place-name">{{ place.place_name }}</div>
              <div class="place-address">{{ place.address_name }}</div>
              <div class="place-distance" v-if="place.distance">{{ place.distance }}m</div>
            </li>
          </ul>
        </div>
      </div>

      <div id="product-bank-map" class="map-area"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useKakaoMapStore } from '@/stores/kakaomap'

const props = defineProps({
  bankName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const kakaoMapStore = useKakaoMapStore()

// 시/도 선택 시 시/군/구 옵션 업데이트
const onCityChange = () => {
  kakaoMapStore.updateDistrictOptions()
}

// 출발지 검색 후 은행 재검색
const searchOriginAndRefresh = () => {
  kakaoMapStore.searchOrigin()
  // 출발지 변경 후 주변 은행 재검색
  setTimeout(() => {
    if (kakaoMapStore.originLocation) {
      kakaoMapStore.searchBankNearby(
        props.bankName,
        kakaoMapStore.originLocation.lat,
        kakaoMapStore.originLocation.lng
      )
    }
  }, 500)
}

// 현재 위치로 설정 후 은행 재검색
const setCurrentAndRefresh = () => {
  kakaoMapStore.setOriginToCurrentLocation()
  // 출발지 변경 후 주변 은행 재검색
  setTimeout(() => {
    if (kakaoMapStore.currentLocation) {
      kakaoMapStore.searchBankNearby(
        props.bankName,
        kakaoMapStore.currentLocation.lat,
        kakaoMapStore.currentLocation.lng
      )
    }
  }, 500)
}

// 지역 선택으로 검색
const searchByRegion = () => {
  kakaoMapStore.searchBankByRegion(props.bankName)
}

onMounted(() => {
  // data.json 로드
  fetch('/data.json')
    .then((response) => response.json())
    .then((data) => kakaoMapStore.loadData(data))

  // 카카오 API 로드 (ProductDetailView용 옵션)
  kakaoMapStore.loadKakaoScript('product-bank-map', {
    level: 5,
    autoSearch: true,
    bankName: props.bankName,
    showCurrentLocationMarker: false,  // 출발지 마커로 대체
    autoSetOrigin: true
  })
})

onUnmounted(() => {
  // 지도 정리
  kakaoMapStore.cleanup()
})
</script>

<style scoped>
.product-bank-map {
  margin-top: 20px;
  border: 2px solid #e67e57;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #e67e57;
  color: white;
}

.map-header h3 {
  margin: 0;
  font-size: 16px;
}

.close-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0 4px;
}

.close-btn:hover {
  opacity: 0.8;
}

.map-content {
  display: flex;
  height: 500px;
}

.search-box {
  width: 280px;
  padding: 16px;
  border-right: 1px solid #eee;
  overflow-y: auto;
}

.section {
  margin-bottom: 12px;
}

.search-box label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #333;
}

.search-box select {
  width: 100%;
  padding: 8px;
  font-size: 13px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 8px;
}

.origin-section {
  display: flex;
  gap: 4px;
  margin-bottom: 8px;
}

.origin-input {
  flex: 1;
  padding: 8px;
  font-size: 13px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.origin-search-btn {
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  background: #4A90E2;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.origin-search-btn:hover {
  background: #357ABD;
}

.current-location-btn {
  width: 100%;
  padding: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #e67e57;
  background: #fff;
  border: 1px solid #e67e57;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 8px;
}

.current-location-btn:hover {
  background: #fff5f2;
}

.origin-display {
  font-size: 12px;
  color: #4A90E2;
  font-weight: 600;
}

.divider {
  border: none;
  border-top: 1px solid #eee;
  margin: 16px 0;
}

.search-btn {
  width: 100%;
  padding: 10px;
  font-size: 13px;
  font-weight: 700;
  color: white;
  background: #e67e57;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.search-btn:hover {
  background: #d86d45;
}

.results-section {
  margin-top: 16px;
}

.results-list {
  list-style: none;
  padding: 0;
  margin: 8px 0 0;
  max-height: 200px;
  overflow-y: auto;
}

.results-list li {
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.results-list li:hover {
  background: #f9f9f9;
  border-color: #e67e57;
}

.results-list li.selected {
  background: #fff5f2;
  border-color: #e67e57;
}

.place-name {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.place-address {
  font-size: 11px;
  color: #888;
}

.place-distance {
  font-size: 11px;
  color: #e67e57;
  font-weight: 600;
  margin-top: 4px;
}

.map-area {
  flex: 1;
  min-height: 100%;
}
</style>
