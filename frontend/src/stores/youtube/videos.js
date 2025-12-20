import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useVideoStore = defineStore("video", () => {
  const savedVideos = ref([])

  const isSaved = computed(() => {
    return (videoId) => savedVideos.value.some(v => v.id === videoId)
  })

  const toggleVideo = function (video) {
    const exists = savedVideos.value.some(v => v.id === video.id)
    
    if (exists) {
      savedVideos.value = savedVideos.value.filter(v => v.id !== video.id)
    }
    else {
      savedVideos.value.unshift(video)
    }
  }

  const removeVideo = function (videoId) {
    savedVideos.value = savedVideos.value.filter(v => v.id !== videoId)
  }

  const clearVideos = function () {
    savedVideos.value = []
  }

  return {savedVideos, isSaved, toggleVideo, removeVideo, clearVideos}
}, {persist: true})