<template>
  <div>
    <div class="container mt-5">
      <h2 class="text-center mb-4">Login</h2>
      <form @submit.prevent="login" class="form-container">
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="form-control form-control-sm"
            placeholder="Enter your email"
            required
            aria-label="Email"
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-control form-control-sm"
            placeholder="Enter your password"
            required
            aria-label="Password"
          />
        </div>

        <button type="submit" class="btn btn-success w-100 py-2 mt-3">Login</button>

        <div v-if="error" class="alert alert-danger mt-3 text-center">
          {{ error }}
        </div>
      </form>

      <div class="text-center mt-4">
        <router-link to="/register/sponsor" class="text-decoration-none">
          Register as Sponsor
        </router-link>
        <br />
        <router-link to="/register/influencer" class="text-decoration-none">
          Register as Influencer
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      error: null,
    };
  },
  methods: {
    async login() {
      this.error = null;
      try {
        const response = await axios.post('http://localhost:5000/auth/login', {
          email: this.email,
          password: this.password,
        });

        // Store the JWT token in local storage
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem("user_id", response.data.user_id); // Save user_id for later use
        localStorage.setItem("role", response.data.role);

        // Redirect based on user role
        if (response.data.role === 'sponsor') {
          this.$router.push('/sponsor/profile');
        } else if (response.data.role === 'influencer') {
          this.$router.push('/influencer/profile');
        } else if (response.data.role === 'admin') {
          this.$router.push('/admin/users');
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Invalid credentials';
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin-top: 50px;
}

.form-container {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.form-control-sm {
  font-size: 0.875rem;
  padding: 0.375rem 0.75rem;
}

button {
  font-size: 1rem;
  padding: 12px;
}

button:hover {
  background-color: #388e56;
}

.alert {
  font-size: 0.875rem;
  margin-top: 10px;
}

.text-center {
  text-align: center;
}

.mt-3 {
  margin-top: 1rem;
}

.mb-3 {
  margin-bottom: 1rem;
}
</style>
