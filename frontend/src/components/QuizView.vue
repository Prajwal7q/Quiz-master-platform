<template>
  <Navbar />

    <h1 class="text-center mb-5 text-primary fw-bold">Quizzes</h1>

  <div class="d-flex justify-content-end">
    <router-link to="/add-quiz" class="btn btn-success mb-3"
      >Add New Quiz</router-link
    >
  </div>
  <hr />

  <div class="container-fluid px-5">
    <div class="mb-3 d-flex justify-content-center">
      <input
        type="text"
        class="form-control w-50"
        v-model="searchQuery"
        placeholder="Enter quiz name..."
      />
      <button class="btn btn-primary ms-2" @click="getQuizzes">Search</button>
    </div>

  <div class="row">
    <div class="col-md-4" v-for="quiz in quizzes" :key="quiz.id">
      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">{{ quiz.name }}</h5>
          <hr>
          <p class="card-text">
            Duration: {{ quiz.duration }} minutes
            <br />
            Start Date: {{ quiz.start_date }}
            <br />
            Start Time: {{ quiz.start_time }}
            <br />
            End Date: {{ quiz.end_date }}
            <br />
            End Time: {{ quiz.end_time }}
            <br />
            Chapter: {{ quiz.chapter_name }}
          </p>
          <div class="d-flex justify-content-end">
            <router-link
              :to="`/edit-quiz/${quiz.id}`"
              class="btn btn-primary btn-sm me-2"
            >
              Edit
            </router-link>
            <button
              class="btn btn-danger btn-sm"
              @click="deleteQuiz(quiz.id)"
            >
              Delete
            </button>
          </div>
        </div>
    

      </div>

    </div>
  </div>
  </div>

  <p v-if="quizzes.length === 0" class="text-center text-muted mt-4">No quizzes found.</p>


</template>

<script>
import Navbar from "@/components/NavBar.vue";

export default {
  data() {
    return {
      quizzes: [],
      searchQuery: "",
    };
  },
  mounted() {
    this.getQuizzes();
  },
  methods: {
    async getQuizzes() {
      try {
        const response = await fetch(`/api/quiz?search=${this.searchQuery}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        this.quizzes = data;
      } catch (error) {
        console.error(error);
      }
    },

    async deleteQuiz(id) {
      const confirmation = confirm("Are you sure you want to delete?");
      if (!confirmation) return; // Exit if user cancels

      try {
        const response = await fetch(`/api/quiz/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const result = await response.json();
          alert(result.message);
          this.getQuizzes(); // Refresh quiz list
          this.$router.push("/quizzes");
        }
      } catch (error) {
        console.error(error);
      }
    },
  },

  name: "QuizView",
  components: {
    Navbar,
  },
};
</script>
