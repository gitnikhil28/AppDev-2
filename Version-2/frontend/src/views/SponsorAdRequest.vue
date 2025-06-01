<template>
  <div>
    <SponsorNavbar />
    <h2>Create Ad Request</h2>

    <form @submit.prevent="submitAdRequest">
      <div>
        <label for="name">Ad Request Name:</label>
        <input type="text" id="name" name="name" v-model="name" required>
      </div>
      <div>
        <label for="campaign_id">Select Campaign:</label>
        <select id="campaign_id" name="campaign_id" v-model="campaign_id" required>
          <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">{{ campaign.name }}</option>
        </select>
      </div>
      <div>
        <label for="messages">Messages:</label>
        <textarea id="messages" name="messages" v-model="messages"></textarea>
      </div>
      <div>
        <label for="requirements">Requirements:</label>
        <textarea id="requirements" name="requirements" v-model="requirements" required></textarea>
      </div>
      <div>
        <label for="payment_amount">Payment Amount:</label>
        <input type="number" id="payment_amount" name="payment_amount" v-model="payment_amount" required>
      </div>
      <button type="submit">Create Ad Request</button>
    </form>
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
      campaigns: [],
      campaign_id: null,
      messages: '',
      requirements: '',
      payment_amount: 0,
      name: '' 
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("access_token");
      const campaignsResponse = await axios.get('http://localhost:5000/sponsor/campaigns', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.campaigns = campaignsResponse.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async submitAdRequest() {
      try {
        const influencerId = this.$route.params.influencer_id;
        const token = localStorage.getItem("access_token");
        await axios.post(`http://localhost:5000/sponsor/create_ad_request/${influencerId}`, {
          name: this.name, 
          campaign_id: this.campaign_id,
          messages: this.messages,
          requirements: this.requirements,
          payment_amount: this.payment_amount
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.$router.push('/sponsor/ad_requests');
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>