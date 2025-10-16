<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card-body text-center">
      <h5 class="card-title">Sign Up</h5>
      <br />
      <form @submit.prevent="signup">
        <div class="form-floating mb-3 mx-auto d-block col-6">
          <input
            type="text"
            class="form-control"
            id="floatingFullName"
            placeholder="Full Name"
            v-model="fullName"
            required
          />
          <label for="floatingFullName">Full Name</label>
        </div>
        <div class="form-floating mb-3 mx-auto d-block col-6">
          <input
            type="email"
            class="form-control"
            id="floatingInput"
            placeholder="Email"
            v-model="email"
            required
          />
          <label for="floatingInput">Email</label>
        </div>
        <div class="form-floating mb-3 mx-auto d-block col-6">
          <input
            type="password"
            class="form-control"
            id="floatingPassword"
            placeholder="Password"
            v-model="password"
            required
          />
          <label for="floatingPassword">Password</label>
        </div>
        <div v-if="errorMessage" class="text-danger">{{ errorMessage }}</div>
        
        <button type="submit" class="btn btn-success">Sign Up</button>
        <br /> or <br /> 
        <router-link to="/student-login" class="btn btn-primary">Back to Login </router-link>
      </form>
      <br />
    </div>
  </div>

</template>

<script>
export default {
  data() {
    return {
      fullName: "",
      email: "",
      password: "",
      errorMessage: null,
      
    };
  },
  methods: {
    async signup() {
      this.errorMessage = null;
      

      const payload = {
        name: this.fullName, // Fixed: It should be this.fullName instead of this.name
        email: this.email,
        password: this.password,
        role: "user"
      };

      try {
        const response = await fetch("/api/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
          this.errorMessage = result.message || "Something went wrong";
        } else {
          alert(result.message + ", Please Login to continue...");
          this.$router.push("/student-login");
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = "Server error. Please try again.";
      }
    }
  }
};
</script>