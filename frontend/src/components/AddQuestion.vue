<template>
  <div class="d-flex justify-content-center">
    <h2>Add Question</h2>
  </div>
  <form @submit.prevent="addQuestion">
    <div class="d-flex justify-content-center">
      <div style="width: 30%">
        <div class="form-group">
          <label for="question">Question</label>
          <input
            type="text"
            class="form-control"
            id="question"
            v-model="question"
            required
          />
        </div>
        <div class="form-group">
          <label for="option1">Option 1</label>
          <input
            type="text"
            class="form-control"
            id="option1"
            v-model="option1"
            required
          />
        </div>
        <div class="form-group">
          <label for="option2">Option 2</label>
          <input
            type="text"
            class="form-control"
            id="option2"
            v-model="option2"
            required
          />
        </div>
        <div class="form-group">
          <label for="option3">Option 3</label>
          <input
            type="text"
            class="form-control"
            id="option3"
            v-model="option3"
            required
          />
        </div>
        <div class="form-group">
          <label for="option4">Option 4</label>
          <input
            type="text"
            class="form-control"
            id="option4"
            v-model="option4"
            required
          />
        </div>
        <div class="form-group">
          <label for="correctOption">Correct Option</label>
          <input
            type="number"
            class="form-control"
            id="correctOption"
            v-model.number="correctOption"
            required
            min="1"
            max="4"
          />
        </div>
        <div class="form-group">
          <label for="quiz">Select Quiz</label>
          <select
            class="form-control"
            id="quiz"
            v-model="selectedQuizId"
            required
            style="appearance: menulist"
          >
            <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
              {{ quiz.name }}
            </option>
          </select>
        </div>
        <br />
        <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
        <div class="d-flex justify-content-center">
          <button type="submit" class="btn btn-primary">Add Question</button>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  name: "AddQuestion",
  data() {
    return {
      question: "",
      option1: "",
      option2: "",
      option3: "",
      option4: "",
      correctOption: 0,
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
    async addQuestion() {
      const payload = {
        question: this.question,
        option1: this.option1,
        option2: this.option2,
        option3: this.option3,
        option4: this.option4,
        correct: this.correctOption,
        quiz_id: this.selectedQuizId,
      };

      try {
        const response = await fetch("/api/question", {
          method: "POST",
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
          alert(result.message);
        }
      } catch (error) {
        this.errorMessage = error.message;
        setTimeout(() => {
            this.errorMessage = null;
          }, 5000)
        console.log(error);
      }
    },
  },
  mounted() {
    this.getQuizzes();
  },
};
</script>
