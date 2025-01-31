<template>
  <div class="admin-dashboard">
    <div class="header">
      <h1 style="margin: 3px; color: #00695c">ADMIN-Dashboard</h1>
      <button @click="export_csv" class="logout-button">Export CSV</button>
      <button @click="logout" class="logout-button">Logout</button>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div class="stats">
      <div class="stat-item">Number of Users: {{ users.length }}</div>
      <div class="stat-item">Number of Creators: {{ creators.length }}</div>
      <div class="stat-item">Number of Albums: {{ albums.length }}</div>
      <div class="stat-item">Number of Songs: {{ songs.length }}</div>
    </div>
    <div class="dashboard-content">
      <div class="column users">
        <h2>Users</h2>
        <div class="item" v-for="user in users" :key="user.id">
          <span v-if="user.flag" class="emoji-flag">⚠️</span>
          {{ user.username }} is : {{ user.roles[0].name }}
          <button @click="toggleUserFlag(user)">
            {{ user.flag ? "Unflag" : "Flag" }}
          </button>
          <button @click="deleteUser(user.id)">Delete</button>
        </div>
      </div>
      <div class="column albums">
        <h2>Albums</h2>
        <div class="item" v-for="album in albums" :key="album.id">
          {{ album.title }}
          <button @click="deleteAlbum(album.id)">Delete</button>
        </div>
      </div>
      <div class="column songs">
        <h2>Songs</h2>
        <div class="item" v-for="song in songs" :key="song.id">
          <span v-if="song.flag" class="emoji-flag">⚠️</span>
          {{ song.title }} by : {{ song.artist }}
          <button @click="deleteSong(song.id)">Delete</button>
        </div>
      </div>
    </div>
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
      users: [],
      creators: [], // Assuming you have a method to fetch creators
      albums: [],
      songs: [],
      errorMessage: "",
    };
  },
  created() {
    this.fetchUsers();
    this.fetchCreators(); // Ensure you implement this method
    this.fetchAlbums();
    this.fetchSongs();
  },
  methods: {
    async fetchUsers() {
      const response = await fetch("http://127.0.0.1:5001/api/user", {
        method: "GET",
        headers: getHeaders(),
      });
      const data = await response.json();
      this.users = data;
    },
    async fetchCreators() {
      const response = await fetch("http://127.0.0.1:5001/api/user", {
        method: "GET",
        headers: getHeaders(),
      });
      const data = await response.json();
      this.creators = data.filter((creator) =>
        creator.roles.some((role) => role.name === "creator")
      );
    },
    async fetchAlbums() {
      const response = await fetch("http://127.0.0.1:5001/api/albums", {
        method: "GET",
        headers: getHeaders(),
      });
      const data = await response.json();
      this.albums = data;
    },
    async fetchSongs() {
      const response = await fetch("http://127.0.0.1:5001/api/songs", {
        method: "GET",
        headers: getHeaders(),
      });
      const data = await response.json();
      this.songs = data;
    },
    async deleteUser(id) {
      await fetch(`http://127.0.0.1:5001/api/user/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });
      this.fetchUsers();
    },
    async deleteAlbum(id) {
      await fetch(`http://127.0.0.1:5001/api/albums/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });
      this.fetchAlbums();
    },
    async toggleUserFlag(user) {
      await fetch(`http://127.0.0.1:5001/api/flag-user/${user.id}`, {
        method: "PUT",
        headers: getHeaders(),
      });
      this.fetchUsers(); // Refresh the list after toggling
    },
    async deleteSong(id) {
      await fetch(`http://127.0.0.1:5001/api/songs/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });
      this.fetchSongs();
    },
    export_csv() {
      fetch(`http://127.0.0.1:5001/api/export/${this.email}`, {
        method: "GET",
        headers: getHeaders(),
      })
        .then(() => {
          alert("Mail Sent!");
        })
        .catch((error) => {
          console.error("Export Error", error);
        });
    },
    logout() {
      fetch(`http://127.0.0.1:5001/logout`, {
        method: "POST",
        headers: getHeaders(),
      })
        .then(() => {
          sessionStorage.removeItem("auth-token");
          sessionStorage.removeItem("user-roles"); // Clear roles on logout
          this.$router.push("/");
        })
        .catch((error) => {
          console.error("Logout failed:", error);
        });
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  background-color: #e0f2f1;
  padding: 20px;
  justify-content: space-between;
  align-items: center;
  width: 95%;
}

.stats {
  display: flex;
  justify-content: space-around;
  width: 100%;
  padding: 20px 0;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.admin-dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f0fff4; /* Light green background */
}

.logout-button {
  margin: 20px;
  padding: 10px 20px;
  background-color: #31b572; /* Green button */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.dashboard-content {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

.column {
  flex: 1;
  padding: 20px;
}

.item {
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  background-color: #31b572; /* Green button */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  padding: 5px 10px;
}
.emoji-flag {
  margin-right: 5px;
  color: #ffcc00; /* Yellow color for caution */
}
.error-message {
  color: #d32f2f; /* Bright red to catch the user's attention */
  background-color: #ffcdd2; /* Light red background for contrast */
  padding: 10px;
  margin: 20px 0;
  border-radius: 4px;
}
</style>
