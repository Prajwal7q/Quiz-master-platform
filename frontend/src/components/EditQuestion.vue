<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div style="width: 30%">
      <h2 class="display-4 text-primary mb-4">Edit Question</h2>
      <form @submit.prevent="editQuestion">
        <div class="form-group">
          <label for="question">Question</label>
          <input type="text" class="form-control" id="question" v-model="question" required />
        </div>
        <div class="form-group">
          <label for="option1">Option 1</label>
          <input type="text" class="form-control" id="option1" v-model="option1" />
        </div>
        <div class="form-group">
          <label for="option2">Option 2</label>
          <input type="text" class="form-control" id="option2" v-model="option2" />
        </div>
        <div class="form-group">
          <label for="option3">Option 3</label>
          <input type="text" class="form-control" id="option3" v-model="option3" />
        </div>
        <div class="form-group">
          <label for="option4">Option 4</label>
          <input type="text" class="form-control" id="option4" v-model="option4" />
        </div>
        <div class="form-group">
          <label for="correct">Correct Answer (1-4)</label>
          <input type="number" min="1" max="4" class="form-control" id="correct" v-model="correct" />
        </div>
        <div class="form-group">
          <label for="quiz">Select Quiz</label>
          <select class="form-control" id="quiz" v-model="selectedQuizId" required>
            <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
              {{ quiz.name }}
            </option>
          </select>
        </div>

        <br />
        <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
        <button type="submit" class="btn btn-primary">Update Question</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "EditQuestion",
  data() {
    return {
      question: "",
      option1: "",
      option2: "",
      option3: "",
      option4: "",
      correct: 1,
      selectedQuizId: "",
      quizzes: [],
      errorMessage: "",
    };
  },
  methods: {
    async getQuizzes() {
      try {
        const response = await fetch("/api/quiz", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
        this.quizzes = data;
      } catch (error) {
        console.log(error);
      }
    },
    async getQuestionDetails() {
      const questionId = this.$route.params.id;

      try {
        const response = await fetch(`/api/question/${questionId}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch question details");
        }

        const data = await response.json();

        // Populate the form fields with the fetched data
        this.question = data.question;
        this.option1 = data.options[0]; // First option
        this.option2 = data.options[1]; // Second option
        this.option3 = data.options[2]; // Third option
        this.option4 = data.options[3]; // Fourth option
        this.correct = data.correct; // Ensure correct answer is properly assigned
        this.selectedQuizId = data.quiz_id;
      } catch (error) {
        console.error(error);
        this.errorMessage = "Failed to load question details.";
      }
    },
    async editQuestion() {
      const payload = {
        question: this.question,
        option1: this.option1,
        option2: this.option2,
        option3: this.option3,
        option4: this.option4,
        correct: this.correct,
        quiz_id: this.selectedQuizId,
      };

      const questionId = this.$route.params.id;

      try {
        const response = await fetch(`/api/question/${questionId}`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message);
          this.$router.push("/questions");
        } else {
          this.errorMessage = result.message;
          setTimeout(() => {
            this.errorMessage = null;
          }, 5000)
        }
      } catch (error) {

        console.log(error);
      }
    },
  },
  mounted() {
    this.getQuizzes();
    this.getQuestionDetails(); // Fetch question details on component mount
  },
};
</script>
