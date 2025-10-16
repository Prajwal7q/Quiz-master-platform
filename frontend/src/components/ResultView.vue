<template>
  <div class="d-flex justify-content-end mb-3">
    <router-link to="/student-dashboard" class="btn btn-success"> Dashboard </router-link>
  </div>

  <div class="d-flex justify-content-center vh-100">
    <div style="width: 70%">
      <div v-if="question">
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">{{ question.question }}</h5>
            <ul class="list-group">
              <li
                v-for="(option, index) in question.options"
                :key="option "
                class="list-group-item"
              >
                <span>{{ option }}</span>
                <span v-if="option === correctAnswer" class="text-success fw-bold">
                  ✔️ Correct
                </span>
                <span v-else-if="option === chosenAnswer" class="text-danger fw-bold">
                  ❌ Your Choice
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div class="container mt-4">
          <div class="row justify-content-between align-items-center">
            <div class="col-auto">
              <p class="mb-0">
                Showing Question <strong>{{ currentPage }}</strong> of
                <strong>{{ totalPages }}</strong>
              </p>
            </div>
            <div class="col-auto">
              <nav>
                <ul class="pagination mb-0">
                  <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <a
                      class="page-link"
                      href="#"
                      @click.prevent="fetchResult(currentPage - 1)"
                      >Previous</a
                    >
                  </li>
                  <li class="page-item">
                    <form class="d-flex" @submit.prevent="fetchResult(page)">
                      <input
                        type="number"
                        min="1"
                        :max="totalPages"
                        class="form-control me-2"
                        style="width: 60px"
                        v-model.number="page"
                      />
                      <button type="submit" class="btn btn-secondary">Go</button>
                    </form>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <a
                      class="page-link"
                      href="#"
                      @click.prevent="fetchResult(currentPage + 1)"
                      >Next</a
                    >
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      scoreId: null,
      question: null,
      chosenAnswer: "",
      currentPage: 1,
      totalPages: 1,
      totalQuestions: 0,
      correctAnswer: "",
      page: 1,
    };
  },
  methods: {
    async fetchResult(page = 1) {
      try {
        const response = await fetch(`/api/result/${this.scoreId}?page_p=${page}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("usertoken")}`,
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();

        if (response.ok) {
          this.question = data.questions[0];
          this.chosenAnswer = this.question.options[data.chosen_answer] || "";
          this.currentPage = data.question_no;
          this.totalPages = Math.ceil(data.total_questions / 1);

          // Get the correct answer from the options list using zero-based indexing
          const correctIndex = this.question.correct; // Convert 1-based to 0-based index
          if (correctIndex >= 0 && correctIndex < this.question.options.length) {
            this.correctAnswer = this.question.options[correctIndex];
          }
        } else {
          alert(data.message);
          this.$router.push("/student-dashboard");
          console.log(data.message);
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
  mounted() {
    this.scoreId = this.$route.params.id;
    this.fetchResult();
  },
  name: "ResultView",
};
</script>
