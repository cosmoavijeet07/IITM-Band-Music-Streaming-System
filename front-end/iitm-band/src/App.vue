<template>
  <nav>
    <img src="@/assets/logo.jpeg" alt="IITM-Band Logo" />
    <h1>IITM-Band</h1>
  </nav>
  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  background-color: #b2d8b4; /* Light green background */
  padding: 10px 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

nav h1 {
  font-size: 32px; /* Moderately large font size */
  color: #2c3e50; /* Font color */
  margin-left: 20px; /* Space between logo and title */
}

nav img {
  height: 50px; /* Smaller logo size */
  width: auto;
}
</style>
