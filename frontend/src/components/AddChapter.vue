<template>
  <div class="d-flex justify-content-center">
    <h2>Add Chapters</h2>
  </div>
  <form @submit.prevent="addChapter">
    <div class="d-flex justify-content-center">
      <div style="width: 30%">
        <div class="form-group">
          <label for="name">Chapter Name</label>
          <input type="text" class="form-control" id="name" v-model="name" required />
        </div>
        <div class="form-group">
          <label for="description">Subject Description</label>
          <textarea
            class="form-control"
            id="description"
            v-model="about"
            required
            rows="3"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="subject">Select Subject</label>
          <select class="form-control" id="subject" v-model="selectedSubjectId" required>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>

        <br />
        <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
        <button type="submit" class="btn btn-primary">Add Chapter</button>
      </div>
    </div>
  </form>
</template>


<script>
export default {
  data() {
    return {
      name: "",
      about: "",
      selectedSubjectId: "",
      subjects: [],
      errorMessage: "",
    };
  },
  methods: {
    async getSubjects() {
      try {
        const response = await fetch("/api/subject", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
        this.subjects = data;
      } catch (error) {
        console.log(error);
      }
    },

    async addChapter() {
      this.errorMessage = "";
      const payload = {
        name: this.name,
        about: this.about,
        subject_id: this.selectedSubjectId,
      };

      try {
        const response = await fetch("/api/chapter", {
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
          this.$router.push("/chapters");
        } else {
          this.errorMessage = result.message;
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = "Failed to add chapter. Please try again.";
      }
    },
  },

  mounted() {
    this.getSubjects();
  },

  name: "AddChapter",
};
</script>

