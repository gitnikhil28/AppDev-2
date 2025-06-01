<template>
  <div>
    <AdminNavbar />
    <h2>Admin Statistics</h2>
    
    
    <div class="chart-container">
      <canvas id="userRolesChart"></canvas>
    </div>

    <div class="chart-container">
      <canvas id="campaignsPerNicheChart"></canvas>
    </div>

    <div class="chart-container">
      <canvas id="adRequestsPerInfluencerChart"></canvas>
    </div>

    <div class="chart-container">
      <canvas id="adRequestStatusChart"></canvas>
    </div>

    <div class="chart-container">
      <canvas id="flaggedUsersChart"></canvas>
    </div>
    
    <h4>Overall Statistics</h4>
    <ul>
      <li>Total Users: {{ stats.total_users }}</li>
      <li>Total Sponsors: {{ stats.total_sponsors }}</li>
      <li>Total Influencers: {{ stats.total_influencers }}</li>
      <li>Total Campaigns: {{ stats.total_campaigns }}</li>
      <li>Total Ad Requests: {{ stats.total_ad_requests }}</li>
      <li>Pending Ad Requests: {{ stats.pending_ad_requests }}</li>
      <li>Accepted Ad Requests: {{ stats.accepted_ad_requests }}</li>
      <li>Rejected Ad Requests: {{ stats.rejected_ad_requests }}</li>
      <li>Flagged Users: {{ stats.flagged_users }}</li>
      <li>Flagged Campaigns: {{ stats.flagged_campaigns }}</li>
    </ul>
    
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';
import AdminNavbar from '@/components/AdminNavbar.vue';

export default {
  components: {
    AdminNavbar,
  },
  data() {
    return {
      stats: {}
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get('http://localhost:5000/admin/stats', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.stats = response.data;

      this.createUserRolesChart();
      this.createCampaignsPerNicheChart();
      this.createAdRequestsPerInfluencerChart();
      this.createAdRequestStatusChart();
      this.createFlaggedUsersChart();
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    createUserRolesChart() {
      new Chart(
        document.getElementById('userRolesChart'),
        {
          type: 'pie',
          data: {
            labels: ['Sponsors', 'Influencers'],
            datasets: [{
              label: 'User Roles',
              data: [this.stats.total_sponsors, this.stats.total_influencers],
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: 'Distribution of User Roles'
              }
            }
          }
        }
      );
    },
    createCampaignsPerNicheChart() {
      new Chart(
        document.getElementById('campaignsPerNicheChart'),
        {
          type: 'bar',
          data: {
            labels: this.stats.campaigns_per_niche.map(item => item.niche),
            datasets: [{
              label: 'Campaigns per Niche',
              data: this.stats.campaigns_per_niche.map(item => item.count),
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            },
            plugins: {
              title: {
                display: true,
                text: 'Number of Campaigns per Niche'
              }
            }
          }
        }
      );
    },
    createAdRequestsPerInfluencerChart() {
      new Chart(
        document.getElementById('adRequestsPerInfluencerChart'),
        {
          type: 'bar',
          data: {
            labels: this.stats.ad_requests_per_influencer.map(item => item.influencer),
            datasets: [{
              label: 'Ad Requests per Influencer',
              data: this.stats.ad_requests_per_influencer.map(item => item.count),
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
              borderColor: 'rgba(153, 102, 255, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            },
            indexAxis: 'y', 
            plugins: {
              title: {
                display: true,
                text: 'Number of Ad Requests per Influencer'
              }
            }
          }
        }
      );
    },
    createAdRequestStatusChart() {
      new Chart(
        document.getElementById('adRequestStatusChart'),
        {
          type: 'doughnut', 
          data: {
            labels: ['Pending', 'Accepted', 'Rejected'],
            datasets: [{
              label: 'Ad Request Status',
              data: [
                this.stats.pending_ad_requests,
                this.stats.accepted_ad_requests,
                this.stats.rejected_ad_requests
              ],
              backgroundColor: [
                'rgba(255, 206, 86, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 99, 132, 0.2)'
              ],
              borderColor: [
                'rgba(255, 206, 86, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: 'Ad Request Status Distribution' 
              }
            }
          }
        }
      );
    },
    createFlaggedUsersChart() {
      new Chart(
        document.getElementById('flaggedUsersChart'),
        {
          type: 'pie', 
          data: {
            labels: ['Flagged Users', 'Non-Flagged Users'],
            datasets: [{
              label: 'Flagged Users',
              data: [this.stats.flagged_users, this.stats.total_users - this.stats.flagged_users],
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(75, 192, 192, 0.2)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(75, 192, 192, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: 'Proportion of Flagged Users'
              }
            }
          }
        }
      );
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 30%;
  margin: 20px auto;
}
</style>