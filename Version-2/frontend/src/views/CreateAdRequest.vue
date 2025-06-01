<template>
  <div>
    <InfluencerNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Create Ad Request</h4>
      <form @submit.prevent="createAdRequest">
        <div class="form-group mb-3">
          <label for="name">Ad Request Name:</label>
          <input
            type="text"
            id="name"
            v-model="adRequest.name"
            class="form-control"
            placeholder=""
            required
          />
        </div>
        
        <div class="form-group mb-3">
          <label for="requirements">Requirements:</label>
          <textarea
            id="requirements"
            v-model="adRequest.requirements"
            class="form-control"
            placeholder=""
            required
          ></textarea>
        </div>
        <div class="form-group mb-3">
          <label for="payment_amount">Proposed Payment Amount:</label>
          <input
            type="number"
            id="payment_amount"
            v-model="adRequest.payment_amount"
            class="form-control"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Submit Request</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import InfluencerNavbar from "@/components/InfluencerNavbar.vue";

export default {
  components: {
    InfluencerNavbar,
  },
  data() {
    return {
      adRequest: {
        name: "", // Ad request name
        campaign_id: this.$route.params.id, 
        influencer_id: localStorage.getItem("user_id"), 
        requirements: "",
        payment_amount: 0,
      },
    };
  },
  methods: {
    async createAdRequest() {
      try {
        const token = localStorage.getItem("access_token");
        await axios.post(
          `http://localhost:5000/influencer/send_ad_requests`,
          this.adRequest,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        alert("Ad request sent successfully.");
        this.$router.push("/influencer/dashboard");
      } catch (error) {
        console.error(error);
        alert("Failed to send ad request.");
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: auto;
}

h4 {
  text-align: center;
  margin-bottom: 20px;
}

button {
  margin-top: 20px;
}
</style>
