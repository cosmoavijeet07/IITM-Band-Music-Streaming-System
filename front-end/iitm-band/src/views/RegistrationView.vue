<template>
  <div class="register-container">
    <h1>Register with IITM-Band</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          pattern="^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
          required
        />
        <span v-if="emailError" class="error-message">{{ emailError }}</span>
      </div>
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          minlength="6"
          title="Password requires atleast 6 characters. "
          pattern=".{6,}"
          required
        />
        <span v-if="passwordError" class="error-message">{{
          passwordError
        }}</span>
      </div>
      <div class="form-group">
        <label>Register as Creator:</label>
        <input
          type="checkbox"
          id="role"
          v-model="role"
          true-value="creator"
          false-value="user"
        />
      </div>
      <div class="register-button">
        <button type="submit" class="submit-btn" center>Register</button>
      </div>
      <div class="form-buttons">
        <button type="button" class="login-btn" @click="login('creator')">
          Creator Login
        </button>
        <button type="button" class="login-btn" @click="login('user')">
          User Login
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      username: "",
      password: "",
      role: "user",
      emailError: null,
      passwordError: null,
      usernameError: null,
    };
  },
  methods: {
    submitForm() {
      if (this.email && this.username && this.password) {
        const formData = {
          email: this.email,
          username: this.username,
          password: this.password,
          role: this.role,
        };
        fetch("http://127.0.0.1:5001/api/user", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        })
          .then((response) => {
            if (!response.ok) {
              return response.json().then((err) => Promise.reject(err));
            }
            return response.json();
          })
          .then((data) => {
            console.log("Success:", data);
            if (this.role === "creator") {
              this.$router.push("/creatorlogin");
            } else {
              this.$router.push("/login");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            if (error.status === 409) {
              if (error.description.includes("email")) {
                this.emailError = error.description;
              } else if (error.description.includes("username")) {
                this.usernameError = error.description;
              }
            }
          });
      }
    },
    validateForm() {
      this.emailError = this.validateEmail(this.email)
        ? null
        : "Please enter a valid email address.";
      this.passwordError = this.validatePassword(this.password)
        ? null
        : "Password must be at least 8 characters long and include a number.";
      return this.emailError === null && this.passwordError === null;
    },
    validateEmail(email) {
      const re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
      return re.test(email);
    },
    validatePassword(password) {
      this.passwordError =
        password.length >= 8 && /\d/.test(password)
          ? null
          : "Password must be at least 8 characters long and include a number.";
      return this.passwordError === null;
    },
    login(type) {
      // Replace these with actual login endpoints or route navigation
      console.log(`${type} login clicked`);
      if (type === "creator") {
        this.$router.push("/creatorlogin");
      } else {
        this.$router.push("/login");
      }
    },
  },
};
</script>

<style>
.register-container {
  max-width: 400px;
  margin: auto;
  background: #f0fff4;
  padding: 20px;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 20px;
}

.register-button {
  margin-bottom: 20px;
}

.label,
.error-message {
  display: block;
}
.input {
  width: 100%;
  padding: 8px;
  margin: 4px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
.error-message {
  color: red;
}
.form-buttons {
  display: flex;
  justify-content: space-between;
}
.submit-btn,
.login-btn {
  background-color: #4caf50; /* Light green background */
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.submit-btn:hover,
.login-btn:hover {
  background-color: #45a049;
}
</style>
