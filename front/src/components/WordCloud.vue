<!-- components/WordCloud.vue -->
<template>
  <div class="word-cloud-container">
    <div v-if="loading" class="loading-message">Loading word cloud data...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <vue-wordcloud
        v-else-if="sortedWords.length"
        :words="sortedWords"
        :color="colorOptions"
        :font-family="fontFamily"
        :font-size="fontSizeMapper"
        :rotation="rotationMapper"
        :spacing="spacing"
        @word-click="onWordClick"
    />
    <div v-else class="no-data-message">No words available for the cloud.</div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import VueWordCloud from 'vue-wordcloud'

export default {
  name: 'WordCloud',
  components: {
    VueWordCloud
  },
  props: {
    maxWords: {
      type: Number,
      default: 100
    },
    valueKey: {
      type: String,
      default: 'value'
    }
  },
  setup(props) {
    const loading = ref(true)
    const error = ref(null)
    const data = ref([])

    const colorOptions = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    const fontFamily = 'Arial, sans-serif'
    const spacing = 5

    const fontSizeMapper = (word) => Math.log2(word[props.valueKey]) * 5 + 16
    const rotationMapper = () => ~~(Math.random() * 2) * 90

    const sortedWords = computed(() => {
      if (!data.value || !Array.isArray(data.value)) {
        return []
      }
      return [...data.value]
          .sort((a, b) => parseFloat(b[props.valueKey]) - parseFloat(a[props.valueKey]))
          .slice(0, props.maxWords)
    })

    const fetchWords = async () => {
      // Simulating API call with dummy data
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve([
            { text: 'Vue', value: 100 },
            { text: 'React', value: 80 },
            { text: 'Angular', value: 70 },
            { text: 'JavaScript', value: 90 },
            { text: 'TypeScript', value: 75 },
            { text: 'HTML', value: 85 },
            { text: 'CSS', value: 85 },
            { text: 'Webpack', value: 65 },
            { text: 'Vite', value: 60 },
            { text: 'Node.js', value: 70 },
            { text: 'Express', value: 55 },
            { text: 'MongoDB', value: 50 },
            { text: 'SQL', value: 60 },
            { text: 'Git', value: 75 },
            { text: 'Docker', value: 45 },
            { text: 'AWS', value: 40 },
            { text: 'Redux', value: 55 },
            { text: 'Vuex', value: 50 },
            { text: 'Jest', value: 40 },
            { text: 'Cypress', value: 35 },
          ])
        }, 1000)
      })
    }

    onMounted(async () => {
      try {
        data.value = await fetchWords()
      } catch (e) {
        console.error('Error fetching word cloud data:', e)
        error.value = 'Failed to load word cloud data. Please try again later.'
      } finally {
        loading.value = false
      }
    })

    const onWordClick = (word) => {
      console.log('Word clicked:', word)
      // Implement any click handling logic here
    }

    return {
      loading,
      error,
      sortedWords,
      colorOptions,
      fontFamily,
      fontSizeMapper,
      rotationMapper,
      spacing,
      onWordClick
    }
  }
}
</script>

<style scoped>
.word-cloud-container {
  width: 100%;
  height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
}

.loading-message,
.error-message,
.no-data-message {
  font-size: 18px;
  color: #666;
  text-align: center;
}

.error-message {
  color: #d32f2f;
}
</style>