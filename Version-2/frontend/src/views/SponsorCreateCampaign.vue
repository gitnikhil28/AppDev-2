<template>
  <div>
    <SponsorNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Create Campaign</h4>
      <form @submit.prevent="submitCampaign">
        <div class="form-group mb-3">
          <label for="name">Campaign Name:</label>
          <input type="text" id="name" v-model="campaign.name" class="form-control" required />
        </div>
        <div class="form-group mb-3">
          <label for="description">Description:</label>
          <textarea id="description" v-model="campaign.description" class="form-control" required></textarea>
        </div>
        <div class="form-group mb-3">
          <label for="niche">Niche:</label>
          <select id="niche" v-model="campaign.niche" class="form-control" required>
            <option value="" disabled>Select a niche</option>
            <option v-for="option in NICHE_OPTIONS" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
        </div>
        <div class="form-group mb-3">
          <label for="start_date">Start Date:</label>
          <input type="date" id="start_date" v-model="campaign.start_date" class="form-control" required />
        </div>
        <div class="form-group mb-3">
          <label for="end_date">End Date:</label>
          <input type="date" id="end_date" v-model="campaign.end_date" class="form-control" required />
        </div>
        <div class="form-group mb-3">
          <label for="budget">Budget:</label>
          <input type="number" id="budget" v-model="campaign.budget" class="form-control" required />
        </div>
        <div class="form-group mb-3">
          <label for="visibility">Visibility:</label>
          <select id="visibility" v-model="campaign.visibility" class="form-control" required>
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Create Campaign</button>
      </form>
    </div>
  </div>
</template>

<script>
import SponsorNavbar from "@/components/SponsorNavbar.vue";

export default {
  components: { SponsorNavbar },
  data() {
    return {
      campaign: {
        name: "",
        description: "",
        niche: "",
        start_date: "",
        end_date: "",
        budget: 0,
        visibility: "public",
      },
      NICHE_OPTIONS: [
        "Fashion & Beauty",
        "Lifestyle",
        "Travel",
        "Fitness & Health",
        "Gaming",
        "Food & Cooking",
        "Technology",
        "Finance",
        "Entertainment",
      ],
    };
  },
  methods: {
    async submitCampaign() {
      try {
        const token = localStorage.getItem("access_token");
        await fetch("http://localhost:5000/sponsor/campaigns", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.campaign),
        });
        alert("Campaign created successfully");
        this.$router.push("/sponsor/campaigns");
      } catch (error) {
        console.error(error);
        alert("Error creating campaign");
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

button {
  margin-top: 20px;
}
</style>
