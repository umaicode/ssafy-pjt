// Youtube api 호출
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://www.googleapis.com/youtube/v3',
  params: {
    key: import.meta.env.VITE_YOUTUBE_API_KEY,
  },
})

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

export async function fetchVideoDetail(id) {
  const { data } = await api.get('/videos', {
    params: {
      part: 'snippet,contentDetails,statistics',
      id,
    },
  })
  return data.items?.[0] ?? null
}
