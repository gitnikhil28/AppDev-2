<template>
  <div>
    <SponsorNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Edit Campaign</h4>
      <form @submit.prevent="updateCampaign">
        <div class="form-group">
          <label for="name">Campaign Name:</label>
          <input type="text" id="name" v-model="campaign.name" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="campaign.description" class="form-control" required></textarea>
        </div>
        <div class="form-group">
          <label for="start_date">Start Date:</label>
          <input type="date" id="start_date" v-model="campaign.start_date" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="end_date">End Date:</label>
          <input type="date" id="end_date" v-model="campaign.end_date" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="budget">Budget:</label>
          <input type="number" id="budget" v-model="campaign.budget" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="visibility">Visibility:</label>
          <select id="visibility" v-model="campaign.visibility" class="form-control" required>
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
        <div class="form-group">
          <label for="goals">Goals:</label>
          <textarea id="goals" v-model="campaign.goals" class="form-control" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </form>
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
      campaign: {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: 0,
        visibility: 'public',
        goals: '',
      },
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
    async updateCampaign() {
      try {
        const campaignId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        await axios.put(`http://localhost:5000/sponsor/campaign/${campaignId}`, this.campaign, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        alert('Campaign updated successfully.');
        this.$router.push('/sponsor/campaigns'); // Redirect to the campaigns list
      } catch (error) {
        console.error(error);
        alert('Failed to update the campaign.');
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 350px;
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

button {
  margin-top: 20px;
}
</style>
