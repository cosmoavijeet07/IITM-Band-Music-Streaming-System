<template>
  <div id="app" class="container">
    <h1>Create Playlist</h1>
    <form @submit.prevent="createPlaylist">
      <div class="input-group">
        <label for="playlistName">Playlist Name:</label>
        <input
          type="text"
          id="playlistName"
          v-model="playlistName"
          placeholder="Enter playlist name"
          required
        />
      </div>

      <h3>Songs:</h3>
      <div class="song-list">
        <label>Song selection:</label>
        <div class="input-group" v-for="song in allSongs" :key="song.id">
          <input type="checkbox" v-model="selectedSongs" :value="song.id" />
          {{ song.title }}
        </div>
      </div>

      <div class="button-group">
        <button type="submit">Create Playlist</button>
      </div>
    </form>
    <br />
    <button @click="goBack" class="back-button">UserDashboard</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      playlistName: "",
      allSongs: [],
      selectedSongs: [],
    };
  },
  created() {
    this.fetchSongs();
  },
  methods: {
    fetchSongs() {
      fetch("http://127.0.0.1:5001/api/songs", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": `${sessionStorage.getItem("auth-token")}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.allSongs = data;
        })
        .catch((error) => console.error("Error:", error));
    },
    goBack() {
      this.$router.push({ name: "userdashboard" });
    },
    createPlaylist() {
      const data = {
        title: this.playlistName,
        user_id: sessionStorage.getItem("user_id"),
        songs: this.selectedSongs,
      };
      fetch("http://127.0.0.1:5001/api/playlists", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": `${sessionStorage.getItem("auth-token")}`,
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to create playlist");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data.id);
          alert(`Playlist created successfully!`);
          this.playlistName = ""; // Reset playlist name
          this.selectedSongs = []; // Reset selected songs
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Failed to create playlist. Please try again.");
        });
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background-color: #e6ffe6;
}

.input-group {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.input-group input {
  flex-grow: 1;
  margin-right: 10px;
}

button {
  padding: 8px 16px;
  background-color: #aaffaa;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #77cc77;
}
</style>
