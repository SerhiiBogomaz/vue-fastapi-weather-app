<template>
  <div class="wrapper">
    <h1>Welcome</h1>
    <button @click="goTo('login')">Login</button>
    <button @click="goTo('register')">Register</button>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { onMounted } from 'vue'
const router = useRouter()
const route = useRoute()

function goTo(page) {
  router.push(`/${page}`)
}

onMounted(() => {
  const token = localStorage.getItem('token')
  if (token && route.path === '/') {
    router.push('/home')
  }
})
</script>
