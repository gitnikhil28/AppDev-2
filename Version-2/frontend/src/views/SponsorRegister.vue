<template>
  <div class="register">
    <h2>Sponsor Registration</h2>
    <form @submit.prevent="submitSponsorRegister">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <label for="companyName">Company Name:</label>
        <input type="text" id="companyName" v-model="company_name" required />
      </div>
      <div>
        <label for="industry">Industry:</label>
        <input type="text" id="industry" v-model="industry" required />
      </div>
      <div>
        <label for="budget">Budget:</label>
        <input type="number" id="budget" v-model="budget" required />
      </div>

      <button type="submit">Register</button>
    </form>

    <p>
      Already have an account? 
      <router-link to="/login">Login Here</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: ' ',
      password: '',
      company_name: '',
      industry: '',
      budget: null,
      
    };
  },
  methods: {
    async submitSponsorRegister() {
      const sponsorData = {
        username: this.username,
        email: this.email,
        password: this.password,
        company_name: this.company_name,
        industry: this.industry,
        budget: this.budget,
        role: 'sponsor',
      };

      try {
        const response = await fetch('http://localhost:5000/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(sponsorData),
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message);
          this.$router.push('/login');  // Redirect to login after successful registration
        } else {
          alert(result.message);
        }
      } catch (error) {
        console.error(error);
        alert('Error occurred during registration');
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

input {
  margin: 10px 0;
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  border: none;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #388e56;
}

p {
  margin-top: 20px;
}
</style>