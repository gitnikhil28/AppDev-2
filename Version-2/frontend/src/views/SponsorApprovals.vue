<template>
  <div>
  <AdminNavbar />
    <h4>Pending Sponsor Approvals</h4>
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Industry</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sponsor in sponsors" :key="sponsor.id">
          <td>{{ sponsor.username }}</td>
          <td>{{ sponsor.email }}</td>
          <td>{{ sponsor.industry }}</td>
          <td>
            <button @click="viewSponsorDetails(sponsor.id)">View Details</button>
            <button @click="approveSponsor(sponsor.id)">Approve</button>
            <button @click="deleteSponsor(sponsor.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showSponsorDetails" class="modal">
      <div class="modal-content">
        <h3>Sponsor Details</h3>
        <p><strong>Username:</strong> {{ selectedSponsor.username }}</p>
        <p><strong>Email:</strong> {{ selectedSponsor.email }}</p>
        <p><strong>Company Name:</strong> {{ selectedSponsor.company_name }}</p>
        <p><strong>Industry:</strong> {{ selectedSponsor.industry }}</p>
        <p><strong>Budget:</strong> {{ selectedSponsor.budget }}</p>
        <button @click="showSponsorDetails = false">Close</button>
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
      sponsors: [],
      showSponsorDetails: false,
      selectedSponsor: {}
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get('http://localhost:5000/admin/sponsor_approvals', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.sponsors = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async viewSponsorDetails(sponsorId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:5000/admin/sponsor_approvals/${sponsorId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.selectedSponsor = response.data;
        this.showSponsorDetails = true;
      } catch (error) {
        console.error(error);
      }
    },
    async approveSponsor(sponsorId) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.put(`http://localhost:5000/admin/sponsor_approvals/${sponsorId}`, null, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        // Update the UI or show a success message
        this.sponsors = this.sponsors.filter(sponsor => sponsor.id !== sponsorId); 
      } catch (error) {
        console.error(error);
      }
    },
    async deleteSponsor(sponsorId) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`http://localhost:5000/admin/sponsor_approvals/${sponsorId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.sponsors = this.sponsors.filter(sponsor => sponsor.id !== sponsorId);
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