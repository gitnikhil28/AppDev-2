<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Sponsor Dashboard</a>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">   

            <router-link class="nav-link   
 active" aria-current="page" to="/sponsor/dashboard"></router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/sponsor/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/sponsor/campaigns">Campaigns</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/sponsor/ad_requests">Ad Requests</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/sponsor/search_influencers">Find Influencers</router-link>
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