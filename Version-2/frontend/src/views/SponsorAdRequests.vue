<template>
  <div>
    <SponsorNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Ad Requests</h4>

      <table class="table table-striped">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Influencer</th>
            <th>Status</th>
            <th>Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="adRequest in adRequests" :key="adRequest.id">
            <td>{{ adRequest.name }}</td>
            <td>{{ adRequest.campaign_name }}</td>
            <td>{{ adRequest.influencer_username }}</td>
            <td>
              <span
                :class="{
                  'badge bg-warning': adRequest.status === 'Pending',
                  'badge bg-success': adRequest.status === 'Accepted',
                  'badge bg-danger': adRequest.status === 'Rejected',
                }"
              >
                {{ adRequest.status }}
              </span>
            </td>
            <td>
              {{ adRequest.by_sponsor ? "Sent" : "Received" }}
            </td>
            <td>
              <button
                v-if="adRequest.status === 'Pending' && !adRequest.by_sponsor"
                class="btn btn-success btn-sm me-2"
                @click="handleAdRequest(adRequest.id, 'accept')"
              >
                Accept
              </button>
              <button
                v-if="adRequest.status === 'Pending' && !adRequest.by_sponsor"
                class="btn btn-danger btn-sm me-2"
                @click="handleAdRequest(adRequest.id, 'reject')"
              >
                Reject
              </button>
              <button
                v-if="adRequest.status === 'Pending' && adRequest.by_sponsor"
                class="btn btn-primary btn-sm me-2"
                @click="editAdRequest(adRequest.id)"
              >
                Edit
              </button>
              <button
                v-if="adRequest.status === 'Pending'"
                class="btn btn-danger btn-sm"
                @click="deleteAdRequest(adRequest.id)"
              >
                Delete
              </button>
              <button
                class="btn btn-secondary btn-sm ms-2"
                @click="viewAdRequest(adRequest.id)"
              >
                View
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SponsorNavbar from "@/components/SponsorNavbar.vue";

export default {
  components: {
    SponsorNavbar,
  },
  data() {
    return {
      adRequests: [],
    };
  },
  async mounted() {
    await this.fetchAdRequests();
  },
  methods: {
    async fetchAdRequests() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:5000/sponsor/ad_requests", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.adRequests = response.data;
      } catch (error) {
        console.error(error);
        alert("Failed to fetch ad requests");
      }
    },
    async handleAdRequest(adRequestId, action) {
      try {
        const token = localStorage.getItem("access_token");
        await axios.post(
          `http://localhost:5000/sponsor/ad_requests/${adRequestId}`,
          { action },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        alert(`Ad request ${action}ed successfully`);
        this.fetchAdRequests();
      } catch (error) {
        console.error(error);
        alert(`Failed to ${action} the ad request`);
      }
    },
    editAdRequest(adRequestId) {
      this.$router.push(`/sponsor/ad_request/edit/${adRequestId}`);
    },
    deleteAdRequest(adRequestId) {
      if (confirm("Are you sure you want to delete this ad request?")) {
        try {
          const token = localStorage.getItem("access_token");
          axios
            .delete(`http://localhost:5000/sponsor/ad_requests/${adRequestId}`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            })
            .then(() => {
              alert("Ad request deleted successfully");
              this.fetchAdRequests();
            });
        } catch (error) {
          console.error(error);
          alert("Failed to delete ad request");
        }
      }
    },
    viewAdRequest(adRequestId) {
      this.$router.push(`/sponsor/ad_request/${adRequestId}`);
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: auto;
}

h4 {
  text-align: center;
  margin-bottom: 20px;
}

.badge {
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
