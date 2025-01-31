<template>
  <div class="unauthorized-container">
    <div class="message">
      <p>
        You’re a bug. Unauthorized Access. Goooo Backkkkkkkk
        <br /><span class="emoji">☠️ 👉🏻</span>
      </p>
    </div>
    <button @click="goHome">Get Out</button>
  </div>
</template>

<script>
export default {
  name: "UnauthorizedAccess",
  methods: {
    goHome() {
      // Redirect to home.
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.unauthorized-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #e8f5e9; /* Light green background */
}

.message {
  color: red;
  font-size: 64px;
  text-align: center;
}

.emoji {
  font-size: 48px;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 20px;
  color: white;
  background-color: green;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: darkgreen;
}
</style>
