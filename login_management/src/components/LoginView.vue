<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">Đăng nhập</h2>
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-gray-700">Tên đăng nhập</label>
          <input type="username" v-model="username" required
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div>
          <label class="block text-gray-700">Mật khẩu</label>
          <input type="password" v-model="password" required
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <button type="submit"
          class="w-full py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition">
          Đăng nhập
        </button>
      </form>
      <p v-if="error" class="mt-4 text-red-500 text-center">{{ error }}</p>

      <button @click="goToRegister"
        class="mt-4 w-full py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg hover:bg-gray-300 transition">
        Đăng ký tài khoản mới
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router'; // Import useRouter để sử dụng router trong setup() nếu dùng Composition API, nhưng ở đây dùng Options API

export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async onSubmit() {
      this.error = '';
      try {
        const res = await axios.post('http://localhost:8000/api/login/', {
          username: this.username,
          password: this.password
        });
        const token = res.data.access_token;
        localStorage.setItem('token', token);
        this.$router.push('/customer_profile'); // Chuyển hướng sau khi đăng nhập thành công
      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
          this.error = err.response.data.detail;
        } else {
          this.error = 'Không thể kết nối server.';
        }
      }
    },
    // Phương thức mới để chuyển hướng đến trang đăng ký
    goToRegister() {
      this.$router.push('/register'); // Thay '/register' bằng đường dẫn thực tế đến form đăng ký của bạn
    }
  }
}
</script>