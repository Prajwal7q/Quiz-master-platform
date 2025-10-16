<template>
<div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card-body text-center">
        <h5 class="card-title">Welcome to Quiz Menia</h5>
        <br>
        <form @submit.prevent="adminlogin">
            <div class="form-floating mb-3 mx-auto d-block col-6">
                <input type="email" class="form-control" id="floatingInput" placeholder="Email" v-model="email" required>
                <label for="floatingInput">Email</label>
            </div>
            <div class="form-floating mb-3 mx-auto d-block col-6">
                <input type="password" class="form-control" id="floatingPassword" placeholder="Password" v-model="password" required>
                <label for="floatingPassword">Password</label>
            </div>
            <div v-if="errorMessage" class="text-danger"> {{ errorMessage }} </div>    
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <br>
    </div>
</div>

</template>

<script>
export default {
    data() {
        return {
            email: "",
            password: "",
            errorMessage: null,
        };
    },
    methods: {
        async adminlogin() {
            this.errorMessage = null;

            const payload = {
                email: this.email,
                password: this.password,
            };
            try{
                const response = await fetch("/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(payload),
                });

                const result = await response.json();

                if (!response.ok) {
                    this.errorMessage = result.message || "Something went wrong";
                }else {
                    if (result.user_role == "admin") {
                        alert("Admin Login Successful")
                        localStorage.setItem("admintoken", result.token);
                        this.$router.push("/admin-dashboard");
                    }else {
                        this.errorMessage = "You are not an admin";
                        return;
                    }
                    // alert("Login Successful")
                    // localStorage.setItem("admintoken", result.token);
                    // this.$router.push("/admin-dashboard");
                }

            }catch(error) {
                this.errorMessage = "Unable to connect to server";
                console.error(error);
            }
        },
    },
    name: "AdminLogin",
};
</script>