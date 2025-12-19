import { defineStore } from "pinia";
import { ref, reactive } from "vue";

export const useKakaoMapStore = defineStore("kakaomap", () => {
  // 상태 정의
  // 1. 지도 객체
  const map = ref(null);
  // 2. 장소 검색 객체
  const places = ref(null);
  // 3. 인포윈도우 객체
  const infoWindow = ref(null);
  // 4. 현재 지도에 표시된 마커들
  const markers = reactive([]);
  // 5. 시/도 옵션
  const cityOptions = ref([]);
  // 6. 시/군/구 옵션
  const districtOptions = ref([]);
  // 7. 선택된 시/도
  const selectedCity = ref(null);
  // 8. 선택된 시/군/구
  const selectedDistrict = ref(null);
  // 9. 선택된 은행
  const selectedBank = ref('');
  // 10. 은행 옵션
  const bankOptions = ref([]);
  // 11. data.json 모든 데이터
  const allData = ref(null);
  // 12. 현재 위치 좌표
  const currentLocation = ref(null);
  // 13. 경로 표시용 Polyline
  const routePolyline = ref(null);
  // 14. 출발지 정보 (이름, 좌표)
  const originLocation = ref(null);
  // 15. 출발지 검색어
  const originSearchKeyword = ref('');
  // 16. 출발지 마커
  const originMarker = ref(null);
  // 17. 검색 결과 목록
  const searchResults = ref([]);
  // 18. 선택된 장소
  const selectedPlace = ref(null);
  // 19. 현재 위치 마커
  const currentLocationMarker = ref(null);

  // 카카오 지도 API 스크립트 로드 (containerId: 지도 컨테이너 ID, options: 추가 옵션)
  const loadKakaoScript = (containerId = 'map', options = {}) => {
    // 이미 카카오 스크립트가 로드되어 있으면 바로 초기화
    if (window.kakao && window.kakao.maps) {
      initializeMap(containerId, options);
      return;
    }
    
    const apiKey = import.meta.env.VITE_KAKAO_API_KEY;
    const script = document.createElement('script');
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&autoload=false&libraries=services`;
    script.type = 'text/javascript';
    script.onload = () => initializeMap(containerId, options);
    document.head.appendChild(script);
  };

  // 지도 초기화 (containerId: 지도 컨테이너 ID, options: { autoSearch: boolean, bankName: string, showCurrentLocationMarker: boolean })
  const initializeMap = (containerId = 'map', options = {}) => {
    if (!window.kakao || !window.kakao.maps) {
      console.error('Kakao maps script not loaded');
      return;
    }
    
    window.kakao.maps.load(() => {
      const mapContainer = document.getElementById(containerId);
      if (!mapContainer) {
        console.error('Map container not found:', containerId);
        return;
      }
      
      // 기본 위치 (강남역)
      const defaultLat = 37.49818;
      const defaultLng = 127.027386;
      
      const mapOption = {
        center: new window.kakao.maps.LatLng(defaultLat, defaultLng),
        level: options.level || 5,
      };
      
      map.value = new window.kakao.maps.Map(mapContainer, mapOption);
      infoWindow.value = new window.kakao.maps.InfoWindow({ 
        zIndex: 1,
        removable: true
      });
      places.value = new window.kakao.maps.services.Places(map.value);
      
      // 현재 위치 가져오기
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const locPosition = new window.kakao.maps.LatLng(lat, lng);
            
            // 현재 위치 좌표 저장
            currentLocation.value = { lat, lng };
            
            // 지도 중심을 현재 위치로 이동
            map.value.setCenter(locPosition);
            
            // 현재 위치 마커 표시 (옵션에 따라)
            if (options.showCurrentLocationMarker !== false) {
              displayCurrentLocationMarker(lat, lng);
            }
            
            // 자동으로 출발지를 현재 위치로 설정
            if (options.autoSetOrigin !== false) {
              setOriginToCurrentLocation();
            }
            
            // 자동 검색 옵션이 있으면 주변 은행 검색
            if (options.autoSearch && options.bankName) {
              searchBankNearby(options.bankName, lat, lng);
            }
            
            console.log('현재 위치로 지도 설정:', lat, lng);
          },
          (error) => {
            console.warn('현재 위치를 가져올 수 없습니다. 기본 위치(강남역)를 사용합니다.', error);
            // 기본 위치로 출발지 설정
            if (options.autoSetOrigin !== false) {
              currentLocation.value = { lat: defaultLat, lng: defaultLng };
            }
          }
        );
      } else {
        console.warn('Geolocation을 지원하지 않는 브라우저입니다.');
      }
      
      console.log('Map initialized successfully');
    });
  };

  // 현재 위치 마커 표시
  const displayCurrentLocationMarker = (lat, lng) => {
    // 기존 마커 제거
    if (currentLocationMarker.value) {
      currentLocationMarker.value.setMap(null);
    }
    
    const locPosition = new window.kakao.maps.LatLng(lat, lng);
    
    currentLocationMarker.value = new window.kakao.maps.Marker({
      position: locPosition,
      map: map.value
    });
    
    // 역지오코딩으로 주소 정보 가져오기
    const geocoder = new window.kakao.maps.services.Geocoder();
    geocoder.coord2Address(lng, lat, (result, status) => {
      let addressName = '';
      let roadAddressName = '';
      
      if (status === window.kakao.maps.services.Status.OK) {
        const address = result[0];
        addressName = address.address?.address_name || '';
        roadAddressName = address.road_address?.address_name || '';
      }
      
      const message = `
        <div style="padding:10px; min-width:200px;">
          <div style="font-size:14px; font-weight:bold; margin-bottom:8px; color:#4A90E2;">
            📍 현재 위치
          </div>
          ${addressName ? `
            <div style="font-size:12px; color:#666; margin-bottom:4px;">
              📍 ${addressName}
            </div>
          ` : ''}
          ${roadAddressName ? `
            <div style="font-size:11px; color:#888; margin-bottom:4px;">
              🛣️ ${roadAddressName}
            </div>
          ` : ''}
        </div>
      `;
      
      const customInfoWindow = new window.kakao.maps.InfoWindow({
        content: message,
        removable: true
      });
      customInfoWindow.open(map.value, currentLocationMarker.value);
    });
  };

  // data.json 로드
  const loadData = (data) => {
    allData.value = data;
    cityOptions.value = data.mapInfo.map((sido) => sido.name);
    bankOptions.value = data.bankInfo || [];
  };

  // 시/도 선택 시 시/군/구 업데이트
  const updateDistrictOptions = () => {
    const selectedCityValue = selectedCity.value;
    if (!selectedCityValue) {
      districtOptions.value = [];
      return;
    }
    const sido = allData.value.mapInfo.find((item) => item.name === selectedCityValue);
    districtOptions.value = sido ? sido.countries : [];
  };

  // 장소 검색 콜백
  const placesSearchCallback = (result, status) => {
    if (status !== window.kakao.maps.services.Status.OK) {
      alert('검색 결과가 없습니다.');
      return;
    }
    clearMarkers();
    infoWindow.value.close();
    
    const bounds = new window.kakao.maps.LatLngBounds();
    
    result.forEach((place) => {
      const position = new window.kakao.maps.LatLng(place.y, place.x);
      const marker = new window.kakao.maps.Marker({ position });
      marker.setMap(map.value);
      markers.push(marker);
      bounds.extend(position);
      
      // 상세 정보 HTML 구성
      const html = `
        <div style="padding:10px; min-width:200px;">
          <div style="font-size:14px; font-weight:bold; margin-bottom:8px; color:#e67e57;">
            ${place.place_name}
          </div>
          <div style="font-size:12px; color:#666; margin-bottom:4px;">
            📍 ${place.address_name}
          </div>
          ${place.road_address_name ? `
            <div style="font-size:11px; color:#888; margin-bottom:4px;">
              🛣️ ${place.road_address_name}
            </div>
          ` : ''}
          ${place.phone ? `
            <div style="font-size:11px; color:#888; margin-bottom:4px;">
              📞 ${place.phone}
            </div>
          ` : ''}
          ${place.distance ? `
            <div style="font-size:11px; color:#e67e57; font-weight:600; margin-top:6px;">
              📏 ${place.distance}m
            </div>
          ` : ''}
        </div>
      `;
      
      window.kakao.maps.event.addListener(marker, 'click', () => {
        infoWindow.value.setContent(html);
        infoWindow.value.open(map.value, marker);
        
        // 출발지가 설정되어 있으면 경로 표시 (출발지 우선, 없으면 현재 위치)
        const origin = originLocation.value || currentLocation.value;
        if (origin) {
          drawRoute(origin.lat, origin.lng, place.y, place.x);
        } else {
          console.log('출발지를 먼저 설정해주세요.');
        }
      });
    });
    
    map.value.setBounds(bounds);
  };

  // 마커 지우기
  const clearMarkers = () => {
    markers.forEach((marker) => marker.setMap(null));
    markers.length = 0; // 마커 배열 비우기
  };

  // 경로 그리기 함수
  const drawRoute = async (originLat, originLng, destLat, destLng) => {
    try {
      // 기존 경로 제거
      if (routePolyline.value) {
        routePolyline.value.setMap(null);
      }
      
      // Kakao Mobility API 호출 (REST API KEY 사용)
      const REST_API_KEY = import.meta.env.VITE_KAKAO_REST_API_KEY;
      const REST_API_URL = 'https://apis-navi.kakaomobility.com/v1/directions';
      const response = await fetch(
        `${REST_API_URL}?origin=${originLng},${originLat}&destination=${destLng},${destLat}&priority=RECOMMEND`,
        {
          headers: {
            'Authorization': `KakaoAK ${REST_API_KEY}`
          }
        }
      );
      
      if (!response.ok) {
        console.error('경로 API 호출 실패:', response.status);
        return;
      }
      
      const data = await response.json();
      
      if (data.routes && data.routes.length > 0) {
        const route = data.routes[0];
        const path = [];
        
        // 경로의 모든 구간(section)에서 좌표 추출
        route.sections.forEach(section => {
          section.roads.forEach(road => {
            road.vertexes.forEach((vertex, index) => {
              // vertexes는 [lng, lat, lng, lat, ...] 형태
              if (index % 2 === 0) {
                const lng = vertex;
                const lat = road.vertexes[index + 1];
                path.push(new window.kakao.maps.LatLng(lat, lng));
              }
            });
          });
        });
        
        // Polyline 생성
        routePolyline.value = new window.kakao.maps.Polyline({
          path: path,
          strokeWeight: 5,
          strokeColor: '#4A90E2',
          strokeOpacity: 0.8,
          strokeStyle: 'solid'
        });
        
        // 지도에 표시
        routePolyline.value.setMap(map.value);
        
        console.log('경로 표시 완료:', route.summary);
      }
    } catch (error) {
      console.error('경로 그리기 오류:', error);
      alert('경로를 표시할 수 없습니다.');
    }
  };
  
  // 검색 처리
  const handleSearch = () => {
    // 지도가 초기화되지 않았으면 경고
    if (!places.value) {
      alert('지도가 아직 로딩 중입니다. 잠시 후 다시 시도해주세요.');
      return;
    }
    if (!selectedCity.value || !selectedBank.value) {
      alert('시/도와 은행명을 선택해주세요.');
      return;
    }
    const keyword = `${selectedCity.value} ${selectedDistrict.value ? selectedDistrict.value + ' ' : ''}${selectedBank.value} 은행`;
    places.value.keywordSearch(keyword, placesSearchCallback);
  };

  // 출발지를 현재 위치로 설정
  const setOriginToCurrentLocation = () => {
    if (!currentLocation.value) {
      alert('현재 위치를 가져올 수 없습니다.');
      return;
    }
    
    const { lat, lng } = currentLocation.value;
    
    // 역지오코딩으로 주소 정보 가져오기
    const geocoder = new window.kakao.maps.services.Geocoder();
    geocoder.coord2Address(lng, lat, (result, status) => {
      let placeInfo = null;
      
      if (status === window.kakao.maps.services.Status.OK) {
        const address = result[0];
        placeInfo = {
          address_name: address.address?.address_name || '',
          road_address_name: address.road_address?.address_name || '',
          phone: '',
          distance: ''
        };
      }
      
      setOrigin(lat, lng, '현재 위치', placeInfo);
    });
  };
  
  // 출발지 설정 (공통 함수)
  const setOrigin = (lat, lng, name, placeInfo = null) => {
    originLocation.value = { lat, lng, name };
    
    // 기존 출발지 마커 제거
    if (originMarker.value) {
      originMarker.value.setMap(null);
    }
    
    // 새 출발지 마커 생성 (빨간색 마커)
    const position = new window.kakao.maps.LatLng(lat, lng);
    
    const markerImage = new window.kakao.maps.MarkerImage(
      'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/red_b.png',
      new window.kakao.maps.Size(50, 45),
      { offset: new window.kakao.maps.Point(15, 43) }
    );
    
    originMarker.value = new window.kakao.maps.Marker({
      position: position,
      map: map.value,
      image: markerImage
    });
    
    // 출발지 인포윈도우 (은행 인포윈도우와 동일한 스타일)
    const originInfoContent = `
      <div style="padding:10px; min-width:200px;">
        <div style="font-size:14px; font-weight:bold; margin-bottom:8px; color:#e67e57;">
          🚗 출발지: ${name}
        </div>
        ${placeInfo?.address_name ? `
          <div style="font-size:12px; color:#666; margin-bottom:4px;">
            📍 ${placeInfo.address_name}
          </div>
        ` : ''}
        ${placeInfo?.road_address_name ? `
          <div style="font-size:11px; color:#888; margin-bottom:4px;">
            🛣️ ${placeInfo.road_address_name}
          </div>
        ` : ''}
        ${placeInfo?.phone ? `
          <div style="font-size:11px; color:#888; margin-bottom:4px;">
            📞 ${placeInfo.phone}
          </div>
        ` : ''}
        ${placeInfo?.distance ? `
          <div style="font-size:11px; color:#e67e57; font-weight:600; margin-top:6px;">
            📏 ${placeInfo.distance}m
          </div>
        ` : ''}
      </div>
    `;
    const originInfo = new window.kakao.maps.InfoWindow({
      content: originInfoContent,
      removable: true
    });
    originInfo.open(map.value, originMarker.value);
    
    console.log('출발지 설정:', name, lat, lng);
  };
  
  // 출발지 검색
  const searchOrigin = () => {
    if (!originSearchKeyword.value.trim()) {
      alert('출발지를 입력해주세요.');
      return;
    }
    
    if (!places.value) {
      alert('지도가 아직 로딩 중입니다.');
      return;
    }
    
    places.value.keywordSearch(originSearchKeyword.value, (result, status) => {
      if (status !== window.kakao.maps.services.Status.OK) {
        alert('검색 결과가 없습니다.');
        return;
      }
      
      // 첫 번째 결과를 출발지로 설정 (장소 정보 포함)
      const place = result[0];
      setOrigin(place.y, place.x, place.place_name, {
        address_name: place.address_name,
        road_address_name: place.road_address_name,
        phone: place.phone,
        distance: place.distance
      });
      
      // 지도 중심 이동
      const position = new window.kakao.maps.LatLng(place.y, place.x);
      map.value.setCenter(position);
    });
  };

  // 특정 은행 주변 검색 (ProductDetailView용)
  const searchBankNearby = (bankName, lat, lng) => {
    if (!places.value) {
      console.error('Places 객체가 초기화되지 않았습니다.');
      return;
    }
    
    const location = new window.kakao.maps.LatLng(lat, lng);
    
    places.value.keywordSearch(
      `${bankName}`,
      (result, status) => {
        if (status !== window.kakao.maps.services.Status.OK) {
          console.log('주변 은행 검색 결과 없음');
          searchResults.value = [];
          return;
        }
        
        displayBankMarkers(result);
      },
      {
        location: location,
        radius: 5000, // 5km 반경
        sort: window.kakao.maps.services.SortBy.DISTANCE
      }
    );
  };

  // 지역 + 은행명으로 검색 (ProductDetailView용)
  const searchBankByRegion = (bankName) => {
    if (!places.value) {
      alert('지도가 아직 로딩 중입니다.');
      return;
    }
    
    if (!selectedCity.value) {
      alert('검색 지역을 선택해주세요.');
      return;
    }
    
    const keyword = `${selectedCity.value} ${selectedDistrict.value ? selectedDistrict.value + ' ' : ''}${bankName}`;
    
    places.value.keywordSearch(keyword, (result, status) => {
      if (status !== window.kakao.maps.services.Status.OK) {
        alert('검색 결과가 없습니다.');
        searchResults.value = [];
        return;
      }
      
      displayBankMarkers(result);
    });
  };

  // 은행 마커 표시 (검색 결과용)
  const displayBankMarkers = (results) => {
    clearMarkers();
    searchResults.value = results;
    
    const bounds = new window.kakao.maps.LatLngBounds();
    
    results.forEach((place) => {
      const position = new window.kakao.maps.LatLng(place.y, place.x);
      const marker = new window.kakao.maps.Marker({ position });
      marker.setMap(map.value);
      markers.push(marker);
      bounds.extend(position);
      
      // 마커 클릭 이벤트
      window.kakao.maps.event.addListener(marker, 'click', () => {
        showBankInfoWindow(place, marker);
        selectedPlace.value = place;
        
        // 출발지가 설정되어 있으면 경로 표시
        const origin = originLocation.value || currentLocation.value;
        if (origin) {
          drawRoute(origin.lat, origin.lng, place.y, place.x);
        }
      });
    });
    
    // 출발지 마커도 bounds에 포함
    if (originLocation.value) {
      bounds.extend(new window.kakao.maps.LatLng(originLocation.value.lat, originLocation.value.lng));
    }
    
    map.value.setBounds(bounds);
  };

  // 은행 인포윈도우 표시
  const showBankInfoWindow = (place, marker) => {
    const html = `
      <div style="padding:10px; min-width:200px;">
        <div style="font-size:14px; font-weight:bold; margin-bottom:8px; color:#e67e57;">
          ${place.place_name}
        </div>
        <div style="font-size:12px; color:#666; margin-bottom:4px;">
          📍 ${place.address_name}
        </div>
        ${place.road_address_name ? `
          <div style="font-size:11px; color:#888; margin-bottom:4px;">
            🛣️ ${place.road_address_name}
          </div>
        ` : ''}
        ${place.phone ? `
          <div style="font-size:11px; color:#888; margin-bottom:4px;">
            📞 ${place.phone}
          </div>
        ` : ''}
        ${place.distance ? `
          <div style="font-size:11px; color:#e67e57; font-weight:600; margin-top:6px;">
            📏 ${place.distance}m
          </div>
        ` : ''}
      </div>
    `;
    
    infoWindow.value.setContent(html);
    infoWindow.value.open(map.value, marker);
  };

  // 은행 선택 (리스트에서 클릭 시)
  const selectBank = (place) => {
    selectedPlace.value = place;
    
    const position = new window.kakao.maps.LatLng(place.y, place.x);
    map.value.setCenter(position);
    
    // 해당 마커 찾아서 인포윈도우 열기
    const markerIndex = searchResults.value.findIndex(p => p.id === place.id);
    if (markerIndex >= 0 && markers[markerIndex]) {
      showBankInfoWindow(place, markers[markerIndex]);
    }
    
    // 경로 그리기
    const origin = originLocation.value || currentLocation.value;
    if (origin) {
      drawRoute(origin.lat, origin.lng, place.y, place.x);
    }
  };

  // 지도 정리 (컴포넌트 언마운트 시)
  const cleanup = () => {
    clearMarkers();
    if (originMarker.value) {
      originMarker.value.setMap(null);
      originMarker.value = null;
    }
    if (currentLocationMarker.value) {
      currentLocationMarker.value.setMap(null);
      currentLocationMarker.value = null;
    }
    if (routePolyline.value) {
      routePolyline.value.setMap(null);
      routePolyline.value = null;
    }
    searchResults.value = [];
    selectedPlace.value = null;
    originLocation.value = null;
    map.value = null;
    places.value = null;
    infoWindow.value = null;
  };

  return {
    map,
    places,
    infoWindow,
    markers,
    cityOptions,
    districtOptions,
    bankOptions,
    selectedCity,
    selectedDistrict,
    selectedBank,
    allData,
    currentLocation,
    routePolyline,
    originLocation,
    originSearchKeyword,
    originMarker,
    searchResults,
    selectedPlace,
    currentLocationMarker,
    loadKakaoScript,
    initializeMap,
    loadData,
    updateDistrictOptions,
    placesSearchCallback,
    clearMarkers,
    handleSearch,
    drawRoute,
    setOriginToCurrentLocation,
    setOrigin,
    searchOrigin,
    searchBankNearby,
    searchBankByRegion,
    displayBankMarkers,
    showBankInfoWindow,
    selectBank,
    cleanup,
  };
})