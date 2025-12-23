<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { Chart } from 'chart.js/auto'

const props = defineProps({
  labels: Array,
  prices: Array,
  metal: String,
})

const canvas = ref(null)
let chart = null

// 테마 감지
const isDarkMode = () => document.documentElement.getAttribute('data-theme') === 'dark'

// 색상 팔레트
const getColors = () => {
  const isGold = props.metal === 'gold'
  const dark = isDarkMode()
  
  return {
    primary: isGold ? '#FFB800' : '#AD88C6',
    secondary: isGold ? '#FFA500' : '#7469B6',
    gradient1: isGold ? 'rgba(255, 184, 0, 0.4)' : 'rgba(173, 136, 198, 0.4)',
    gradient2: isGold ? 'rgba(255, 184, 0, 0.05)' : 'rgba(116, 105, 182, 0.05)',
    gridColor: dark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)',
    textColor: dark ? '#e4e4e7' : '#52525b',
    tooltipBg: dark ? '#27272a' : '#ffffff',
    tooltipText: dark ? '#e4e4e7' : '#18181b',
  }
}

const drawChart = () => {
  if (chart) chart.destroy()
  if (!canvas.value || !props.labels?.length || !props.prices?.length) return

  const ctx = canvas.value.getContext('2d')
  const colors = getColors()

  // 그라데이션 생성
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.value.offsetHeight || 300)
  gradient.addColorStop(0, colors.gradient1)
  gradient.addColorStop(1, colors.gradient2)

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: [
        {
          label: props.metal === 'gold' ? 'Gold Price (USD/oz)' : 'Silver Price (USD/oz)',
          data: props.prices,
          borderColor: colors.primary,
          backgroundColor: gradient,
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          pointHoverRadius: 8,
          pointHoverBackgroundColor: colors.primary,
          pointHoverBorderColor: '#fff',
          pointHoverBorderWidth: 3,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 1200,
        easing: 'easeInOutQuart',
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'end',
          labels: {
            color: colors.textColor,
            font: {
              size: 12,
              weight: '600',
              family: "'Pretendard', sans-serif",
            },
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 20,
          }
        },
        tooltip: {
          enabled: true,
          backgroundColor: colors.tooltipBg,
          titleColor: colors.tooltipText,
          bodyColor: colors.tooltipText,
          titleFont: {
            size: 13,
            weight: '700',
            family: "'Pretendard', sans-serif",
          },
          bodyFont: {
            size: 14,
            weight: '600',
            family: "'Pretendard', sans-serif",
          },
          padding: 14,
          cornerRadius: 12,
          displayColors: true,
          boxPadding: 6,
          borderColor: colors.primary,
          borderWidth: 1,
          callbacks: {
            label: function(context) {
              const value = context.parsed.y
              return ` $${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: colors.textColor,
            font: {
              size: 11,
              weight: '500',
              family: "'Pretendard', sans-serif",
            },
            maxRotation: 0,
            maxTicksLimit: 8,
          },
          border: {
            display: false,
          }
        },
        y: {
          grid: {
            color: colors.gridColor,
            lineWidth: 1,
          },
          ticks: {
            color: colors.textColor,
            font: {
              size: 11,
              weight: '500',
              family: "'Pretendard', sans-serif",
            },
            padding: 12,
            callback: function(value) {
              return '$' + value.toLocaleString()
            }
          },
          border: {
            display: false,
          }
        }
      }
    }
  })
}

// 테마 변경 감지
const handleThemeChange = () => {
  drawChart()
}

onMounted(() => {
  drawChart()
  // 테마 변경 감지
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'data-theme') {
        handleThemeChange()
      }
    })
  })
  observer.observe(document.documentElement, { attributes: true })
})

onUnmounted(() => {
  if (chart) chart.destroy()
})

watch(() => [props.labels, props.prices, props.metal], drawChart, { deep: true })
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 320px;
  padding: 16px;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.8), rgba(249, 250, 251, 0.9));
  border-radius: 16px;
  box-shadow: 
    0 4px 20px rgba(116, 105, 182, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(116, 105, 182, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.chart-container:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px rgba(116, 105, 182, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

/* Dark Mode */
[data-theme="dark"] .chart-container {
  background: linear-gradient(145deg, rgba(39, 39, 42, 0.9), rgba(24, 24, 27, 0.95));
  border-color: rgba(116, 105, 182, 0.2);
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .chart-container:hover {
  box-shadow: 
    0 8px 30px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
</style>
