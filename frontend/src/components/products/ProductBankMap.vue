<template>
  <div class="product-bank-map">
    <!-- Header -->
    <div class="map-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
        </div>
        <div class="header-text">
          <h3>{{ bankName }} 위치 찾기</h3>
          <p>가까운 지점을 검색해보세요</p>
        </div>
      </div>
      <button class="close-btn" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>
    
    <div class="map-content">
      <!-- Search Sidebar -->
      <div class="search-sidebar">
        <!-- Origin Section -->
        <div class="input-section">
          <label class="input-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            출발지
          </label>
          <div class="origin-row">
            <input 
              type="text" 
              v-model="kakaoMapStore.originSearchKeyword" 
              placeholder="출발지 검색"
              @keyup.enter="searchOriginAndRefresh"
              class="input-field"
            />
            <button class="btn-origin-search" @click="searchOriginAndRefresh">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
            </button>
          </div>
          <button class="btn-current-location" @click="setCurrentAndRefresh">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="3 11 22 2 13 21 11 13 3 11"/>
            </svg>
            현재 위치로 설정
          </button>
          <div v-if="kakaoMapStore.originLocation" class="origin-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            {{ kakaoMapStore.originLocation.name }}
          </div>
        </div>

        <div class="section-divider"></div>

        <!-- Region Filters -->
        <div class="input-section">
          <label class="input-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            지역 선택
          </label>
          
          <div class="select-wrapper">
            <select v-model="kakaoMapStore.selectedCity" @change="onCityChange" class="select-field">
              <option value="">광역시/도 선택</option>
              <option v-for="city in kakaoMapStore.cityOptions" :key="city" :value="city">{{ city }}</option>
            </select>
            <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>

          <div class="select-wrapper">
            <select v-model="kakaoMapStore.selectedDistrict" class="select-field">
              <option value="">시/군/구 선택</option>
              <option v-for="district in kakaoMapStore.districtOptions" :key="district" :value="district">{{ district }}</option>
            </select>
            <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>
        </div>

        <!-- Search Button -->
        <button class="btn-search" @click="searchByRegion">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          {{ bankName }} 찾기
        </button>

        <!-- Search Results -->
        <div class="results-section" v-if="kakaoMapStore.searchResults.length">
          <div class="results-header">
            <span class="results-title">검색 결과</span>
            <span class="results-count">{{ kakaoMapStore.searchResults.length }}개</span>
          </div>
          <ul class="results-list">
            <li 
              v-for="(place, index) in kakaoMapStore.searchResults" 
              :key="index"
              @click="kakaoMapStore.selectBank(place)"
              :class="{ selected: kakaoMapStore.selectedPlace?.id === place.id }"
              class="result-item"
            >
              <div class="result-info">
                <div class="place-name">{{ place.place_name }}</div>
                <div class="place-address">{{ place.address_name }}</div>
              </div>
              <div class="place-distance" v-if="place.distance">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                {{ formatDistance(place.distance) }}
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Map Area -->
      <div class="map-wrapper">
        <div id="product-bank-map" class="map-area"></div>
        <div class="map-overlay">
          <span class="overlay-badge">Kakao Map</span>
        </div>
      </div>
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

// 거리 포맷팅
const formatDistance = (distance) => {
  const d = parseInt(distance)
  if (d >= 1000) {
    return (d / 1000).toFixed(1) + 'km'
  }
  return d + 'm'
}

// 시/도 선택 시 시/군/구 옵션 업데이트
const onCityChange = () => {
  kakaoMapStore.updateDistrictOptions()
}

// 출발지 검색 후 은행 재검색
const searchOriginAndRefresh = () => {
  kakaoMapStore.searchOrigin()
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
  fetch('/data.json')
    .then((response) => response.json())
    .then((data) => kakaoMapStore.loadData(data))

  kakaoMapStore.loadKakaoScript('product-bank-map', {
    level: 5,
    autoSearch: true,
    bankName: props.bankName,
    showCurrentLocationMarker: false,
    autoSetOrigin: true
  })
})

onUnmounted(() => {
  kakaoMapStore.cleanup()
})
</script>

<style scoped>
.product-bank-map {
  margin-top: 20px;
  border-radius: 20px;
  overflow: hidden;
  background: white;
  box-shadow: 0 8px 32px rgba(116, 105, 182, 0.15);
  border: 1px solid rgba(116, 105, 182, 0.1);
}

/* Header */
.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon svg {
  width: 22px;
  height: 22px;
  color: white;
}

.header-text h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
  margin: 0 0 2px;
}

.header-text p {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.close-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn svg {
  width: 18px;
  height: 18px;
  color: white;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* Content */
.map-content {
  display: flex;
  height: 480px;
}

/* Search Sidebar */
.search-sidebar {
  width: 300px;
  padding: 20px;
  overflow-y: auto;
  border-right: 1px solid #e4e4e7;
  background: #fafafa;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8125rem;
  font-weight: 700;
  color: #18181b;
}

.input-label svg {
  width: 14px;
  height: 14px;
  color: #7469B6;
}

.input-field {
  width: 100%;
  padding: 10px 12px;
  font-size: 0.8125rem;
  border: 1px solid #e4e4e7;
  border-radius: 10px;
  background: white;
  transition: all 0.2s;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #7469B6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.1);
}

.origin-row {
  display: flex;
  gap: 8px;
}

.origin-row .input-field {
  flex: 1;
}

.btn-origin-search {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-origin-search svg {
  width: 16px;
  height: 16px;
  color: white;
}

.btn-origin-search:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-current-location {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 10px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #7469B6;
  background: rgba(116, 105, 182, 0.08);
  border: 1px solid rgba(116, 105, 182, 0.2);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-current-location svg {
  width: 12px;
  height: 12px;
}

.btn-current-location:hover {
  background: rgba(116, 105, 182, 0.12);
}

.origin-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #16a34a;
  background: #f0fdf4;
  border-radius: 8px;
}

.origin-badge svg {
  width: 14px;
  height: 14px;
}

.section-divider {
  height: 1px;
  background: #e4e4e7;
  margin: 16px 0;
}

.select-wrapper {
  position: relative;
}

.select-field {
  width: 100%;
  padding: 10px 36px 10px 12px;
  font-size: 0.8125rem;
  border: 1px solid #e4e4e7;
  border-radius: 10px;
  background: white;
  appearance: none;
  cursor: pointer;
  transition: all 0.2s;
  box-sizing: border-box;
}

.select-field:focus {
  outline: none;
  border-color: #7469B6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.1);
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  color: #71717a;
  pointer-events: none;
}

.btn-search {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  font-size: 0.875rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  margin-top: 16px;
  transition: all 0.2s;
}

.btn-search svg {
  width: 16px;
  height: 16px;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(116, 105, 182, 0.4);
}

/* Results */
.results-section {
  margin-top: 16px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.results-title {
  font-size: 0.8125rem;
  font-weight: 700;
  color: #18181b;
}

.results-count {
  font-size: 0.75rem;
  font-weight: 600;
  color: #7469B6;
  background: rgba(116, 105, 182, 0.1);
  padding: 4px 10px;
  border-radius: 12px;
}

.results-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 180px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: white;
  border: 1px solid #e4e4e7;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.result-item:hover {
  border-color: #AD88C6;
  box-shadow: 0 2px 8px rgba(116, 105, 182, 0.1);
}

.result-item.selected {
  background: rgba(116, 105, 182, 0.08);
  border-color: #7469B6;
}

.result-info {
  flex: 1;
  min-width: 0;
}

.place-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #18181b;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.place-address {
  font-size: 0.6875rem;
  color: #71717a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.place-distance {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.6875rem;
  font-weight: 600;
  color: #7469B6;
  flex-shrink: 0;
  margin-left: 8px;
}

.place-distance svg {
  width: 12px;
  height: 12px;
}

/* Map Wrapper */
.map-wrapper {
  flex: 1;
  position: relative;
}

.map-area {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  top: 12px;
  right: 12px;
}

.overlay-badge {
  padding: 6px 12px;
  font-size: 0.6875rem;
  font-weight: 600;
  color: white;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  border-radius: 6px;
}

/* Dark Mode */
[data-theme="dark"] .product-bank-map {
  background: #18181b;
  border-color: rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .map-header {
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.15) 0%, rgba(173, 136, 198, 0.15) 100%);
}

[data-theme="dark"] .header-icon {
  background: rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .header-text h3 {
  color: #e4e4e7;
}

[data-theme="dark"] .header-text p {
  color: #a1a1aa;
}

[data-theme="dark"] .close-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #a1a1aa;
}

[data-theme="dark"] .close-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #e4e4e7;
}

[data-theme="dark"] .search-sidebar {
  background: #0a0a0a;
  border-right-color: #27272a;
}

[data-theme="dark"] .input-label {
  color: #e4e4e7;
}

[data-theme="dark"] .input-field,
[data-theme="dark"] .select-field {
  background: #18181b;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .input-field::placeholder {
  color: #71717a;
}

[data-theme="dark"] .input-field:focus,
[data-theme="dark"] .select-field:focus {
  border-color: #7469B6;
}

[data-theme="dark"] .btn-origin-search {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .btn-origin-search:hover {
  background: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .btn-current-location {
  background: rgba(116, 105, 182, 0.15);
  color: #E1AFD1;
}

[data-theme="dark"] .btn-current-location:hover {
  background: rgba(116, 105, 182, 0.25);
}

[data-theme="dark"] .origin-badge {
  background: rgba(116, 105, 182, 0.2);
  color: #E1AFD1;
}

[data-theme="dark"] .section-divider {
  background: #27272a;
}

[data-theme="dark"] .select-arrow {
  color: #71717a;
}

[data-theme="dark"] .results-title {
  color: #e4e4e7;
}

[data-theme="dark"] .result-item {
  background: #18181b;
  border-color: #3f3f46;
}

[data-theme="dark"] .result-item:hover {
  border-color: #AD88C6;
}

[data-theme="dark"] .result-item.selected {
  background: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .place-name {
  color: #e4e4e7;
}

[data-theme="dark"] .place-address {
  color: #a1a1aa;
}

/* Responsive */
@media (max-width: 768px) {
  .map-content {
    flex-direction: column;
    height: auto;
  }

  .search-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e4e4e7;
  }

  .map-wrapper {
    height: 350px;
  }
}
</style>
