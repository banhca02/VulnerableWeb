<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">Đăng ký tài khoản mới</h2>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label for="username" class="block text-gray-700 text-sm font-bold mb-2">Tên đăng nhập</label>
          <input type="text" id="username" v-model="username" required
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Mật khẩu</label>
          <input type="password" id="password" v-model="password" required
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input type="email" id="email" v-model="email" required
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label for="fullname" class="block text-gray-700 text-sm font-bold mb-2">Họ và tên</label>
          <input type="text" id="fullname" v-model="fullname" required
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label for="address" class="block text-gray-700 text-sm font-bold mb-2">Địa chỉ</label>
          <input type="text" id="address" v-model="address"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label for="phonenumber" class="block text-gray-700 text-sm font-bold mb-2">Số điện thoại</label>
          <input type="tel" id="phonenumber" v-model="phonenumber"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label for="birthdate" class="block text-gray-700 text-sm font-bold mb-2">Ngày sinh</label>
          <input type="date" id="birthdate" v-model="birthdate"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <button type="submit"
          class="w-full py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition">
          Đăng ký
        </button>
      </form>

      <p v-if="successMessage" class="mt-4 text-green-600 text-center">{{ successMessage }}</p>
      <p v-if="error" class="mt-4 text-red-500 text-center">{{ error }}</p>

      <p class="mt-6 text-center text-gray-600">
        Đã có tài khoản?
        <router-link to="/" class="text-indigo-600 hover:underline">Đăng nhập ngay</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router'; // Dùng useRouter cho setup() nhưng không cần nếu dùng Options API
// Mẹo: Trong Options API, bạn dùng this.$router trực tiếp.

export default {
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      fullname: '',
      address: '',
      phonenumber: '',
      birthdate: '', // Sẽ là chuỗi định dạng YYYY-MM-DD
      successMessage: '',
      error: ''
    };
  },
  methods: {
    async onSubmit() {
      this.error = '';
      this.successMessage = '';

      // Chuẩn bị dữ liệu gửi đi
      const registerData = {
        username: this.username,
        password: this.password,
        email: this.email,
        fullname: this.fullname,
        address: this.address || null, // Gửi null nếu không có giá trị
        phonenumber: this.phonenumber || null,
        // birthdate phải là chuỗi ISO 8601 hoặc null/undefined.
        // Input type="date" thường trả về YYYY-MM-DD, phù hợp với datetime của Python/PostgreSQL
        birthdate: this.birthdate || null 
      };

      try {
        // Gửi yêu cầu POST đến API đăng ký của bạn
        // Đảm bảo URL này khớp với endpoint đăng ký ở backend của bạn
        const res = await axios.post('http://localhost:8000/api/register/', registerData); 
        
        this.successMessage = 'Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.';
        this.resetForm(); // Xóa dữ liệu form sau khi đăng ký thành công
        
        // Tùy chọn: Chuyển hướng người dùng đến trang đăng nhập sau một thời gian
        setTimeout(() => {
          this.$router.push('/');
        }, 2000); 

      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
          // Xử lý lỗi từ backend (ví dụ: tên đăng nhập đã tồn tại)
          this.error = err.response.data.detail;
        } else {
          this.error = 'Đã xảy ra lỗi khi đăng ký. Vui lòng thử lại.';
          console.error('Lỗi đăng ký:', err); // In ra console để debug
        }
      }
    },
    resetForm() {
      // Đặt lại các trường về giá trị ban đầu
      this.username = '';
      this.password = '';
      this.email = '';
      this.fullname = '';
      this.address = '';
      this.phonenumber = '';
      this.birthdate = '';
    }
  }
};
</script>
