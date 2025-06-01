<template>
  <SponsorNavbar />
  <div class="container">
    <h4 class="my-4 text-center">Find Influencers</h4>

    <div class="row mb-3">
      <div class="col-md-4">
        <input type="text" class="form-control" v-model="username" placeholder="Name or Username...">
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="niche">
          <option value="">All Niches</option>
          <option v-for="nicheOption in nicheOptions" :key="nicheOption" :value="nicheOption">{{ nicheOption }}</option>
        </select>
      </div>
      <div class="col-md-3">
        <input type="number" class="form-control" v-model="minReach" placeholder="Minimum Reach">
      </div>
      <div class="col-md-2 d-flex align-items-end">
        <button type="button" class="btn btn-primary me-2" @click="searchInfluencers">Filter</button>
        <button type="button" class="btn btn-secondary" @click="clearFilters">Clear</button>
      </div>
    </div>

    <div v-if="searchResults.length === 0 && searched">
      <p class="mt-2 text-center">No influencers found.</p>
    </div>

    <div class="row">
      <div v-for="influencer in searchResults" :key="influencer.user_id" class="col-md-6 mb-3">
        <div class="card h-100 d-flex flex-row align-items-center">
          <img v-if="influencer.profile_picture" :src="influencer.profile_picture" alt="Profile Picture" class="card-img-left">
          <div class="card-body">
            <h5 class="card-title">{{ influencer.username }}</h5>
            <p class="card-text">Niche: {{ influencer.niche }}</p>
            <p class="card-text">Reach: {{ influencer.reach }}</p>
            <router-link :to="{ name: 'SponsorAdRequest', params: { influencer_id: influencer.user_id } }"> 
              <button class="btn btn-primary btn-sm">Assign Influencer</button>
            </router-link>
          </div>
        </div>
      </div>
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
      niche: '',
      minReach: 0,
      maxReach: 10000000,
      username: '',
      searchResults: [],
      searched: false,
      nicheOptions: [] 
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get('http://localhost:5000/sponsor/search_influencers', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.searchResults = response.data.influencers; 
      this.nicheOptions = response.data.niches;   
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async searchInfluencers() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get('http://localhost:5000/sponsor/search_influencers', {
          headers: {
            Authorization: `Bearer ${token}`
          },
          params: {
            niche: this.niche,
            min_reach: this.minReach,
            max_reach: this.maxReach,
            username: this.username
          }
        });
        this.searchResults = response.data.influencers;
        this.searched = true;
      } catch (error) {
        console.error(error);
      }
    },
    clearFilters() {
      this.niche = '';
      this.minReach = 0;
      this.maxReach = Infinity;
      this.username = '';
      this.searchInfluencers();
    }
  }
};
</script>

<style scoped>
body {
  background: linear-gradient(135deg, #010515 0%, #220341e5 100%);
  color: #fff;
}

.container {
  max-width: 800px;
  margin: auto;
}

.card {
  border-radius: 10px;
  overflow: hidden;
}

.card-img-left {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
}

.card-body {
  padding: 15px;
}

.card-title {
  font-size: 1.25rem;
  margin-bottom: 10px;
}

.btn {
  margin-top: 5px;
}

.row {
  margin-left: -5px;
  margin-right: -5px;
}

.col-md-4,
.col-md-3,
.col-md-2 {
  padding-left: 5px;
  padding-right: 5px;
}
</style>