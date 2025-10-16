<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/student-dashboard">Quiz Menia</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/user_summary">Summary</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="#" @click="logout" style="cursor: pointer;"> Logout </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>


    <div class="chart-container text-center mt-4">
      <h3>User Performance Chart</h3>
      <img v-if="chartUrl" :src="chartUrl" alt="User Bar Chart" class="img-fluid" />
      <p v-else>Loading Chart...</p>
    </div>

  
</template>

<script>
export default {
  data() {
    return {
      chartUrl: null,
    };
  },
  mounted() {
    this.fetchChart();
  },
  methods: {
    async fetchChart() {
      try {
        const token = localStorage.getItem("usertoken"); // Fetch user token
        const response = await fetch("/api/user_chart/image", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`, // Include auth token
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const blob = await response.blob(); // Convert response to blob
        this.chartUrl = URL.createObjectURL(blob); // Create image URL
      } catch (error) {
        console.log("Error fetching chart data:", error);
      }
    },
    logout() {
      localStorage.removeItem("usertoken");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.chart-container {
  margin-top: 20px;
}

.img-fluid {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
}
</style>
