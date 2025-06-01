<template>
  <div>
    <InfluencerNavbar />
    <div class="container mt-4">
      <h2 class="text-center mb-4">{{ campaign.name }}</h2>
      <div v-if="campaign">
        <p><strong>Description:</strong> {{ campaign.description }}</p>
        <p><strong>Start Date:</strong> {{ campaign.start_date }}</p>
        <p><strong>End Date:</strong> {{ campaign.end_date }}</p>
        <p><strong>Budget:</strong> ${{ campaign.budget }}</p>
        <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>
        <p><strong>Sponsor:</strong> {{ campaign.sponsor_name }}</p>
        <p><strong>Goals:</strong> {{ campaign.goals }}</p>
      </div>
      <div v-else>
        <p>Loading campaign details...</p>
      </div>
      <div class="text-center mt-4">
        <button @click="sendAdRequest" class="btn btn-primary">Send Ad Request</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import InfluencerNavbar from '@/components/InfluencerNavbar.vue';

export default {
  components: {
    InfluencerNavbar,
  },
  data() {
    return {
      campaign: null, // Campaign details
    };
  },
  async mounted() {
    this.fetchCampaignDetails();
  },
  methods: {
    async fetchCampaignDetails() {
      try {
        const campaignId = this.$route.params.id; // Get campaign ID from route
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
    sendAdRequest() {
      const campaignId = this.$route.params.id;
      this.$router.push(`/influencer/ad_request/create/${campaignId}`); // Redirect to ad request creation page
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}

p {
  font-size: 1rem;
  line-height: 1.6;
}

button {
  margin-top: 20px;
}
</style>
