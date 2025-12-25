<template>
  <div class="stock-chart">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import 'chartjs-adapter-date-fns'

// Chart.js 등록
Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  currency: {
    type: String,
    default: 'USD'
  }
})

const chartCanvas = ref(null)
let chartInstance = null

const createChart = () => {
  if (!chartCanvas.value || !props.data.length) return

  // 기존 차트 제거
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')

  // 데이터 준비 - 날짜 형식 안전하게 처리
  const processedData = props.data.map(item => {
    let date
    try {
      // ISO 문자열을 Date 객체로 변환
      date = new Date(item.date)
      // Invalid Date 체크
      if (isNaN(date.getTime())) {
        // 다른 형식으로 시도
        const dateStr = item.date.toString().replace('T', ' ').replace('Z', '')
        date = new Date(dateStr)
        if (isNaN(date.getTime())) {
          // 마지막으로 현재 시간 사용
          date = new Date()
        }
      }
    } catch (e) {
      console.warn('날짜 파싱 실패:', item.date, e)
      date = new Date()
    }
    
    return {
      date,
      close: item.close || 0
    }
  }).sort((a, b) => a.date - b.date) // 날짜 순으로 정렬

  const labels = processedData.map(item => item.date)
  const prices = processedData.map(item => item.close)

  // 그라데이션 생성
  const gradient = ctx.createLinearGradient(0, 0, 0, 300)
  gradient.addColorStop(0, 'rgba(102, 126, 234, 0.3)')
  gradient.addColorStop(1, 'rgba(102, 126, 234, 0.0)')

  // 가격 변동에 따른 색상 결정
  const firstPrice = prices[0]
  const lastPrice = prices[prices.length - 1]
  const isPositive = lastPrice >= firstPrice

  const lineColor = isPositive ? '#10b981' : '#ef4444'
  const fillGradient = ctx.createLinearGradient(0, 0, 0, 300)
  fillGradient.addColorStop(0, isPositive ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)')
  fillGradient.addColorStop(1, 'rgba(255, 255, 255, 0)')

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: '가격',
        data: prices,
        borderColor: lineColor,
        backgroundColor: fillGradient,
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: lineColor,
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#1f2937',
          bodyColor: '#4b5563',
          borderColor: '#e5e7eb',
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            title: (items) => {
              if (items.length > 0) {
                try {
                  const item = items[0]
                  let date
                  
                  // Chart.js time scale에서는 parsed.x가 실제 timestamp
                  if (item.parsed && item.parsed.x) {
                    date = new Date(item.parsed.x)
                  } 
                  // 또는 dataIndex를 사용해서 원본 labels에서 가져오기
                  else if (typeof item.dataIndex === 'number' && labels[item.dataIndex]) {
                    date = labels[item.dataIndex]
                  }
                  // 마지막으로 label 사용
                  else {
                    date = new Date(item.label)
                  }
                  
                  // Invalid Date 체크
                  if (isNaN(date.getTime())) {
                    console.warn('Invalid date:', { 
                      parsed: item.parsed, 
                      label: item.label, 
                      dataIndex: item.dataIndex,
                      labelsLength: labels.length 
                    })
                    return '날짜 정보 없음'
                  }
                  
                  return date.toLocaleDateString('ko-KR', {
                    year: 'numeric',
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })
                } catch (e) {
                  console.warn('Tooltip 날짜 포맷 실패:', e)
                  return '날짜 정보 없음'
                }
              }
              return ''
            },
            label: (item) => {
              const price = item.raw
              if (props.currency === 'KRW') {
                return `₩${price.toLocaleString('ko-KR', { maximumFractionDigits: 0 })}`
              }
              return `$${price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
            }
          }
        }
      },
      scales: {
        x: {
          type: 'time',
          time: {
            displayFormats: {
              minute: 'HH:mm',
              hour: 'HH:mm',
              day: 'MM/dd',
              week: 'MM/dd',
              month: 'yyyy/MM'
            }
          },
          grid: {
            display: false
          },
          ticks: {
            color: '#9ca3af',
            font: {
              size: 11
            },
            maxTicksLimit: 8
          }
        },
        y: {
          position: 'right',
          grace: '10%',
          grid: {
            color: '#f3f4f6'
          },
          ticks: {
            color: '#9ca3af',
            font: {
              size: 11
            },
            callback: (value) => {
              if (props.currency === 'KRW') {
                return `₩${value.toLocaleString('ko-KR', { maximumFractionDigits: 0 })}`
              }
              return `$${value.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`
            }
          }
        }
      }
    }
  })
}

onMounted(() => {
  createChart()
})

watch(() => props.data, () => {
  createChart()
}, { deep: true })

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

<style scoped>
.stock-chart {
  width: 100%;
  height: 100%;
  min-height: 300px;
}

.stock-chart canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
