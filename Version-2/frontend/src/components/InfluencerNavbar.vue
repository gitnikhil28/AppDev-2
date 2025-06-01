<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Influencer Dashboard</a>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">   

            <router-link class="nav-link   
 active" aria-current="page" to="/influencer/dashboard"></router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/influencer/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/influencer/find_campaigns">Campaigns</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/influencer/list_ad_requests">Ad requests</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default   
 {
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.navbar {
  background-color: lightblue;
}

.navbar-nav {
  display: flex;
  gap: 5px; 
}

.navbar-nav .nav-link.active {
  font-weight: bold;
}
</style>