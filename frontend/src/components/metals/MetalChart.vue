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

// 색상 팔레트 - 미니멀하고 프리미엄한 색상
const getColors = () => {
  const isGold = props.metal === 'gold'
  const dark = isDarkMode()
  
  if (isGold) {
    return {
      primary: dark ? '#F7D794' : '#D4AF37',
      gradient1: dark ? 'rgba(247, 215, 148, 0.25)' : 'rgba(212, 175, 55, 0.2)',
      gradient2: dark ? 'rgba(247, 215, 148, 0.02)' : 'rgba(212, 175, 55, 0.01)',
      gridColor: dark ? 'rgba(247, 215, 148, 0.05)' : 'rgba(212, 175, 55, 0.08)',
      textColor: dark ? '#d4d4d8' : '#52525b',
      tooltipBg: dark ? 'rgba(24, 24, 27, 0.95)' : 'rgba(255, 255, 255, 0.98)',
      tooltipText: dark ? '#F7D794' : '#D4AF37',
      tooltipBorder: dark ? '#F7D794' : '#D4AF37',
    }
  } else {
    return {
      primary: dark ? '#CBD5E1' : '#64748B',
      gradient1: dark ? 'rgba(203, 213, 225, 0.2)' : 'rgba(100, 116, 139, 0.15)',
      gradient2: dark ? 'rgba(203, 213, 225, 0.02)' : 'rgba(100, 116, 139, 0.01)',
      gridColor: dark ? 'rgba(203, 213, 225, 0.05)' : 'rgba(100, 116, 139, 0.08)',
      textColor: dark ? '#d4d4d8' : '#52525b',
      tooltipBg: dark ? 'rgba(24, 24, 27, 0.95)' : 'rgba(255, 255, 255, 0.98)',
      tooltipText: dark ? '#CBD5E1' : '#64748B',
      tooltipBorder: dark ? '#CBD5E1' : '#64748B',
    }
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
          label: props.metal === 'gold' ? 'Gold (USD/oz)' : 'Silver (USD/oz)',
          data: props.prices,
          borderColor: colors.primary,
          backgroundColor: gradient,
          borderWidth: 2,
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: colors.primary,
          pointHoverBorderColor: colors.tooltipBg,
          pointHoverBorderWidth: 2,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 2000,
        easing: 'easeInOutQuart',
        onProgress: function(animation) {
          const chart = animation.chart;
          const ctx = chart.ctx;
          const chartArea = chart.chartArea;
          
          if (!chartArea) return;
          
          const progress = animation.currentStep / animation.numSteps;
          const clipWidth = chartArea.left + (chartArea.right - chartArea.left) * progress;
          
          ctx.save();
          ctx.beginPath();
          ctx.rect(chartArea.left, chartArea.top, clipWidth - chartArea.left, chartArea.bottom - chartArea.top);
          ctx.clip();
        },
        onComplete: function(animation) {
          const chart = animation.chart;
          chart.ctx.restore();
        },
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
              weight: '500',
              family: "'Pretendard', -apple-system, sans-serif",
            },
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 16,
            boxWidth: 8,
            boxHeight: 8,
          }
        },
        tooltip: {
          enabled: true,
          backgroundColor: colors.tooltipBg,
          titleColor: colors.textColor,
          bodyColor: colors.tooltipText,
          titleFont: {
            size: 11,
            weight: '500',
            family: "'Pretendard', -apple-system, sans-serif",
          },
          bodyFont: {
            size: 15,
            weight: '600',
            family: "'Pretendard', -apple-system, sans-serif",
          },
          padding: 12,
          cornerRadius: 10,
          displayColors: false,
          borderColor: colors.tooltipBorder,
          borderWidth: 1,
          caretSize: 6,
          caretPadding: 8,
          callbacks: {
            label: function(context) {
              const value = context.parsed.y
              return `$${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
            },
            title: function(context) {
              return context[0].label || '';
            },
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
              size: 10,
              weight: '400',
              family: "'Pretendard', -apple-system, sans-serif",
            },
            maxRotation: 0,
            maxTicksLimit: 10,
          },
          border: {
            display: false,
          }
        },
        y: {
          grid: {
            color: colors.gridColor,
            lineWidth: 1,
            drawTicks: false,
          },
          ticks: {
            color: colors.textColor,
            font: {
              size: 10,
              weight: '400',
              family: "'Pretendard', -apple-system, sans-serif",
            },
            padding: 10,
            callback: function(value) {
              return '$' + value.toLocaleString()
            }
          },
          border: {
            display: false,
            dash: [4, 4],
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
  height: 400px;
  padding: 32px 24px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.05),
    0 1px 2px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chart-container:hover {
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.08),
    0 2px 4px rgba(0, 0, 0, 0.06);
  border-color: rgba(0, 0, 0, 0.1);
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

/* Dark Mode */
[data-theme="dark"] .chart-container {
  background: #18181b;
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.3),
    0 1px 2px rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .chart-container:hover {
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.4),
    0 2px 4px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.12);
}
</style>
