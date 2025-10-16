<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div style="width: 50%" class="text-center mb-3">
      <div style="background-color: gray; border-radius: 10px" class="timer-container mb-3">
        <h2>Time Left: {{ formattedTime }}</h2>
      </div>
      <br><br><br>
      <div>
        <form @submit.prevent="submitForm">
          <div v-if="question">
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">{{ question.question }}</h5>
                <div class="list-group">
                  <input
                    type="radio"
                    id="clear"
                    hidden
                    checked
                    :name="`question${question.id}`"
                    value="0"
                  />
                  <label
                    v-for="(option, index) in question.options"
                    :key="index+1"
                    style="cursor: pointer"
                    class="list-group-item d-flex align-items-center"
                  >
                    <input
                      type="radio"
                      :name="`question${question.id}`"
                      :value="index"
                      class="form-check-input me-2"
                      v-model="selectedAnswer"
                    />
                    {{ option }}
                  </label>
                  <label for="clear">
                    <a
                      style="
                        border: 1px solid black;
                        background: rgb(201, 191, 191);
                        border-radius: 5px;
                        cursor: pointer;
                      "
                      @click="selectedAnswer = null"
                    >
                      Clear Selection
                    </a>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <input type="hidden" name="flag" v-if="currentPage === totalPages" value="submit" />
          <button type="submit" class="btn btn-primary w-100">
            {{ currentPage === totalPages ? "Submit Exam" : "Save" }}
          </button>
        </form>

        <!-- Pagination -->
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
                      @click.prevent="fetchQuestion(currentPage - 1)"
                      >Previous</a
                    >
                  </li>
                  <li class="page-item">
                    <form class="d-flex" @submit.prevent="fetchQuestion(page)">
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
                      @click.prevent="fetchQuestion(currentPage + 1)"
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
      quizId: null,
      question: null,
      selectedAnswer: null,
      currentPage: 1,
      totalPages: 1,
      totalQuestions: null,
      page: 1,
      timeLeft: null, // Total quiz time (in seconds)
      timer: null,
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    },
  },
  methods: {
    async fetchQuestion(page = 1) {
      try {
        const response = await fetch(`/api/exam/${this.quizId}?page=${page}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("usertoken")}`,
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();

        if (response.ok) {
          if (!data.question) {
            alert("Exam will start soon");
            this.$router.push("/student-dashboard"); // Redirect or handle accordingly
            return;
          }
          this.question = data.question;
          this.currentPage = data.current_page;
          this.totalPages = Math.ceil(data.total_questions / 1); // Since per_page = 1
          this.totalQuestions = data.total_questions;

          // Set the selected answer from the API response
          // this.selectedAnswer = data.answers[data.question.id] !== undefined ? parseInt(data.answers[data.question.id]) : null;
        } else {
          console.log(data.message);
        }
      } catch (error) {
        console.log(error);
      }
    },
    async submitForm(event) {
      try {
        event.preventDefault();

        const submitFlag = this.currentPage === this.totalPages;

        const formData = {
          quiz_id: this.quizId,
          question_id: this.question.id,
          selected_option: this.selectedAnswer,
          submit: submitFlag,
        };

        const response = await fetch(`/api/exam/${this.quizId}`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("usertoken")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        if (response.ok) {
          this.selectedAnswer = null;

          if (this.currentPage < this.totalPages) {
            this.currentPage += 1;
            this.fetchQuestion(this.currentPage);
          } else {
            this.endExam();
          }
        } else {
          console.log(data.message);
        }
      } catch (error) {
        console.log(error);
      }
    },
    async submitFinalAnswers() {
    try {
      const formData = {
        quiz_id: this.quizId,
        question_id: this.question.id,
        selected_option: this.selectedAnswer,
        submit: true,
      };

      const response = await fetch(`/api/exam/${this.quizId}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("usertoken")}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (response.ok) {
        console.log("Exam submitted successfully.");
      } else {
        console.log(data.message);
      }
    } catch (error) {
      console.log(error);
    }
  },
    startTimer() {
      if (this.timer) clearInterval(this.timer); // Clear any existing timer

      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          clearInterval(this.timer);
          this.endExam();
        }
      }, 1000);
    },
    endExam() {
      this.submitFinalAnswers();
      alert("Exam submitted successfully.");
      this.$router.push("/student-dashboard");
    },
  },
  mounted() {
    this.quizId = this.$route.params.id;
    this.fetchQuestion().then(() => {
      // Initialize the timer with the total duration of the quiz
      this.timeLeft = this.question.duration * 60;
      this.startTimer(); // Start the countdown timer when quiz starts
    });
  },
  beforeUnmount() {
    clearInterval(this.timer); // Stop the timer when component is destroyed
  },
};
</script>
