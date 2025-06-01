<template>
  <div class="register">
    <h2>Influencer Registration</h2>
    <form @submit.prevent="submitInfluencerRegister">
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
        <label for="category">Category:</label>
        <input type="text" id="category" v-model="category" required />
      </div>
      <div>
        <label for="niche">Niche:</label>
        <select id="niche" v-model="niche" required>
          <option value="" disabled>Select your niche</option>
          <option v-for="option in NICHE_OPTIONS" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>
      <div>
        <label for="reach">Reach:</label>
        <input type="number" id="reach" v-model="reach" required />
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
      username: "",
      email: "",
      password: "",
      category: "",
      niche: "",
      reach: null,
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
    async submitInfluencerRegister() {
      const influencerData = {
        username: this.username,
        email: this.email,
        password: this.password,
        category: this.category,
        niche: this.niche,
        reach: this.reach,
        role: "influencer", // Make sure to pass the role as 'influencer'
      };

      try {
        const response = await fetch("http://localhost:5000/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(influencerData),
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message);
          this.$router.push("/login"); // Redirect to login after successful registration
        } else {
          alert(result.message);
        }
      } catch (error) {
        console.error(error);
        alert("Error occurred during registration");
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

input,
select {
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
