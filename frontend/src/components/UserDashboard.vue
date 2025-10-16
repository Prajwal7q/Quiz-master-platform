<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/student-dashboard">QuizDoo</router-link>
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
  <br>
  <h3> Welcome,  {{ student_name }} </h3>
  <h1 class="text-center mb-3 text-primary fw-bold">🎯 User Dashboard</h1>
  <div class="text-center mb-4">
    <p class="lead text-muted">
      Welcome to your Quiz Mania Dashboard! Here, you can attempt ongoing quizzes,
      check past scores, and prepare for upcoming tests. Stay consistent and improve
      your knowledge one quiz at a time! 🚀
    </p>
  </div>

  <!-- Current Quizzes Section -->
  <div class="mb-5 p-4 bg-white shadow rounded ">
    <h2 class="text-primary">📌 Current Quizzes</h2>
    <div class="table-responsive w-80 mx-auto">
      <table class="table table-hover shadow-sm rounded overflow-hidden">
        <thead class="table-dark text-white">
          <tr>
            <th>Quiz Name</th>
            <th>Chapter</th>
            <th>Duration</th>
            <th>Deadline</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in currentQuizzes" :key="i.id">
            <td>{{ i.name }}</td>
            <td>{{ i.chapter_name }}</td>
            <td>{{ i.duration }}</td>
            <td class="bg-warning fw-bold text-dark">{{i.end_date}}, {{ i.end_time }}</td>
            <td>
              <router-link
                :to="`/exam/${i.id}`"
                class="btn btn-success btn-sm rounded-pill"
                >Start Quiz</router-link
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- History -->
  <div class="mb-5 p-4 bg-white shadow rounded">
    <h2 class="text-info">Quiz History</h2>
    <div class="table-responsive mx-auto">
      <table class="table table-hover shadow-sm rounded overflow-hidden" id="history">
        <thead class="table-dark text-white">
          <tr>
            <th>Quiz Name</th>
            <th>Chapter</th>
            <th>Your Score</th>
            <th>Deadline</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in historyQuizzes" :key="i.id">
            <td>{{ i.quiz_name }}</td>
            <td>{{ i.chapter_name }}</td>
            <td class="fw-bold text-primary">{{ i.percentage }}%</td>
            <td>{{ i.end_time }}</td>

            <td>
              <router-link
                v-if="currentQuizzes.some(q => q.id === i.quiz_id)"
                :to="`/exam/${i.quiz_id}`"
                class="btn btn-warning btn-sm rounded-pill"
                >Reattempt</router-link
              >
              &nbsp;
                <router-link
                  :to="`/result/${i.id}`"
                  class="btn btn-primary btn-sm rounded-pill"
                  >Check Result</router-link>

            </td>

          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Past Quizzes -->
  <div class="mb-5 p-4 bg-white shadow rounded">
    <h2 class="text-secondary">📆 Past Quizzes</h2>
    <div class="table-responsive mx-auto">
      <table class="table table-hover shadow-sm rounded overflow-hidden" id="post">
        <thead class="table-dark text-white">
          <tr>
            <th>Quiz Name</th>
            <th>Chapter</th>
            <th>Duration</th>
            <th>Starts On</th>
            <th>Deadline</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in pastQuizzes" :key="i.id">
            <td>{{ i.name }}</td>
            <td>{{ i.chapter_name }}</td>
            <td>{{ i.duration }}</td>
            <td class="fw-bold">{{ i.start_date }} {{ i.start_time }}</td>
            <td class="bg-danger fw-bold text-white">
              {{ i.end_date }} {{ i.end_time }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Pre Quizzes -->
  <div class="mb-5 p-4 bg-white shadow rounded">
    <h2 class="text-success">⏳ Upcoming Quizzes</h2>
    <div class="table-responsive mx-auto">
      <table class="table table-hover shadow-sm rounded overflow-hidden" id="pre">
        <thead class="table-dark text-white">
          <tr>
            <th>Quiz Name</th>
            <th>Chapter</th>
            <th>Duration</th>
            <th>Starts On</th>
            <th>Deadline</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in upcomingQuizzes" :key="i.id">
            <td>{{ i.name }}</td>
            <td>{{ i.chapter_name }}</td>
            <td>{{ i.duration }}</td>
            <td>{{ i.start_date }} {{ i.start_time }}</td>
            <td class="bg-warning fw-bold text-dark">
              {{ i.end_date }} {{ i.end_time }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      student_name: '',
      currentQuizzes: [],
      historyQuizzes: [],
      pastQuizzes: [],
      upcomingQuizzes: [],
    };
  },

  methods: {
    async getData() {
      try {
        const response = await fetch("/api/user_dash", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("usertoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          alert("Error");
        } else {
          const result = await response.json();
          this.student_name = result.student_name;
          this.currentQuizzes = result.current_quizs;
          this.historyQuizzes = result.history_quizs;
          this.pastQuizzes = result.past_quizs;
          this.upcomingQuizzes = result.pre_quizs;
        }
      } catch (error) {
        console.log(error);
      }
    },
    logout() {
      localStorage.removeItem("usertoken");
      this.$router.push("/");
      
    },
  },
  mounted() {
    this.getData();
  },

  name: "UserDashboard",
};
</script>
