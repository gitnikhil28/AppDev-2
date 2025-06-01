<template>
  <div>
    <InfluencerNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Ad Request Details</h4>
      
      <div v-if="adRequest">
        <div class="mb-3">
          <strong>Name:</strong> {{ adRequest.name }}
        </div>
        <div class="mb-3">
          <strong>Campaign:</strong> {{ adRequest.campaign_name }}
        </div>
        <div class="mb-3">
          <strong>Status:</strong>
          <span
            :class="{
              'badge bg-warning': adRequest.status === 'Pending',
              'badge bg-success': adRequest.status === 'Accepted',
              'badge bg-danger': adRequest.status === 'Rejected',
            }"
          >
            {{ adRequest.status }}
          </span>
        </div>
        <div class="mb-3">
          <strong>Price:</strong> ₹{{ adRequest.price }}
        </div>
        <div class="mb-3" v-if="adRequest.negotiated_price">
          <strong>Negotiated Price:</strong> ₹{{ adRequest.negotiated_price }}
        </div>
        <div class="mb-3">
          <strong>Influencer:</strong> {{ adRequest.influencer_username }}
        </div>
        <div class="mb-3">
          <strong>Requirements:</strong> {{ adRequest.requirements }}
        </div>

        <button class="btn btn-primary" @click="goBack">Back</button>
      </div>
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
    goBack() {
      this.$router.push('/influencer/list_ad_requests');
    },
  },
};
</script>
