<template>
  <div>
    <SponsorNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Your Profile</h4>
      <div v-if="sponsor">
        <div class="form-group">
          <label for="company_name">Company Name:</label>
          <input type="text" id="company_name" v-model="sponsor.company_name" class="form-control" :readonly="!editing">
        </div>
        <div class="form-group">
          <label for="industry">Industry:</label>
          <input type="text" id="industry" v-model="sponsor.industry" class="form-control" :readonly="!editing">
        </div>
        <div class="form-group">
          <label for="budget">Budget:</label>
          <input type="number" id="budget" v-model="sponsor.budget" class="form-control" :readonly="!editing">
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="sponsor.email" class="form-control" readonly>
        </div>
        <br>
        <div v-if="editing">
          <button @click="saveChanges" class="btn btn-primary">Save Changes</button>
          <button @click="cancelEditing" class="btn btn-secondary">Cancel</button>
        </div>
        <div v-else>
          <button @click="startEditing" class="btn btn-primary">Edit Profile</button>
        </div>
      </div>
      <div v-else>
        <p>Loading profile...</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import SponsorNavbar from '@/components/SponsorNavbar.vue';

export default {
  components: {
    SponsorNavbar
  },
  data() {
    return {
      sponsor: null,
      editing: false
    };
  },
  async mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/profiledetails/sponsor', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.sponsor = response.data;
      } catch (error) {
        console.error(error);
        // Handle error, e.g., redirect to login
      }
    },
    startEditing() {
      this.editing = true;
    },
    cancelEditing() {
      this.editing = false;
      this.fetchProfile(); // Reset the form
    },
    async saveChanges() {
      try {
        const token = localStorage.getItem('access_token');
        await axios.put('http://localhost:5000/update/profile/sponsor', this.sponsor, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.editing = false;
        // Optionally display a success message
      } catch (error) {
        console.error(error);
        // Handle error, e.g., display an error message
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin-top: 10px;
}

button {
  padding: 12px;
}

.form-control-sm {
  font-size: 0.6rem;  
  padding: 0.2rem 0.5rem;  
}

.form-select-sm {
  font-size: 0.6rem;
  padding: 0.375rem 0.75rem;
}
</style>
