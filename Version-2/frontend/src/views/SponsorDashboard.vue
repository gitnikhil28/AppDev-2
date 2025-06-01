<template>
  <div>
    <SponsorNavbar />
    <div class="container mt-4">
      <h2 class="text-center">Welcome to Your Dashboard</h2>
      <p class="text-center">Here you can manage your ad requests, profile, and search for campaigns.</p>
    </div>
  </div>
</template>

<script>
import SponsorNavbar from '@/components/SponsorNavbar.vue';

export default {
  components: {
    SponsorNavbar
  }
};
</script>

<style scoped>
.container {
  margin-top: 50px;
}
</style>