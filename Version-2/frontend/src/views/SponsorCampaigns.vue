<template>
  <div>
    <SponsorNavbar />
    <div class="container mt-4">
      <!-- Button to create a new campaign -->
      <div class="text-end mb-4">
        <router-link to="/sponsor/create_campaign" class="btn btn-primary">Create a New Campaign</router-link>
      </div>

      <!-- Display list of campaigns in a table -->
      <div v-if="campaigns && campaigns.length > 0">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col">Niche</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="campaign in campaigns" :key="campaign.id">
              <td>{{ campaign.name }}</td>
              <td>{{ campaign.description }}</td>
              <td>{{ campaign.niche }}</td>
              <td>
                <button @click="viewDetails(campaign.id)" class="btn btn-primary btn-sm">View Details</button>
                <button @click="editCampaign(campaign.id)" class="btn btn-secondary btn-sm">Edit</button>
                <button @click="deleteCampaign(campaign.id)" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p class="text-center mt-3">No campaigns available.</p>
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
      campaigns: [], // Holds the list of campaigns
    };
  },
  async mounted() {
    this.fetchCampaigns();
  },
  methods: {
    async fetchCampaigns() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/sponsor/campaigns', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.campaigns = response.data;
      } catch (error) {
        console.error(error);
        alert('Failed to fetch campaigns.');
      }
    },
    viewDetails(campaignId) {
      this.$router.push(`/sponsor/campaign/${campaignId}`); // Navigate to campaign details page
    },
    editCampaign(campaignId) {
      this.$router.push(`/sponsor/campaign/edit/${campaignId}`); // Navigate to edit campaign page
    },
    async deleteCampaign(campaignId) {
      if (confirm('Are you sure you want to delete this campaign?')) {
        try {
          const token = localStorage.getItem('access_token');
          await axios.delete(`http://localhost:5000/sponsor/campaign/${campaignId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          alert('Campaign deleted successfully.');
          this.fetchCampaigns(); // Refresh the list after deletion
        } catch (error) {
          console.error(error);
          alert('Failed to delete the campaign.');
        }
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.btn-primary, .btn-secondary, .btn-danger {
  font-size: 0.875rem;
}

.table {
  margin-top: 1rem;
  border-radius: 10px;
}

.table th, .table td {
  vertical-align: middle;
  text-align: center;
}

.text-end {
  text-align: right;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}
</style>