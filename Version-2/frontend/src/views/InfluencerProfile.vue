<template>
  <div class="profile">
    <InfluencerNavbar />
    <div class="container mt-4">
      <h4 class="text-center mb-4">Your Profile</h4>
      <div v-if="influencer">
        <div class="text-center mb-4">
          <img
            v-if="influencer.profile_picture"
            :src="influencer.profile_picture"
            alt="Profile Picture"
            class="profile-img"
          />
          <div v-else class="placeholder">No Profile Picture</div>
          <input
            v-if="editing"
            type="file"
            @change="handleProfilePictureUpload"
            class="form-control mt-2"
          />
        </div>
        <div v-if="editing">
          <div class="form-group">
            <label for="category">Category:</label>
            <input
              type="text"
              id="category"
              v-model="editedProfile.category"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="niche">Niche:</label>
            <select
              id="niche"
              v-model="editedProfile.niche"
              class="form-control"
            >
              <option
                v-for="option in nicheOptions"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="reach">Reach:</label>
            <input
              type="number"
              id="reach"
              v-model="editedProfile.reach"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="followers">Followers:</label>
            <input
              type="number"
              id="followers"
              v-model="editedProfile.followers"
              class="form-control"
            />
          </div>
          <button @click="saveProfile" class="btn btn-primary mt-3">Save</button>
          <button @click="cancelEditing" class="btn btn-secondary mt-3 ml-2">
            Cancel
          </button>
        </div>
        <div v-else>
          <p><strong>Category:</strong> {{ influencer.category }}</p>
          <p><strong>Niche:</strong> {{ influencer.niche }}</p>
          <p><strong>Reach:</strong> {{ influencer.reach }}</p>
          <p><strong>Followers:</strong> {{ influencer.followers }}</p>
          <button @click="startEditing" class="btn btn-primary mt-3">
            Edit Profile
          </button>
        </div>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
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
      influencer: null,
      editing: false,
      editedProfile: {},
      nicheOptions: [
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
  async mounted() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      const token = localStorage.getItem("access_token");
      try {
        const response = await axios.get(
          "http://localhost:5000/influencer/profile",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.influencer = response.data;
        this.editedProfile = { ...response.data }; // Initialize edited profile
      } catch (error) {
        console.error(error);
        alert("Failed to load profile.");
      }
    },
    startEditing() {
      this.editing = true;
    },
    cancelEditing() {
      this.editing = false;
      this.editedProfile = { ...this.influencer }; // Reset edits
    },
    async saveProfile() {
      const token = localStorage.getItem("access_token");
      try {
        const response = await axios.put(
          "http://localhost:5000/influencer/profile",
          this.editedProfile,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        alert("Profile updated successfully.");
        this.fetchProfile(); // Refresh profile
        this.editing = false;
      } catch (error) {
        console.error(error);
        alert("Failed to update profile.");
      }
    },
    async handleProfilePictureUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("profile_picture", file);

      const token = localStorage.getItem("access_token");
      try {
        const response = await axios.post(
          "http://localhost:5000/influencer/profile/upload",
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
        alert("Profile picture updated successfully.");
        this.fetchProfile(); // Refresh profile to show the new picture
      } catch (error) {
        console.error(error);
        alert("Failed to upload profile picture.");
      }
    },
  },
};
</script>

<style scoped>
.register {
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

.profile-img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto;
  display: block;
}
.placeholder {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem;
  color: #666;
  margin: 0 auto;
}
</style>
