<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div style="width: 30%">
      <h2 class="display-4 text-primary mb-4">Edit Subject</h2>
      <form @submit.prevent="editSubject">
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" class="form-control" id="name" v-model="subject.name" />
        </div>
        <div class="form-group">
          <label for="description">About</label>
          <textarea class="form-control" id="description" v-model="subject.about" rows="3"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Edit Subject</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      subject: {
        name: '',
        about: '',
      },
    };
  },
  mounted() {
    this.getSubjectById();
  },
  methods: {
    async getSubjectById() {
      const subjectId = this.$route.params.id;
      try {
        const response = await fetch(`/api/subject/${subjectId}`, {
          method: 'GET',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("admintoken")}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.subject = data; // Assign fetched data to subject
        } else {
          alert('Failed to fetch subject details');
        }
      } catch (error) {
        console.error('Error fetching subject:', error);
      }
    },
    async editSubject() {
      const subjectId = this.$route.params.id;
      try {
        const response = await fetch(`/api/subject/${subjectId}`, {
          method: 'PUT',
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("admintoken")}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.subject),
        });

        if (response.ok) {
          alert('Subject updated successfully');
          this.$router.push('/admin-subjects');
        } else {
          alert('Failed to update subject');
        }
      } catch (error) {
        console.error('Error updating subject:', error);
      }
    }
  },
  name: "EditSubject",
};
</script>
