<template>
  <Navbar />
  <br>

  <div class="d-flex justify-content-end">
    <button class="btn btn-success" @click="exportData">Export Data</button>
  </div>

  <h1 class="text-center mb-5 text-primary fw-bold">Admin Dashboard</h1>

  <div class="row">
    <!-- Total Students Card -->
    <div class="col-md-6 mb-4">
      <div class="card text-center">
        <div class="card-header bg-primary text-white">Total Students</div>
        <div class="card-body">
          <p class="display-4">{{ total_student }}</p>
        </div>
      </div>
    </div>

    <!-- Average Score Card -->
    <div class="col-md-6 mb-4">
      <div class="card text-center">
        <div class="card-header bg-success text-white">Average Score</div>
        <div class="card-body">
          <p class="display-4">{{ avg_score }}</p>
        </div>
      </div>
    </div>
  </div>

  <div class="text-center"><h4>User Performance Chart</h4></div>
  <div class="row">
    <div class="col-md-6">
      <div class="chart-container text-center mt-4" style="border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
        <img v-if="piechartUrl" :src="piechartUrl" alt="User Pie Chart" class="img-fluid" />
        <p v-else>Loading Chart...</p>
      </div>
    </div>
    <div class="col-md-6">
      <div class="chart-container text-center mt-4" style="border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
        <img v-if="barchartUrl" :src="barchartUrl" alt="User Bar Chart" class="img-fluid" />
        <p v-else>Loading Chart...</p>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/NavBar.vue";

export default {
  data() {
    return {
      total_student: 0,
      avg_score: 0,
      barchartUrl: null,
      piechartUrl: null,
    };
  },

  methods: {
    getData() {
      const toKen = localStorage.getItem("admintoken");
      if (!toKen) {
        this.$router.push("/"); // Redirect if not logged in
        return;
      }
      
      fetch("/api/admin", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.total_student = data.total_students;
          this.avg_score = data.avg_score;
        })
        .catch((error) => {
          console.error("Error fetching admin data:", error);
        });
    },
    async exportData() {
  try {
    const response = await fetch("/api/export/data", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
      },
    });

    if (!response.ok) {
      const contentType = response.headers.get("content-type");
      if (contentType.includes("application/json")) {
        const result = await response.json(); // Extract error message if any
        alert(result.message || "Failed to export data");
      }
      else {
        alert("Failed to export data:Server returned a non-JSON response");
        return;
      }
      
      return;
    }

    // ✅ Convert response to Blob (Binary Large Object for file handling)
    const blob = await response.blob();

    // ✅ Create a URL and trigger download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data_export.csv"; // ✅ Set the download file name
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

  } catch (error) {
    console.error("Export error:", error);
    alert("Error exporting data");
  }
  finally{
    this.exporting = false
  }
},

    async fetchChart1() {
      try {
        const token = localStorage.getItem("admintoken");
        const response = await fetch("/api/admin_pie_chart/image", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const blob = await response.blob(); // Convert response to blob
        this.piechartUrl = URL.createObjectURL(blob); // Create image URL
      } catch (error) {
        console.log("Error fetching chart data:", error);
      }
  },
  async fetchChart2() {
      try {
        const token = localStorage.getItem("admintoken");
        const response = await fetch("/api/admin_bar_chart/image", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("admintoken")}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const blob = await response.blob(); // Convert response to blob
        this.barchartUrl = URL.createObjectURL(blob); // Create image URL
      } catch (error) {
        console.log("Error fetching chart data:", error);
      }
        

  },
},

  mounted() {
    this.getData();
    this.fetchChart1();
    this.fetchChart2();
  },

  name: "AdminDashboard",
  components: {
    Navbar,
  },
};
</script>
