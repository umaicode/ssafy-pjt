<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { Chart } from 'chart.js/auto'

const props = defineProps({
  labels: Array,
  prices: Array,
  metal: String,
})

const canvas = ref(null)
let chart = null

const drawChart = () => {
  if (chart) chart.destroy()

  chart = new Chart(canvas.value, {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: [
        {
          label: props.metal === 'gold' ? 'Gold Price' : 'Silver Price',
          data: props.prices,
          borderColor: props.metal === 'gold' ? 'gold' : 'gray',
          tension: 0.2,
        }
      ]
    }
  })
}

onMounted(drawChart)

watch(() => [props.labels, props.prices, props.metal], drawChart)
</script>
