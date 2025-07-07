<template>
  <div class="wrapper">
    <h1>Registaration</h1>
    <form @submit.prevent="submit" enctype="multipart/form-data">
      <input v-model="form.username" placeholder="Name" required minlength="2" />
      <input type="email" v-model="form.email" placeholder="Email" required />
      <input v-model="form.weather_api_key" placeholder="API Key" />
      <div class="custom-file">
        <label class="file-label">
          <span>Upload Avatar</span>
          <input type="file" @change="handleFile" accept="image/*" />
        </label>
        <p class="file-name" v-if="avatarFile">{{ avatarFile.name }}</p>
      </div>
      <input type="password" v-model="form.password" placeholder="Password" required minlength="6" />
      <input type="password" v-model="confirm" placeholder="Confirm Password" required />
      <p class="error" v-if="error">{{ error }}</p>
      <button type="submit" class="custom-btn">Register</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  username: '',
  email: '',
  weather_api_key: '',
  password: '',
})

const avatarFile = ref(null)
const confirm = ref('')
const error = ref('')

function handleFile(event) {
  avatarFile.value = event.target.files[0]
}

async function submit() {
  if (form.value.password !== confirm.value) {
    error.value = 'The passwords do not match'
    return
  }

  const formData = new FormData()
  for (const key in form.value) {
    formData.append(key, form.value[key])
  }
  if (avatarFile.value) {
    formData.append('avatar', avatarFile.value)
  }

  try {
    const res = await axios.post('/api/v1/users/register', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`
    localStorage.setItem('token', res.data.access_token)
    router.push('/home')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Registration error'
  }
}
</script>

<style scoped>
input {
  font-family: sans-serif;
  font-weight: 400;
  color: #333;
}

input::placeholder {
  color: #666;
  opacity: 1;
}

input,
button {
  display: block;
  margin-top: 10px;
}

.error {
  color: #bd2f2f;
  margin: 5px auto 0;
  font-size: 0.85rem;
  text-align: center;
  max-width: 500px;
  word-wrap: break-word;
  display: block;

  font-family: 'Roboto Condensed', sans-serif;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.custom-file {
  margin-top: 10px;
  width: 100%;
  max-width: 500px;
}

.file-label {
  display: block;
  position: relative;
  overflow: hidden;
  text-align: center;
  font-family: sans-serif;
  font-weight: 500;
  color: white;
}

.file-label input[type="file"] {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-name {
  margin-top: 10px;
  text-align: center;
  color: white;
  font-size: 1rem;
}
</style>
