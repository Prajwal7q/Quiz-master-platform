<template>
  <h1 class="text-center mb-5 text-primary fw-bold">Add Quiz</h1>
  <div class="d-flex justify-content-center">
    <form @submit.prevent="addQuiz" style="width: 50%">
      <div class="mb-3">
        <label for="name" class="form-label">Quiz Name</label>
        <input
          type="text"
          class="form-control form-control-sm"
          id="name"
          v-model="name"
          required
        />
      </div>
      <label for="name" class="form-label">Duration (in minutes)</label>
      <div class="mb-3">
        <input
          class="form-control form-control-sm"
          type="number"
          id="duration"
          name="duration"
          v-model.number="duration"
          min="0"
          max="300"
          required
        />
      </div>
      <div class="mb-3">
        <label for="startDate" class="form-label">Start Date</label>
        <input
          type="date"
          class="form-control form-control-sm"
          id="startDate"
          v-model="startDate"
          required
        />
      </div>
      <div class="mb-3">
        <label for="startTime" class="form-label">Start Time</label>
        <input
          type="time"
          class="form-control form-control-sm"
          id="startTime"
          v-model="startTime"
          required
        />
      </div>
      <div class="mb-3">
        <label for="endDate" class="form-label">End Date</label>
        <input
          type="date"
          class="form-control form-control-sm"
          id="endDate"
          v-model="endDate"
          required
        />
      </div>
      <div class="mb-3">
        <label for="endTime" class="form-label">End Time</label>
        <input
          type="time"
          class="form-control form-control-sm"
          id="endTime"
          v-model="endTime"
          required
        />
      </div>
      <div class="mb-3">
        <label for="chapter" class="form-label">Select Chapter</label>
        <select
          class="form-control form-control-sm"
          id="chapter"
          v-model="selectedChapterId"
          required
          style="appearance: menulist"
        >
          <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
            {{ chapter.name }}
          </option>
        </select>
      </div>
      <br /><br />
      <div class="d-flex justify-content-center">
        <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
      </div>
      <div class="d-flex justify-content-center">
        <button type="submit" class="btn btn-primary btn-lg">Add Quiz</button>
      </div>
    </form>
  </div>
  <br /><br /><br /><br /><br />
</template>

<script>
export default {
  name: "AddQuiz",

  data() {
    return {
      name: "",
      duration: "",
      startDate: "",
      startTime: "",
      endDate: "",
      endTime: "",
      selectedChapterId: "",
      errorMessage: "",
      chapters: [],
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

        const data = await response.json();
        this.chapters = data;
      } catch (error) {
        console.log(error);
      }
    },

    async addQuiz() {
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
        const response = await fetch("/api/quiz", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (!response.ok) {
          // ❌ You were checking `result.ok`, which is incorrect.
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

  mounted() {
    this.getChapters();
  },
};
</script>
