<template>
  <div class="home-page">
    <!-- Header -->
    <!-- <header class="app-header">
      <img src="../assets/logo.jpeg" alt="IITM-Band Logo" class="logo" />
      <h1>IITM-Band</h1>
    </header> -->

    <!-- Main content with big display boxes -->
    <main class="main-content">
      <div class="display-box" @click="navigateTo('registration')">
        <p>Registration</p>
      </div>
      <div class="display-box" @click="navigateTo('login')">
        <p>User Login</p>
      </div>
      <div class="display-box" @click="navigateTo('creatorlogin')">
        <p>Creator Login</p>
      </div>
    </main>
    <img class="aesthetic-image" src="../assets/1.jpg" alt="Aesthetic View" />
    <!-- Admin Login Button at right bottom corner -->
    <button class="admin-login" @click="navigateTo('adminlogin')">
      Admin Login
    </button>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  methods: {
    // Moved inside the export default
    navigateTo(routeName) {
      console.log(`Navigate to ${routeName}`); // Placeholder for navigation
      this.$router.push({ name: routeName });
    },
  },
};
</script>

<style scoped>
.home-page {
  font-family: "Arial", sans-serif;
  color: #2a2a2a;
}

.app-header {
  display: flex;
  align-items: center;
  background-color: #8fd694;
  padding: 20px;
}

.app-header .logo {
  width: 50px;
  height: auto;
  margin-right: 20px;
}

.main-content {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

.display-box {
  width: 200px;
  height: 200px;
  background-color: #a4deb7;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.display-box:hover {
  transform: scale(1.1);
}

.admin-login {
  position: fixed;
  right: 20px;
  bottom: 20px;
  background-color: #6cc787;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

.aesthetic-image {
  border-radius: 10px;
}
</style>
