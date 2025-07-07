<template>
  <div class="wrapper">
    <h1>Authorization</h1>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <p class="error" v-if="error">{{ error }}</p>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function login() {
  try {
    const res = await axios.post('/api/v1/users/login', { email: email.value, password: password.value })
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`
    localStorage.setItem('token', res.data.access_token)
    router.push('/home')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login error'
  }
}
</script>

<style scoped>
input,
button {
  display: block;
  margin-top: 10px;
  width: 100%;
  max-width: 500px;
  padding: 15px 25px;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-family: sans-serif;
  font-weight: 400;
  color: #333;
  box-sizing: border-box;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

input::placeholder {
  color: #666;
  opacity: 1;
}

input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(253, 187, 45, 0.5);
}

button {
  background: #2A7B9B;
  color: white;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

button:hover {
  background: #1e5a75;
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.error {
  color: #bd2f2f;
  margin-top: 5px;
  text-align: center;
  font-family: sans-serif;
}
</style>
