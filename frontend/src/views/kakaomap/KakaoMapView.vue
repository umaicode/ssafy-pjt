<template>
  <div class="kakao-map-page">
    <!-- Header Section -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
        </div>
        <div class="header-text">
          <h1>은행 찾기</h1>
          <p>가까운 은행 지점을 검색해보세요</p>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="main-container">
      <!-- Search Sidebar -->
      <aside class="search-sidebar">
        <div class="search-card">
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
                @keyup.enter="kakaoMapStore.searchOrigin"
                class="input-field"
              />
              <button class="btn-origin-search" @click="kakaoMapStore.searchOrigin">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
              </button>
            </div>
            <button class="btn-current-location" @click="kakaoMapStore.setOriginToCurrentLocation">
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

          <!-- Location Filters -->
          <div class="input-section">
            <label class="input-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              지역 선택
            </label>
            
            <div class="select-wrapper">
              <select v-model="kakaoMapStore.selectedCity" class="select-field">
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

          <div class="section-divider"></div>

          <!-- Bank Selection -->
          <div class="input-section">
            <label class="input-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="7" width="20" height="14" rx="2"/>
                <path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>
              </svg>
              은행 선택
            </label>
            
            <div class="select-wrapper">
              <select v-model="kakaoMapStore.selectedBank" class="select-field">
                <option value="">은행을 선택하세요</option>
                <option v-for="bank in kakaoMapStore.bankOptions" :key="bank" :value="bank">{{ bank }}</option>
              </select>
              <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <!-- Search Button -->
          <button class="btn-search" @click="kakaoMapStore.handleSearch">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            은행 찾기
          </button>
        </div>

        <!-- Info Card -->
        <div class="info-card">
          <div class="info-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
          </div>
          <div class="info-text">
            <p>지도를 클릭하면 해당 위치의 상세 정보를 확인할 수 있습니다.</p>
          </div>
        </div>
      </aside>

      <!-- Map Container -->
      <div class="map-wrapper">
        <div id="map"></div>
        <div class="map-overlay">
          <span class="overlay-badge">Kakao Map</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { useKakaoMapStore } from '@/stores/kakaomap';

const kakaoMapStore = useKakaoMapStore();

// 시/도 선택 시 시/군/구 옵션 업데이트
watch(() => kakaoMapStore.selectedCity, () => {
  kakaoMapStore.updateDistrictOptions();
});

onMounted(() => {
  // data.json 로드
  fetch("/data.json")
    .then((response) => response.json())
    .then((data) => kakaoMapStore.loadData(data));

  // 카카오 API 키 로드
  kakaoMapStore.loadKakaoScript();
});
</script>

<style scoped>
.kakao-map-page {
  min-height: 100vh;
  background: #FDFBFD;
}

/* Header */
.page-header {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  padding: 32px 24px;
  margin-bottom: 0px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 52px;
  height: 52px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.header-text h1 {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  margin: 0 0 4px;
  text-align: left;
}

.header-text p {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

/* Main Container */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  gap: 24px;
  min-height: calc(100vh - 140px);
}

/* Search Sidebar */
.search-sidebar {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
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
  font-size: 0.875rem;
  font-weight: 700;
  color: #18181b;
}

.input-label svg {
  width: 16px;
  height: 16px;
  color: #7469B6;
}

.input-field {
  width: 100%;
  padding: 12px 14px;
  font-size: 0.875rem;
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  background: #fafafa;
  transition: all 0.2s;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #7469B6;
  background: white;
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
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-origin-search svg {
  width: 18px;
  height: 18px;
  color: white;
}

.btn-origin-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-current-location {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #7469B6;
  background: rgba(116, 105, 182, 0.08);
  border: 1px solid rgba(116, 105, 182, 0.2);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-current-location svg {
  width: 14px;
  height: 14px;
}

.btn-current-location:hover {
  background: rgba(116, 105, 182, 0.12);
  border-color: rgba(116, 105, 182, 0.3);
}

.origin-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #16a34a;
  background: #f0fdf4;
  border-radius: 10px;
}

.origin-badge svg {
  width: 16px;
  height: 16px;
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
  padding: 12px 40px 12px 14px;
  font-size: 0.875rem;
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  background: #fafafa;
  appearance: none;
  cursor: pointer;
  transition: all 0.2s;
  box-sizing: border-box;
}

.select-field:focus {
  outline: none;
  border-color: #7469B6;
  background: white;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.1);
}

.select-arrow {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #71717a;
  pointer-events: none;
}

.btn-search {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 14px;
  font-size: 0.9375rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border: none;
  border-radius: 14px;
  cursor: pointer;
  margin-top: 20px;
  transition: all 0.2s;
}

.btn-search svg {
  width: 18px;
  height: 18px;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(116, 105, 182, 0.4);
}

/* Info Card */
.info-card {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.info-icon {
  width: 36px;
  height: 36px;
  background: #fef3c7;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-icon svg {
  width: 18px;
  height: 18px;
  color: #d97706;
}

.info-text p {
  margin: 0;
  font-size: 0.8125rem;
  color: #52525b;
  line-height: 1.5;
}

/* Map Wrapper */
.map-wrapper {
  flex: 1;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

#map {
  width: 100%;
  height: 100%;
  min-height: 500px;
}

.map-overlay {
  position: absolute;
  top: 16px;
  right: 16px;
}

.overlay-badge {
  padding: 8px 14px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  border-radius: 8px;
}

/* Responsive */
@media (max-width: 900px) {
  .main-container {
    flex-direction: column;
  }

  .search-sidebar {
    width: 100%;
  }

  .map-wrapper {
    min-height: 400px;
  }
}

/* Dark Mode */
[data-theme="dark"] .kakao-map-page {
  background: #0a0a0a;
}

[data-theme="dark"] .main-container {
  background: #0a0a0a;
}

[data-theme="dark"] .search-card {
  background: #18181b;
  border-color: rgba(116, 105, 182, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .input-label {
  color: #e4e4e7;
}

[data-theme="dark"] .input-field,
[data-theme="dark"] .select-field {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .input-field:focus,
[data-theme="dark"] .select-field:focus {
  border-color: #7469B6;
  background: #27272a;
}

[data-theme="dark"] .input-field::placeholder {
  color: #71717a;
}

[data-theme="dark"] .select-arrow {
  color: #a1a1aa;
}

[data-theme="dark"] .section-divider {
  background: #27272a;
}

[data-theme="dark"] .info-card {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .info-text p {
  color: #a1a1aa;
}

[data-theme="dark"] .map-wrapper {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
</style>
