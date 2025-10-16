<template>
  <Navbar />
  <h2 class="text-center mb-5 text-primary fw-bold">Subjects</h2>

  <form @submit.prevent="addSubject">
    <div class="d-flex justify-content-center">
      <div style="width: 30%">
        <div class="form-group">
          <label for="name">Subject Name</label>
          <input type="text" class="form-control" id="name" v-model="name" required />
        </div>
        <div class="form-group">
          <label for="description">Subject Description</label>
          <input class="form-control" id="description" v-model="about" required rows="3"></input>
        </div>
        <br />
        <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
        <button type="submit" class="btn btn-primary">Add Subject</button>
      </div>
    </div>
  </form>

  <hr />

  <!-- Search Field with Button -->
  <div class="container-fluid px-5">
    <div class="mb-3 d-flex justify-content-center">
      <input
        type="text"
        class="form-control w-50"
        v-model="searchQuery"
        placeholder="Enter subject name..."
      />
      <button class="btn btn-primary ms-2" @click="getsubjects">Search</button>
    </div>

    <div class="mb-5 p-4 bg-white shadow rounded">
      <div class="table-responsive w-80 mx-auto">
        <table class="table table-hover shadow-sm rounded overflow-hidden" id="current">
          <thead class="table-dark text-white">
            <tr>
              <th scope="col">Name</th>
              <th scope="col">About</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subject in subjects" :key="subject.id">
              <td>{{ subject.name }}</td>
              <td>{{ subject.about }}</td>
              <td>
                <router-link :to="`/edit-subject/${subject.id}`" class="btn btn-primary btn-sm"> Edit </router-link>
                &nbsp; &nbsp;
                <button @click="deleteSubject(subject.id)" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="subjects.length === 0" class="text-center text-muted">No subjects found.</p>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/NavBar.vue";

export default {
  data() {
    return {
      subjects: [],
      name: "",
      about: "",
      errorMessage: null,
      searchQuery: "", // Search query input
    };
  },
  methods: {
    async getsubjects() {
      try {
        const response = await fetch(`/api/subject?search=${this.searchQuery}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          this.subjects = await response.json();
        } else {
          console.error("Failed to fetch subjects");
          this.subjects = [];
        }
      } catch (error) {
        console.error("Error fetching subjects:", error);
        this.subjects = [];
      }
    },

    async deleteSubject(id) {
      const confirmation = confirm("Are you sure you want to delete?");
      if (!confirmation) return;

      try {
        const response = await fetch(`/api/subject/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const result = await response.json();
          alert(result.message);
          this.getsubjects(); // Refresh list after deletion
        } else {
          alert("Error deleting subject.");
        }
      } catch (error) {
        console.error(error);
        alert("Error deleting subject.");
      }
    },

    async addSubject() {
      const payload = { name: this.name, about: this.about };

      try {
        const response = await fetch("/api/subject", {
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
          this.getsubjects(); 
          this.name='';
          this.about='';
          this.errorMessage = null;
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

  name: "SubjectView",
  components: { Navbar },
  mounted() {
    this.getsubjects(); // Load subjects on page load
  },
};
</script>
