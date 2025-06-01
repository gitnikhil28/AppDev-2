<template>
  <div>
    <AdminNavbar />
    <h2>Campaigns</h2>
    <table>
      <thead>
        <tr>
          <th>Campaign Name</th>
          <th>Sponsor Name</th>
          <th>Budget</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="campaign in campaigns" :key="campaign.id">
          <td>{{ campaign.name }}</td>
          <td>{{ campaign.sponsor_name }}</td>
          <td>{{ campaign.budget }}</td>
          <td>
            <button @click="toggleFlag(campaign.id)">
              {{ campaign.is_flagged ? 'Unflag' : 'Flag' }}
            </button>
            <button @click="viewCampaignDetails(campaign.id)">View Details</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showCampaignDetails" class="modal">
      <div class="modal-content">
        <h3>Campaign Details</h3>
        <p><strong>Name:</strong> {{ selectedCampaign.name }}</p>
        <p><strong>Sponsor:</strong> {{ selectedCampaign.sponsor_name }}</p>
        <p><strong>Budget:</strong> {{ selectedCampaign.budget }}</p>
        <p><strong>Description:</strong> {{ selectedCampaign.description }}</p>
        <p><strong>Start Date:</strong> {{ selectedCampaign.start_date }}</p>
        <p><strong>End Date:</strong> {{ selectedCampaign.end_date }}</p>
        <p><strong>Visibility:</strong> {{ selectedCampaign.visibility }}</p>
        <p><strong>Goals:</strong> {{ selectedCampaign.goals }}</p>
        <button @click="showCampaignDetails = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AdminNavbar from '@/components/AdminNavbar.vue';


export default {
  components: {
    AdminNavbar,
  },
  data() {
    return {
      campaigns: [],
      showCampaignDetails: false,
      selectedCampaign: {}
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get('http://localhost:5000/admin/campaigns', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.campaigns = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async toggleFlag(campaignId) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.put(`http://localhost:5000/admin/campaigns/${campaignId}`, null, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const campaign = this.campaigns.find(campaign => campaign.id === campaignId);
        if (campaign) {
          campaign.is_flagged = !campaign.is_flagged;
        }
      } catch (error) {
        console.error(error);
      }
    },
    async viewCampaignDetails(campaignId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:5000/admin/campaigns/${campaignId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.selectedCampaign = response.data;
        this.showCampaignDetails = true;
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
/* Add the same modal styles as in the AdminUsers.vue component */
.modal {
  display: block; 
  position: fixed; 
  z-index: 1; 
  left: 0;
  top: 0;
  width: 100%; 
  height: 100%; 
  overflow: auto; 
  background-color: rgba(0, 0, 0, 0.4); 
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto; 
  padding: 20px;
  border: 1px solid #888;
  width: 60%; 
}
</style>