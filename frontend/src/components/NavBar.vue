<template>
  <nav class="navbar navbar-expand-lg custom-navbar shadow-sm">
    <div class="container-fluid">
      <router-link class="navbar-brand fw-bold text-white" to="/admin-dashboard">
        QuizDoo   Admin
      </router-link>
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
            <router-link class="nav-link text-white" to="/admin-dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/users">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/admin-subjects">Subjects</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/chapters">Chapters</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/quizzes">Quizzes</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/questions">Questions</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white" href="#" @click="logout" style="cursor: pointer;">
              Logout
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  methods: {
    logout() {
      localStorage.removeItem("admintoken");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.custom-navbar {
  background-color: #2c2c2c; /* Blackish grey */
  padding: 0.8rem 1rem;
  border-bottom: 2px solid #444;
}

.nav-link {
  margin-left: 1rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #ffc107; 
  text-decoration: underline;
}
</style>
