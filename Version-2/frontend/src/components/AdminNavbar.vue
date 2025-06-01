<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Admin Dashboard</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/admin/users" class="nav-link">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/campaigns" class="nav-link">Campaigns</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/sponsor_approvals" class="nav-link">Sponsor Approvals</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/stats" class="nav-link">Stats</router-link>
          </li>
          <li class="nav-item">
            <button class="btn btn-danger" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    logout() {
      // Handle logout logic here (e.g., remove token from localStorage)
      localStorage.removeItem("token");
      this.$router.push("/login"); // Redirect to login page
    }
  }
};
</script>

<style scoped>
.navbar {
  margin-bottom: 20px;
}

.navbar-brand {
  font-size: 1.5rem;
}

.nav-item .nav-link {
  font-size: 1.1rem;
}

.nav-item .btn-danger {
  font-size: 1.1rem;
}
</style>
