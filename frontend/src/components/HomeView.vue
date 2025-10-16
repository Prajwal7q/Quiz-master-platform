<template>
  <div>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-navbar px-4">
      <a class="navbar-brand" href="#">QuizDoo</a>
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
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="#about">About</a>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section d-flex flex-column justify-content-center align-items-center text-center">
      <div class="p-5 rounded shadow hero-box text-white">
        <h1 class="display-4 mb-3">Welcome to QuizDoo</h1>
        <p class="lead">
          Your smart companion for mastering quizzes and competitive exams.<br />
          Practice, prepare, and perform—all in one place.
        </p>
        <div class="mt-4">
          <router-link to="/admin-login" class="btn btn-outline-light me-3">
            Admin Login
          </router-link>
          <router-link to="/student-login" class="btn btn-light text-dark">
            Student Login
          </router-link>
        </div>
      </div>
    </div>

    <!-- About Section -->
    <section id="about" class="py-5 bg-footer text-white text-center">
      <div class="container">
        <h2 class="mb-3">About QuizDoo</h2>
        <p class="lead text-light">
          QuizDoo is a platform crafted for students and educators to simplify quiz-based learning and exam prep.
          With easy access for students and an intuitive dashboard for admins, we make knowledge accessible and fun.
        </p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script>

<style scoped>
:root {
  --color-navbar: #503434; /* Blackish grey */
  --color-hero-bg: #605353; /* Slightly lighter grey */
  --color-footer: #622a2a;
}

.bg-navbar {
  background-color:rgba(36, 31, 31, 0.95);
}

.hero-section {
  background-color: rgba(209, 200, 200, 0.95);
  min-height: 100vh;
  padding-top: 60px;
  padding-bottom: 60px;
}

.hero-box {
  background-color: rgba(33, 33, 33, 0.95);
  max-width: 700px;
}

.bg-footer {
  background-color:rgba(81, 52, 52, 0.95);
}
</style>
