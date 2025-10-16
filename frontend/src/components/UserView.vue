<template>
  <Navbar />
  <div class="container mt-5">
    <h1 class="text-center mb-5 text-primary fw-bold">User</h1>

    <div class="container-fluid px-5">
    <div class="mb-3 d-flex justify-content-center">
      <input
        type="text"
        class="form-control w-50"
        v-model="searchQuery"
        placeholder="Enter name..."
      />
      <button class="btn btn-primary ms-2" @click="getusers">Search</button>
    </div>
    </div>

    <!-- Section Wrapper -->
    <div class="container-fluid px-5">
      <div class="mb-5 p-4 bg-white shadow rounded">
        <div class="table-responsive w-80 mx-auto">
          <table class="table table-hover shadow-sm rounded overflow-hidden" id="current">
            <thead class="table-dark text-white">
              <tr>
                <th>Name</th>
                <th>email</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              
              <tr v-for="i in users" :key="i.id">
                <td>{{ i.name }}</td>
                <td>{{ i.email }}</td>
                <td>
                  <button @click="deleteUser(i.id)" class="btn btn-danger">Delete</button>
                </td>
              </tr>
              
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/NavBar.vue";

export default {
  data() {
    return {
      users: [],
      searchQuery: "",
    };
  },
  methods: {
    getusers() {
      fetch(`/api/users?search=${this.searchQuery}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.users = data;
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    },
    async deleteUser(id) {
      const confirmation = confirm("Are you sure you want to delete?");
      if (!confirmation) return;
      try {
        const response = await fetch(`/api/users/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const result = await response.json();
          alert(result.message);
          this.getusers(); // Refresh users list after deletion
        } else {
          alert("Error deleting user.");
        }
      } catch (e) {
        console.error("Error:", e);
        alert("Error deleting user.");
      }
    },
  },
  mounted() {
    this.getusers();
  },
  name: "UserView",
  components: {
    Navbar,
  },
};
</script>
