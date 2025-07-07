<template>
  <div class="weather-widget">
    <h1>Weather in your city</h1>
    <p class="description">Do you want to know weather in {{ city === '' ? 'your city' : cityName }}?</p>

    <input type="text" v-model="city" placeholder="Enter city" />
    <button v-show="city !== ''" @click="getWeather">Get weather for your city</button>

    <p class="error" v-if="error">{{ error }}</p>

    <div v-if="info" class="weather-result">
        <p><strong>City:</strong> {{ info.name }}</p>
        <p><strong>Temperature:</strong> {{ info.main?.temp ?? 'N/A' }} °C</p>
        <p><strong>Weather:</strong> {{ info.weather?.[0]?.description ?? 'N/A' }}</p>
        <p><strong>Humidity:</strong> {{ info.main?.humidity ?? 'N/A' }}%</p>
        <p><strong>Wind:</strong> {{ info.wind?.speed ?? 'N/A' }} m/s</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    apiKey: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      city: '',
      error: '',
      info: null
    }
  },
  computed: {
    cityName() {
      return this.city
    }
  },
  methods: {
    async getWeather() {
      if (this.city.trim().length < 2) {
        this.error = 'Need more than one letter'
        this.info = null
        return
      }

      this.error = ''
      this.info = null

      try {
        const res = await axios.get('/api/v1/users/weather', {
          params: {
            city: this.city,
            api_key: this.apiKey
          }
        })
        this.info = res.data
      } catch (err) {
        if (err.response && err.response.data && err.response.data.message) {
          this.error = err.response.data.message
        } else if (err.response && err.response.data && err.response.data.detail) {
          this.error = err.response.data.detail
        } else {
          this.error = 'City not found or API error'
        }
        this.info = null
        console.error(err)
      }
    }
  }
}
</script>

<style scoped>
.weather-widget {
  width: 100%;
  max-width: 500px;
  margin-top: 20px;
}

.description {
  margin-bottom: 15px;
  text-align: center;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.error {
  color: #bd2f2f;
  margin-top: 10px;
  font-size: 0.9rem;
  text-align: center;
  font-family: 'Roboto Condensed', sans-serif;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.weather-result {
  margin-top: 20px;
  text-align: center;
  color: #fff;
  font-size: 1.1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.weather-result p {
  margin: 6px 0;
}

button {
  margin-top: 15px;
}
</style>
