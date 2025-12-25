/**
 * @파일명 youtube/youtube.js
 * @설명 YouTube Data API v3 호출 모듈
 * @기능
 *   - 동영상 검색 (searchVideos)
 *   - 동영상 상세 조회 (fetchVideoDetail)
 * @API엔드포인트
 *   - GET /search : 동영상 검색
 *   - GET /videos : 동영상 상세 정보
 * @환경변수 VITE_YOUTUBE_API_KEY: YouTube API 키
 */

import axios from 'axios'

// YouTube Data API v3 Axios 인스턴스
const api = axios.create({
  baseURL: 'https://www.googleapis.com/youtube/v3',
  params: {
    key: import.meta.env.VITE_YOUTUBE_API_KEY,
  },
})

/**
 * 동영상 검색
 * @description 키워드로 YouTube 동영상을 검색합니다
 * @param {string} q - 검색 키워드
 * @returns {Promise<Array>} 검색 결과 동영상 배열 (최대 12개)
 */
export async function searchVideos(q) {
  const { data } = await api.get('/search', {
    params: {
      part: 'snippet',
      type: 'video',
      maxResults: 12,
      q,
    },
  })
  return data.items
}

/**
 * 동영상 상세 조회
 * @description 동영상 ID로 상세 정보를 가져옵니다
 * @param {string} id - YouTube 동영상 ID
 * @returns {Promise<Object|null>} 동영상 상세 정보 (snippet, contentDetails, statistics)
 */
export async function fetchVideoDetail(id) {
  const { data } = await api.get('/videos', {
    params: {
      part: 'snippet,contentDetails,statistics',
      id,
    },
  })
  return data.items?.[0] ?? null
}
