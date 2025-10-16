<template>
  <Navbar />
  <h1 class="text-center mb-5 text-primary fw-bold">Questions</h1>
  <div class="d-flex justify-content-end">
    <router-link to="/add-question" class="btn btn-success mb-3"
      >Add New Question</router-link
    >
  </div>
  <hr />
  <div class="container-fluid px-5">
    <div class="mb-3 d-flex justify-content-center">
      <input
        type="text"
        class="form-control w-50"
        v-model="searchQuery"
        placeholder="search for question..."
      />
      <button class="btn btn-primary ms-2" @click="getQuestions">Search</button>
    </div>
  <div class="container-fluid px-5">
    <div class="row">
      <div
        class="col-md-4 mb-4"
        v-for="question in questions"
        :key="question.id"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ question.question }}</h5>
            <p class="card-text">
              Option 1: {{ question.options[0] }}
              <br />
              Option 2: {{ question.options[1] }}
              <br />
              Option 3: {{ question.options[2] }}
              <br />
              Option 4: {{ question.options[3] }}
              <br />
              Correct: {{ question.correct }}
              <br />
              Quiz: {{ question.quiz_name }}
            </p>
            <div class="d-flex justify-content-end">
              <router-link
                :to="`/edit-question/${question.id}`"
                class="btn btn-primary btn-sm me-2"
              >
                Edit
              </router-link>
              <button
                class="btn btn-danger btn-sm"
                @click="deleteQuestion(question.id)"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>

  <p v-if="questions.length === 0" class="text-center text-muted mt-4">No questions found.</p>
</template>

<script>
import Navbar from "@/components/NavBar.vue";

export default {
  name: "QuestionView",
  components: {
    Navbar,
  },
  data() {
    return {
      questions: [],
      searchQuery: "",
    };
  },
  methods: {
    async getQuestions() {
      try {
        const response = await fetch(`/api/question?search=${this.searchQuery}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        console.log(data);
        this.questions = data;
      } catch (error) {
        console.log(error);
      }
    },
    async deleteQuestion(id) {
      const confirmation = confirm("Are you sure you want to delete?");
      if (!confirmation) return;
      try {
        const response = await fetch(`/api/question/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          const result = await response.json();
          alert(result.message);
          this.getQuestions();
        }
      } catch (error) {
        console.log(error);
      }
    },
  },
  mounted() {
    this.getQuestions();
  },
};
</script>
