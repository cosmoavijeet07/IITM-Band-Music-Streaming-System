<template>
  <div class="creator-login">
    <h2>Admin Login</h2>
    <form @submit.prevent="login">
      <!-- Corrected method name -->
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          type="text"
          id="email"
          v-model="email"
          placeholder="Enter email"
          required
        />
      </div>
      <!-- Corrected v-model -->
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter password"
          required
        />
      </div>
      <!-- Corrected v-model -->
      <button type="submit" :disabled="isLoading">Login</button>
      <button type="button" @click="goBack" class="back-button">Back</button>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </form>
  </div>
</template>

<script>
function getHeaders() {
  const headers = {
    "Content-Type": "application/json",
  };
  const auth_token = sessionStorage.getItem("auth-token");
  if (auth_token) {
    headers["Authentication-Token"] = `${auth_token}`;
  }

  return headers;
}

export default {
  data() {
    return {
      email: "",
      password: "",
      auth: null,
      user_id: 1,
      isLoading: false, // You referenced this in your template, so it should be declared here.
      errorMessage: "", // This too, to handle potential error messages.
    };
  },
  methods: {
    async login() {
      this.isLoading = true; // Set loading to true at the start of the login attempt
      try {
        const response = await fetch(
          "http://127.0.0.1:5001/login?include_auth_token",
          {
            method: "POST",
            headers: {
              "Access-Control-Allow-Origin": "*",
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Invalid credentials");
        }

        const data = await response.json();
        if (data.response) {
          this.auth = data.response.user.authentication_token;
          sessionStorage.setItem("auth-token", this.auth);
          sessionStorage.setItem("email", this.email);
          fetch(`http://127.0.0.1:5001/api/user/${this.email}`, {
            method: "GET",
            headers: getHeaders(),
          })
            .then((response) => response.json())
            .then((data) => {
              //   this.user_name = data.user_name;
              this.user_id = data.user_id;
              sessionStorage.setItem("user_id", data.user_id);
              sessionStorage.setItem("user_name", data.user_name);
              sessionStorage.setItem("user_role", data.role);
              sessionStorage.setItem("user_flag", data.flag);
              if (data.role === "admin") {
                this.$router.push("/admindashboard");
              } else {
                this.$router.push("/unauthorisedadmin");
              }
            })
            .catch(() => console.log("Error getting user info"));

          console.log(data); // Handle successful login response
          // You might want to redirect the user or do some other action on successful login
        }
      } catch (error) {
        console.error("Error:", error); // Handle login error
        this.errorMessage = error.message; // Display error message to the user
      } finally {
        this.isLoading = false; // Reset loading state whether login was successful or failed
      }
    },
    goBack() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* New styles for the light green color scheme and improved design */
.creator-login {
  background-color: #e8f5e9; /* Light green background */
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: auto;
}

h2 {
  color: #2e7d32; /* Darker shade of green for contrast */
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  color: #388e3c; /* Green text for labels */
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
  border: 1px solid #c8e6c9; /* Light green border */
  border-radius: 4px;
}

button[type="submit"],
.back-button {
  width: 100%;
  padding: 0.5rem;
  margin-top: 1rem;
  cursor: pointer;
  background-color: #4caf50; /* Green background */
  color: white;
  border: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.back-button {
  background-color: #81c784; /* Lighter green for differentiation */
}

button[type="submit"]:hover,
.back-button:hover {
  background-color: #388e3c; /* Darker green on hover */
}

.error-message {
  color: #d32f2f; /* Error message in red for visibility */
  margin-top: 1rem;
}
</style>
