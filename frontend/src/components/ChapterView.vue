<template>
  <Navbar />
  <h2 class="text-center mb-5 text-primary fw-bold">Chapters</h2>
  <!-- <AddChapter /> -->
  <form @submit.prevent="addChapter">
    <div class="d-flex justify-content-center">
      <div style="width: 30%">
        <div class="form-group">
          <label for="name">Chapter Name</label>
          <input type="text" class="form-control" id="name" v-model="name" required />
        </div>
        <div class="form-group">
          <label for="description">Chapter Description</label>
          <input
            class="form-control"
            id="description"
            v-model="about"
            required
            rows="3"
          ></input>
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

  <!-- <div class="d-flex justify-content-end">
    <router-link to="/add-chapter" class="btn btn-success mb-3"
      >Add New Chapter</router-link
    >
  </div> -->
  <hr />
  <div class="container-fluid px-5">
    <div class="mb-3 d-flex justify-content-center">
      <input
        type="text"
        class="form-control w-50"
        v-model="searchQuery"
        placeholder="Enter chapter name..."
      />
      <button class="btn btn-primary ms-2" @click="getChapters">Search</button>
    </div>



  <div class="container-fluid px-5">
      <div class="mb-5 p-4 bg-white shadow rounded">
        <div class="table-responsive w-80 mx-auto">
        <table class="table table-striped table-bordered">
          <thead class="table-dark">
            <tr>
              <th scope="col">Name</th>
              <th scope="col">About</th>
              <th scope="col">Subject</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="chapter in chapters" :key="chapter.id">
              <td>{{ chapter.name }}</td>
              <td>{{ chapter.about }}</td>
              <!-- <td>{{ chapter.subject_name }}</td> -->
              <td>{{ chapter.subject_name }}</td>
              <td>
                <router-link
                  :to="`/edit-chapter/${chapter.id}`"
                  class="btn btn-primary btn-sm"
                >
                  Edit
                </router-link>
                &nbsp; &nbsp;
                <button @click="deleteChapter(chapter.id)" class="btn btn-danger btn-sm">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="chapters.length === 0" class="text-center text-muted">No chapters found.</p>

      </div>
    </div>
  </div>
  </div>
</template>

<script>
import Navbar from "@/components/NavBar.vue";
// import AddChapter from "@/components/AddChapter.vue";

export default {
  data() {
    return {
      chapters: [],
      name: "",
      about: "",
      selectedSubjectId: "",
      subjects: [],
      errorMessage: "",
      searchQuery: "",
    };
  },

  methods: {
    getChapters() {
      fetch(`/api/chapter?search=${this.searchQuery}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.chapters = data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async deleteChapter(id) {
      const confirmation = confirm("Are you sure you want to delete?");
      if (!confirmation) return;

      try {
        const response = await fetch(`/api/chapter/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const result = await response.json();
          alert(result.message);
          this.getChapters();
          this.$router.push("/chapters");
        } else {
          alert("Error Deleting Chapter.");
        }
      } catch (e) {
        console.error(e);
        alert("Error Deleting Chapter.");
      }
    },
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
          this.getChapters();
          this.name='';
          this.about='';
          this.selectedSubjectId='';
          this.errorMessage = "";

        } else {
          this.errorMessage = result.message;
          setTimeout(() => {
            this.errorMessage = null;
          }, 5000)
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = "Failed to add chapter. Please try again.";
      }
    },
  },

  mounted() {
    this.getChapters();
    this.getSubjects();
  },

  name: "ChapterView",
  components: {
    Navbar,
    // AddChapter
  },
};
</script>
