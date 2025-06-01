<template>
  <div>
    <InfluencerNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Find Campaigns</h4>

      <!-- Filter Form -->
      <form @submit.prevent="fetchCampaigns">
        <div class="row mb-3">
          <div class="col-md-4">
            <label for="search" class="form-label">Name of Campaign:</label>
            <input
              type="text"
              class="form-control"
              v-model="filters.search"
              placeholder="Search by name"
            />
          </div>
          <div class="col-md-3">
            <label for="niche" class="form-label">Niche:</label>
            <select v-model="filters.niche" class="form-select">
              <option value="">All Niches</option>
              <option v-for="niche in niches" :key="niche" :value="niche">{{ niche }}</option>
            </select>
          </div>
          <div class="col-md-2 d-flex align-items-end">
            <button type="submit" class="btn btn-primary w-100">Filter</button>
          </div>
        </div>
      </form>

      <!-- Campaign List -->
      <div v-if="campaigns.length">
        <div class="row">
          <div class="col-md-4 mb-3" v-for="campaign in campaigns" :key="campaign.id">
            <div class="card h-100">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title mb-2">{{ campaign.name }} - {{ campaign.sponsor_name }}</h5>
                <p class="card-text mb-3">{{ campaign.description }}</p>
                <div class="d-flex justify-content-between mt-auto">
                  <button @click="viewDetails(campaign.id)" class="btn btn-secondary btn-sm">View Details</button>
                  <button @click="sendAdRequest(campaign.id)" class="btn btn-primary btn-sm">Send Ad Request</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p class="text-center mt-2">No campaigns available.</p>
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
      campaigns: [], // Holds the list of campaigns
      niches: ["Tech", "Health", "Fashion", "Food"], // Example niches
      filters: {
        search: "",
        niche: "",
      },
    };
  },
  async mounted() {
    this.fetchCampaigns();
  },
  methods: {
    async fetchCampaigns() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:5000/influencer/search_campaigns", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          params: this.filters, // Pass filters as query parameters
        });
        this.campaigns = response.data;
      } catch (error) {
        console.error(error);
        alert("Failed to fetch campaigns.");
      }
    },
    viewDetails(campaignId) {
      this.$router.push(`/influencer/campaign/${campaignId}`); // Navigate to campaign details page
    },
    sendAdRequest(campaignId) {
      this.$router.push(`/influencer/ad_request/create/${campaignId}`); // Navigate to create ad request page
    },
  },
};
</script>

<style scoped>
h4 {
  margin-top: 30px;
  margin-bottom: 20px;
  text-align: center;
}

.card {
  border-radius: 0.5rem;
}

.card-body {
  display: flex;
  flex-direction: column;
}

.btn {
  width: 100%;
  text-align: center;
}
.btn-secondary {
  margin-right: 5px;
}
</style>
