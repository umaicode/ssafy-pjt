<template>
  <div class="kakao-map-container">
    <header class="map-header">PJT08 - 은행 검색 어플리케이션</header>
    <h3 class="map-title">은행 찾기</h3>

    <div class="main">
      <div class="search-box">
        <div>
          <!-- 출발지 설정 섹션 -->
          <label>출발지</label>
          <div class="origin-section">
            <input 
              type="text" 
              v-model="kakaoMapStore.originSearchKeyword" 
              placeholder="출발지 검색"
              @keyup.enter="kakaoMapStore.searchOrigin"
              class="origin-input"
            />
            <button class="origin-search-btn" @click="kakaoMapStore.searchOrigin">검색</button>
          </div>
          <button class="current-location-btn" @click="kakaoMapStore.setOriginToCurrentLocation">
            📍 현재 위치로 설정
          </button>
          <div v-if="kakaoMapStore.originLocation" class="origin-display">
            ✓ {{ kakaoMapStore.originLocation.name }}
          </div>
          
          <hr class="divider" />
          
          <label>광역시 / 도</label>
          <select v-model="kakaoMapStore.selectedCity">
            <option value="">광역시/도 선택하세요</option>
            <option v-for="city in kakaoMapStore.cityOptions" :key="city" :value="city">{{ city }}</option>
          </select>

          <label>시 / 군 / 구</label>
          <select v-model="kakaoMapStore.selectedDistrict">
            <option value="">시/군/구 선택하세요</option>
            <option v-for="district in kakaoMapStore.districtOptions" :key="district" :value="district">{{ district }}</option>
          </select>

          <label>은행</label>
          <select v-model="kakaoMapStore.selectedBank">
            <option value="">은행 선택하세요</option>
            <option v-for="bank in kakaoMapStore.bankOptions" :key="bank" :value="bank">{{ bank }}</option>
          </select>

          <button class="search-btn" @click="kakaoMapStore.handleSearch">찾기</button>
        </div>
      </div>

      <div id="map"></div>
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
.kakao-map-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: sans-serif;
  background: #fff;
}

/* 상단 주황 헤더 */
.map-header {
  height: 36px;
  background: #e67e57;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #d86d45;
  margin: 20px 10px 20px 10px;
}

.map-title {
  border-bottom: 1px solid #e67e57;
  margin: 20px;
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

/* 헤더 아래 영역: 좌 검색 / 우 지도 */
.main {
  display: flex;
  flex: 1;
  min-height: 0;
}

/* 왼쪽 검색 박스 */
.search-box {
  width: 260px;
  padding: 14px 12px;
  box-sizing: border-box;
  background: #fff;
}

.search-box label {
  display: block;
  margin-top: 12px;
  margin-bottom: 4px;
  font-size: 13px;
  font-weight: 700;
  color: #333;
}

.search-box select {
  width: 100%;
  padding: 8px;
  font-size: 13px;
  border: 1px solid #ddd;
  border-radius: 2px;
  background: #fff;
}

.search-btn {
  margin-top: 12px;
  width: 100%;
  padding: 10px;
  font-size: 13px;
  font-weight: 800;
  color: white;
  background: #e67e57;
  border: none;
  cursor: pointer;
  border-radius: 2px;
}

.search-btn:hover {
  background: #d86d45;
}

/* 출발지 관련 스타일 */
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
  border-radius: 2px;
}

.origin-search-btn {
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  background: #4A90E2;
  border: none;
  cursor: pointer;
  border-radius: 2px;
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
  border-radius: 2px;
  margin-bottom: 8px;
}

.current-location-btn:hover {
  background: #fff5f2;
}

.origin-display {
  padding: 6px 8px;
  font-size: 12px;
  color: #4A90E2;
  background: #f0f7ff;
  border-radius: 2px;
  margin-bottom: 8px;
}

.divider {
  border: none;
  border-top: 1px solid #eee;
  margin: 16px 0;
}

/* 오른쪽 지도 영역 */
#map {
  flex: 1;
  min-width: 0;
  height: 100%;
  margin: 20px;
  border: 1px solid #e7baa0;
}
</style>
