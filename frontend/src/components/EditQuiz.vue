<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div style="width: 30%">
      <h2 class="display-4 text-primary mb-4">Edit Quiz</h2>
      <form @submit.prevent="editQuiz">
        <div class="form-group">
          <label for="quizName">Quiz Name</label>
          <input type="text" class="form-control" id="quizName" v-model="name" />
        </div>
        <div class="form-group">
          <label for="duration">Duration (in minutes)</label>
          <input type="number" class="form-control" id="duration" v-model.number="duration" min="0" max="300" />
        </div>
        <div class="form-group">
          <label for="startDate">Start Date</label>
          <input type="date" class="form-control" id="startDate" v-model="startDate" />
        </div>
        <div class="form-group">
          <label for="startTime">Start Time</label>
          <input type="time" class="form-control" id="startTime" v-model="startTime" />
        </div>
        <div class="form-group">
          <label for="endDate">End Date</label>
          <input type="date" class="form-control" id="endDate" v-model="endDate" />
        </div>
        <div class="form-group">
          <label for="endTime">End Time</label>
          <input type="time" class="form-control" id="endTime" v-model="endTime" />
        </div>
        <div class="form-group">
          <label for="chapter">Select Chapter</label>
          <select class="form-control" id="chapter" v-model="selectedChapterId" required>
            <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
              {{ chapter.name }}
            </option>
          </select>
        </div>
        <br />
        <div v-if="errorMessage" class="text-danger"> {{ errorMessage }} </div>
        <button type="submit" class="btn btn-primary">Edit Quiz</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "EditQuiz",
  data() {
    return {
      name: "",
      duration: "",
      startDate: "",
      startTime: "",
      endDate: "",
      endTime: "",
      selectedChapterId: "",
      chapters: [],
      errorMessage: "",
    };
  },
  methods: {
    async getChapters() {
      try {
        const response = await fetch("/api/chapter", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) throw new Error("Failed to fetch chapters");
        const data = await response.json();
        this.chapters = data;
      } catch (error) {
        this.errorMessage = error.message;
      }
    },

    async getQuizDetails() {
      const quizId = this.$route.params.id;
      try {
        const response = await fetch(`/api/quiz/${quizId}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) throw new Error("Failed to fetch quiz details");
        const data = await response.json();

        this.name = data.name;
        this.duration = data.duration;
        this.startDate = data.start_date;
        this.startTime = data.start_time;
        this.endDate = data.end_date;
        this.endTime = data.end_time;
        this.selectedChapterId = data.chapter_id;
      } catch (error) {
        this.errorMessage = error.message;
      }
    },

    async editQuiz() {
      const quizId = this.$route.params.id;
      const payload = {
        name: this.name,
        duration: this.duration,
        start_date: this.startDate,
        start_time: this.startTime,
        end_date: this.endDate,
        end_time: this.endTime,
        chapter_id: this.selectedChapterId,
      };

      try {
        const response = await fetch(`/api/quiz/${quizId}`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (!response.ok) {
          this.errorMessage = result.message;
          setTimeout(() => {
            this.errorMessage = null;
          }, 5000)
        } else {
          alert(result.message);
          this.$router.push("/quizzes");
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
  },

  async mounted() {
    await this.getChapters();
    await this.getQuizDetails();
  },
};
</script>
