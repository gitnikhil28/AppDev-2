<template>
  <div>
    <InfluencerNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Edit Ad Request</h4>

      <form @submit.prevent="submitEdit">
        <div v-if="adRequest">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input
              v-model="adRequest.name"
              type="text"
              class="form-control"
              id="name"
              required
            />
          </div>

          

          <div class="mb-3">
            <label for="price" class="form-label">Price (₹)</label>
            <input
              v-model="adRequest.price"
              type="number"
              class="form-control"
              id="price"
              required
            />
          </div>

          <div class="mb-3">
            <label for="requirements" class="form-label">Requirements</label>
            <input
              v-model="adRequest.requirements"
              type="text"
              class="form-control"
              id="name"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary">Save Changes</button>
          <button type="button" class="btn btn-secondary ms-2" @click="goBack">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import InfluencerNavbar from '@/components/InfluencerNavbar.vue';

export default {
  components: {
    InfluencerNavbar,
  },
  data() {
    return {
      adRequest: null,
    };
  },
  async mounted() {
    const adRequestId = this.$route.params.id; // Get ad request ID from route params
    await this.fetchAdRequest(adRequestId);
  },
  methods: {
    async fetchAdRequest(adRequestId) {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          `http://localhost:5000/influencer/ad_requests/${adRequestId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.adRequest = response.data;
      } catch (error) {
        console.error(error);
        alert("Failed to fetch ad request details");
      }
    },
    async submitEdit() {
      try {
        const token = localStorage.getItem("access_token");
        await axios.put(
          `http://localhost:5000/influencer/ad_requests/${this.adRequest.id}`,
          this.adRequest,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        alert("Ad request updated successfully");
        this.goBack();
      } catch (error) {
        console.error(error);
        alert("Failed to update ad request");
      }
    },
    goBack() {
      this.$router.push('/influencer/list_ad_requests');
    },
  },
};
</script>
