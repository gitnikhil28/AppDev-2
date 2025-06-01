<template>
  <div>
    <SponsorNavbar />
    <div class="container mt-4">
      <div v-if="campaign">
        <h2 class="text-center mb-4">{{ campaign.name }}</h2>
        <p><strong>Description:</strong> {{ campaign.description }}</p>
        <p><strong>Start Date:</strong> {{ campaign.start_date }}</p>
        <p><strong>End Date:</strong> {{ campaign.end_date }}</p>
        <p><strong>Budget:</strong> ${{ campaign.budget }}</p>
        <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>
        
      </div>
      <div v-else>
        <p>Loading campaign details...</p>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import SponsorNavbar from '@/components/SponsorNavbar.vue';

export default {
  components: {
    SponsorNavbar,
  },
  data() {
    return {
      campaign: null, // Holds the campaign data
    };
  },
  async mounted() {
    this.fetchCampaignDetails();
  },
  methods: {
    async fetchCampaignDetails() {
      try {
        const campaignId = this.$route.params.id; // Get the campaign ID from the route
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:5000/sponsor/campaign/${campaignId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.campaign = response.data;
      } catch (error) {
        console.error(error);
        alert('Failed to load campaign details.');
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin-top: 20px;
}

p {
  font-size: 1rem;
  line-height: 1.6;
}
</style>
