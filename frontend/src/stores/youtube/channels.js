import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useChannelStore = defineStore("channel", () => {
  const savedChannels = ref([])

  const isSaved = computed(() => {
    return (channelId) => savedChannels.value.some(c => c.id === channelId)
  })

  const toggleChannel = function (channel) {
    const exists = savedChannels.value.some(c => c.id === channel.id)

    if (exists) {
      savedChannels.value = savedChannels.value.filter(c => c.id !== channel.id)
    }
    else {
      savedChannels.value.unshift(channel)
    }
  }

  const removeChannel = function (channelId) {
    savedChannels.value = savedChannels.value.filter(c => c.id !== channelId)
  }

  const clearChannels = function () {
    savedChannels.value = []
  }

  return {savedChannels, isSaved, toggleChannel, removeChannel, clearChannels}
}, {persist: true})