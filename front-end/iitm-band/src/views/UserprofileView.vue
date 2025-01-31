<template>
  <div class="user-profile">
    <h1>User Profile</h1>
    <div v-if="user">
      <p><strong>Username:</strong> {{ user.user_name }}</p>
      <p><strong>Email:</strong> {{ email }}</p>
      <p><strong>Role:</strong> {{ user.role }}</p>
      <button v-if="user.role === 'user'" @click="changeRole('creator')">
        Switch to Creator
      </button>
    </div>
    <div v-else>
      <p>User information is not available.</p>
    </div>
    <button @click="goBack">Go Back to User Dashboard</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      email: "",
    };
  },
  methods: {
    fetchUserData() {
      this.email = sessionStorage.getItem("email");
      fetch(`http://127.0.0.1:5001/api/user/${this.email}`, {
        method: "GET",
        headers: this.getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.error) {
            this.user = data;
          } else {
            console.error(data.error);
          }
        })
        .catch((error) => console.error("Error:", error));
    },
    changeRole(newRole) {
      fetch(`http://127.0.0.1:5001/api/user/${this.email}`, {
        method: "PUT",
        headers: this.getHeaders(),
        body: JSON.stringify({ role: newRole }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            alert(data.message);
            this.fetchUserData();
            sessionStorage.setItem("user_role", data.role);
          } else {
            console.error(data.error);
          }
        })
        .catch((error) => console.error("Error:", error));
    },
    goBack() {
      this.$router.push("/userdashboard");
    },
    getHeaders() {
      const headers = {
        "Content-Type": "application/json",
      };
      const auth_token = sessionStorage.getItem("auth-token");
      if (auth_token) {
        headers["Authentication-Token"] = `${auth_token}`;
      }

      return headers;
    },
  },
  created() {
    this.fetchUserData();
  },
};
</script>

<style scoped>
.user-profile {
  background-color: #e0f2f1;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  margin: auto;
}

button {
  background-color: #a5d6a7;
  border: none;
  padding: 10px;
  margin: 5px;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #81c784;
}
</style>
