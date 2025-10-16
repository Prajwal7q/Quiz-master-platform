<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div style="width: 30%">
      <h2 class="display-4 text-primary mb-4">Edit Chapter</h2>
      <form @submit.prevent="editChapter">
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" class="form-control" id="name" v-model="name" />
        </div>
        <div class="form-group">
          <label for="description">About</label>
          <textarea
            class="form-control"
            id="description"
            v-model="about"
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
        <button type="submit" class="btn btn-primary">Edit Chapter</button>
      </form>
    </div>
  </div>
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
        if (response.ok) {
          this.subjects = await response.json();
        }
      } catch (error) {
        console.log(error);
      }
    },
    async getChapterDetails() {
      const chapterId = this.$route.params.id;
      try {
        const response = await fetch(`/api/chapter/${chapterId}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          const chapter = await response.json();
          this.name = chapter.name;
          this.about = chapter.about;
          this.selectedSubjectId = chapter.subject_id;
        } else {
          alert("Failed to load chapter details");
        }
      } catch (error) {
        console.log(error);
      }
    },
    async editChapter() {
      const payload = {
        name: this.name,
        about: this.about,
        subject_id: this.selectedSubjectId,
      };
      const chapterId = this.$route.params.id;
      try {
        const response = await fetch(`/api/chapter/${chapterId}`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });
        if (response.ok) {
          alert("Chapter updated successfully");
          this.$router.push("/chapters");
        } else {
          this.errorMessage = "Failed to update chapter";
          setTimeout(() => {
            this.errorMessage = null;
          }, 5000)
        }
      } catch (error) {
        alert(error);
      }
    },
  },
  async mounted() {
    await this.getSubjects();
    await this.getChapterDetails();
  },
  name: "EditChapter",
};
</script>
