<template>
  <div>
    <AdminNavbar />
    <h2>Users</h2>
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Role</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <button @click="toggleFlag(user.id)">
              {{ user.is_flagged ? 'Unflag' : 'Flag' }}
            </button>
            <button @click="viewUserDetails(user.id)">View Details</button> 
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showUserDetails" class="modal"> 
      <div class="modal-content">
        <h3>User Details</h3>
        <p><strong>Username:</strong> {{ selectedUser.username }}</p>
        <p><strong>Email:</strong> {{ selectedUser.email }}</p>
        <p><strong>Role:</strong> {{ selectedUser.role }}</p>
        <div v-if="selectedUser.sponsor_details">
          <h4>Sponsor Details</h4>
          <p><strong>Company Name:</strong> {{ selectedUser.sponsor_details.company_name }}</p>
          <p><strong>Industry:</strong> {{ selectedUser.sponsor_details.industry }}</p>
          <p><strong>Budget:</strong> {{ selectedUser.sponsor_details.budget }}</p>
        </div>
        <div v-if="selectedUser.influencer_details">
          <h4>Influencer Details</h4>
          <p><strong>Category:</strong> {{ selectedUser.influencer_details.category }}</p>
          <p><strong>Niche:</strong> {{ selectedUser.influencer_details.niche }}</p>
          <p><strong>Reach:</strong> {{ selectedUser.influencer_details.reach }}</p>
          <p><strong>Followers:</strong> {{ selectedUser.influencer_details.followers }}</p>
        </div>
        <button @click="showUserDetails = false">Close</button>
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
      users: [],
      showUserDetails: false, 
      selectedUser: {}  
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get('http://localhost:5000/admin/users', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.users = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async toggleFlag(userId) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.put(`http://localhost:5000/admin/users/${userId}`, null, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const user = this.users.find(user => user.id === userId);
        if (user) {
          user.is_flagged = !user.is_flagged;
        }
      } catch (error) {
        console.error(error);
      }
    },
    async viewUserDetails(userId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:5000/admin/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.selectedUser = response.data; 
        this.showUserDetails = true;  
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>

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