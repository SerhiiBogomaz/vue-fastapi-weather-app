<template>
  <div class="wrapper">
    <div class="header">
      <img :src="fullAvatarUrl" class="avatar" />
      <span class="username" @click="goToProfile">{{ user.username }}</span>
      <button class="logout-btn" @click="logout">Log Out</button>
    </div>
    <WeatherWidget :apiKey="user.weather_api_key" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import WeatherWidget from '../components/WeatherWidget.vue'
import defaultAvatar from '@/assets/defaultAvatar.svg'

const user = ref({ username: '', avatar_url: '', weather_api_key: '' })
const router = useRouter()

const fullAvatarUrl = computed(() => {
  if (user.value.avatar_url?.startsWith('/static/')) {
    return `${import.meta.env.VITE_API_URL}${user.value.avatar_url}`
  }
  return user.value.avatar_url || defaultAvatar
})

function goToProfile() {
  router.push('/edit-profile')
}

function logout() {
  localStorage.removeItem('token')
  delete axios.defaults.headers.common['Authorization']
  router.push('/')
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/')
    return
  }

  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  try {
    const res = await axios.get('/api/v1/users/me')
    user.value = res.data
  } catch (err) {
    localStorage.removeItem('token')
    router.push('/')
  }
})
</script>

<style scoped>
.header {
  position: absolute;
  top: 20px;
  right: 30px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.username {
  cursor: pointer;
  color: white;
  font-size: 1.2rem;
  font-family: "Rubik Dirt", system-ui;
  text-shadow: 1px 1px 3px #000;
}
</style>
