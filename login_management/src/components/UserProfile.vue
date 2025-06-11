<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">Thông tin người dùng</h2>

      <div v-if="user" class="space-y-4 text-gray-700">
        <p><strong>Tên người dùng:</strong> <span v-html="user.fullname"></span></p>
        <p><strong>Địa chỉ:</strong> <span v-html="user.address || 'Chưa cập nhật'"></span></p>
        <p><strong>Số điện thoại:</strong> <span v-html="user.phonenumber || 'Chưa cập nhật'"></span></p>
        <p><strong>Sinh nhật:</strong> {{ formatDate(user.birthday) }}</p>
      </div>

      <p v-else-if="loading" class="text-center text-indigo-600">Đang tải thông tin...</p>
      <p v-else-if="error" class="text-red-500 text-center">{{ error }}</p>

      <button @click="logout"
        class="mt-6 w-full py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition">
        Đăng xuất
      </button>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'UserProfile',
  data() {
    return {
      user: null,
      loading: true,
      error: ''
    };
  },
  async created() {
    // Khi component được tạo, gọi API để lấy thông tin người dùng
    await this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      this.loading = true;
      this.error = '';
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = 'Bạn chưa đăng nhập. Vui lòng đăng nhập để xem thông tin.';
          this.loading = false;
          // Chuyển hướng về trang đăng nhập nếu không có token
          this.$router.push('/');
          return;
        }
        const res = await axios.get('http://localhost:8000/api/customer/me/', {
          headers: {
            'Authorization': `Bearer ${token}` // Gửi JWT trong header Authorization
          }
        });
        this.user = res.data;
      } catch (err) {
        console.error('Lỗi khi lấy thông tin người dùng:', err);
        if (err.response) {
          if (err.response.status === 401) {
            this.error = 'Phiên đăng nhập đã hết hạn hoặc không hợp lệ. Vui lòng đăng nhập lại.';
            this.logout(); // Đăng xuất tự động nếu token hết hạn/không hợp lệ
          } else {
            this.error = err.response.data.detail || 'Không thể tải thông tin người dùng.';
          }
        } else {
          this.error = 'Không thể kết nối tới máy chủ API.';
        }
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('vi-VN', options);
    },
    logout() {
      localStorage.removeItem('token'); // Xóa token khỏi Local Storage
      // Chuyển hướng người dùng về trang đăng nhập
      this.$router.push('/');
    }
  }
};
</script>

