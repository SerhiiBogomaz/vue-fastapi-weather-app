<template>
  <div class="wrapper">
    <h1>Editing Profile</h1>
    <form @submit.prevent="save" enctype="multipart/form-data">
      <input v-model="user.username" disabled />
      <input v-model="user.email" disabled />
      <input v-model="user.weather_api_key" placeholder="API Key" />
      <div v-if="avatarFullUrl" class="current-avatar">
        <p>Current avatar:</p>
        <img :src="avatarFullUrl" alt="Avatar" class="avatar-preview" />
        <label>
          <input type="checkbox" v-model="deleteAvatar" />
          Delete avatar
        </label>
      </div>
      <div class="custom-file">
        <label class="file-label">
          <span>Upload Avatar</span>
          <input type="file" @change="handleFile" accept="image/*" />
        </label>
        <p class="file-name" v-if="avatarFile">{{ avatarFile.name }}</p>
      </div>

      <div class="actions">
        <button type="submit">Save</button>
        <button type="button" class="cancel" @click.prevent="router.push('/home')">Cancel</button>
        <button type="button" class="delete" @click.prevent="remove">Delete Profile</button>
      </div>
    </form>
    <div v-if="toast.visible" :class="['toast', toast.type]">
        {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const user = ref({ username: '', email: '', weather_api_key: '', avatar_url: null })
const avatarFile = ref(null)
const deleteAvatar = ref(false)
const router = useRouter()

const avatarFullUrl = computed(() => {
  const path = user.value.avatar_url
  if (!path || typeof path !== 'string' || path.trim() === '') return null
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  return `${import.meta.env.VITE_API_URL}${path.startsWith('/') ? path : '/' + path}`
})

const STORAGE_KEY = 'editProfileData'

onMounted(async () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    user.value = JSON.parse(saved)
  }

  try {
    const res = await axios.get('/api/v1/users/me')
    user.value = res.data
    localStorage.setItem(STORAGE_KEY, JSON.stringify(user.value))
  } catch (error) {
    router.push('/')
  }
})

watch(
  () => user.value.weather_api_key,
  (newVal) => {
    const toSave = {
      username: user.value.username,
      email: user.value.email,
      weather_api_key: newVal,
      avatar_url: user.value.avatar_url,
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave))
  }
)

function handleFile(event) {
  avatarFile.value = event.target.files[0]
}

const toast = ref({
  visible: false,
  message: '',
  type: 'success'
})

function showToast(message, type = 'success', duration = 3000) {
  toast.value.message = message
  toast.value.type = type
  toast.value.visible = true
  setTimeout(() => {
    toast.value.visible = false
  }, duration)
}

async function save() {
try {
    const formData = new FormData()
    formData.append('weather_api_key', user.value.weather_api_key)

    if (avatarFile.value) {
      formData.append('avatar', avatarFile.value)
    }

    if (deleteAvatar.value) {
      formData.append('delete_avatar', 'true')
    }

    await axios.patch('/api/v1/users/me/update', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    const res = await axios.get('/api/v1/users/me')
    user.value = res.data
    avatarFile.value = null
    deleteAvatar.value = false
    localStorage.setItem(STORAGE_KEY, JSON.stringify(user.value))
    showToast('Profile saved successfully', 'success')
  } catch (error) {
    console.error(error)
    showToast('Failed to save profile', 'error')
  }
}

async function remove() {
  try {
    const token = localStorage.getItem('token');

    if (!token) {
      console.warn('No token found in localStorage');
      showToast('You are not authenticated', 'error');
      return;
    }

    console.log('Sending DELETE request to /api/v1/users/me/delete');
    console.log('Token:', token);

    const response = await axios.delete('/api/v1/users/me/delete', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    console.log('Delete success:', response);

    localStorage.removeItem('token');
    localStorage.removeItem(STORAGE_KEY);
    delete axios.defaults.headers.common['Authorization'];
    router.push('/');
    showToast('Profile deleted successfully', 'success');
  } catch (err) {
    console.error('Delete failed:', err);

    if (err.response) {
      console.warn('Server response:', err.response.status, err.response.data);
    }

    showToast('Failed to delete profile', 'error');
  }
}
</script>

<style scoped>
.actions {
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.current-avatar {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  padding: 10px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.avatar-preview {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border: 2px solid white;
}

.current-avatar label {
  display: flex;
  flex-direction: column;
  font-weight: bold;
  font-size: 14px;
  color: #333;
}

.current-avatar input[type="checkbox"] {
  margin-top: 8px;
  transform: scale(1.2);
}

.current-avatar input[type="checkbox"] {
  margin-top: 8px;
  transform: scale(1.2);
  box-shadow: none;
}

.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  min-width: 200px;
  padding: 12px 20px;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  z-index: 9999;
  opacity: 0.95;
  user-select: none;
  transition: opacity 0.3s ease;
}

.toast.success {
  background-color: #4caf50;
}

.toast.error {
  background-color: #f44336;
}
</style>
