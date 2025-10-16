<template>
    <h1 class="text-center mb-5 text-primary fw-bold">Add Subject</h1>
  <form @submit.prevent="addSubject">
    <div class="d-flex justify-content-center">
      <div style="width: 30%">
        <div class="form-group">
          <label for="name">Subject Name</label>
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
        <br>
        <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
        <button type="submit" class="btn btn-primary">Add Subject</button>
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
      errorMessage: null,
    };
  },
  methods: {
    async addSubject() {

        const payload = {
            name: this.name,
            about: this.about,
        };


        try {
          const response = await fetch("/api/subject", {
            method: "POST",
            headers: {
              Authorization: `Bearer  ${localStorage.getItem("admintoken")}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),

          });
          const result = await response.json();
        
          if (response.ok) {
            alert(result.message);
            this.$router.push("/admin-subjects");
          } else {
            this.errorMessage = result.message;
            
          }
        } catch (error) {
          console.error(error);
        }

    },
  },

  name: "AddSubject",
};
</script>
