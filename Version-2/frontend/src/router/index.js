import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import SponsorRegister from '../views/SponsorRegister.vue';
import InfluencerRegister from '../views/InfluencerRegister.vue';
import SponsorDashboard from '../views/SponsorDashboard.vue';
import InfluencerDashboard from '../views/InfluencerDashboard.vue';
import SponsorCreateCampaign from '../views/SponsorCreateCampaign.vue';
import SponsorProfile from '../views/SponsorProfile.vue';
import InfluencerProfile from '../views/InfluencerProfile.vue';
import SponsorCampaigns from '../views/SponsorCampaigns.vue';
import SponsorCampaignDetails from '../views/SponsorCampaignDetails.vue';
import EditSponsorCampaign from '../views/EditSponsorCampaign.vue';
import FindCampaigns from '../views/FindCampaigns.vue';
import CampaignDetails from '../views/CampaignDetails.vue';
import CreateAdRequest from '../views/CreateAdRequest.vue';
import SponsorAdRequests from '../views/SponsorAdRequests.vue';
import InfluencerAdRequests from "../views/InfluencerAdRequests.vue";
import AdRequestView from "../views/AdRequestView.vue";
import AdRequestEdit from "../views/AdRequestEdit.vue";
import SpViewAdRequest from "../views/SpViewAdRequest"
import SearchInfluencers from "../views/SearchInfluencers"
import SponsorAdRequest from "../views/SponsorAdRequest"
import AdminUsers from "../views/AdminUsers"
import AdminCampaigns from "../views/AdminCampaigns"
import AdminStats from "../views/AdminStats"
import SponsorApprovals from "../views/SponsorApprovals"



const routes = [
  { path: '/', component: Login },
  { path: '/login', component: Login },
  { path: '/register/sponsor', component: SponsorRegister },
  { path: '/register/influencer', component: InfluencerRegister },
  { path: '/influencer/dashboard', name: 'InfluencerDashboard', component: InfluencerDashboard },
  { path: '/sponsor/dashboard', name: 'SponsorDashboard', component: SponsorDashboard },
  { path: '/sponsor/create_campaign', name: 'SponsorCreateCampaign', component: SponsorCreateCampaign },
  { path: '/sponsor/profile', name: 'SponsorProfile', component: SponsorProfile },
  { path: '/influencer/profile', name: 'InfluencerProfile', component: InfluencerProfile },
  { path: '/sponsor/campaigns', name: 'SponsorCampaigns', component: SponsorCampaigns },
  { path: '/sponsor/campaign/:id', name: 'SponsorCampaignDetails', component: SponsorCampaignDetails },
  { path: '/sponsor/campaign/edit/:id', name: 'EditSponsorCampaign', component: EditSponsorCampaign },
  { path: '/influencer/find_campaigns', name: 'FindCampaigns', component: FindCampaigns },
  { path: '/influencer/campaign/:id', name: 'CampaignDetails', component: CampaignDetails }, 
  { path: '/influencer/ad_request/create/:id', name: 'CreateAdRequest', component: CreateAdRequest },
  { path: '/sponsor/ad_requests', name: 'SponsorAdRequests', component: SponsorAdRequests },
  { path: '/influencer/list_ad_requests', name: 'InfluencerAdRequests', component: InfluencerAdRequests },
  { path: '/influencer/ad_request/:id', name: 'viewAdRequest', component: AdRequestView },
  { path: '/influencer/ad_request/edit/:id', name: 'editAdRequest', component: AdRequestEdit },
  { path: '/sponsor/ad_request/:id', name: 'spviewAdRequest', component: SpViewAdRequest },
  { path: '/sponsor/search_influencers', name: 'SearchInfluencers', component: SearchInfluencers },
  { path: '/sponsor/create_ad_request/:influencer_id', name: 'SponsorAdRequest', component: SponsorAdRequest },
  {
    path: '/admin/users',  
    name: 'AdminUsers',   
    component: AdminUsers 
  },
  {
    path: '/admin/campaigns',  
    name: 'AdminCampaigns',   
    component: AdminCampaigns 
  },
  {
    path: '/admin/stats',  
    name: 'AdminStats',   
    component: AdminStats
  },
  {
    path: '/admin/sponsor_approvals',  
    name: 'SponsorApprovals',   
    component: SponsorApprovals
  }




   
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
