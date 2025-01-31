<template>
  <div class="playlist-container">
    <button @click="goBack" class="back-button">UserDashboard</button>
    <h1>{{ playlistTitle }}</h1>
    <button @click="showAddSongModal = true" class="add-song-button">
      Add Song
    </button>

    <!-- Add Song Modal -->
    <div v-if="showAddSongModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showAddSongModal = false">&times;</span>
        <h2>Add a New Song</h2>
        <form @submit.prevent="submitSong">
          <label for="song-select">Choose a Song:</label>
          <select id="song-select" v-model="newSong.id" required>
            <option
              v-for="availableSong in availableSongs"
              :key="availableSong.id"
              :value="availableSong.id"
            >
              {{ availableSong.title }}
            </option>
          </select>
          <br />
          <button type="submit">Add Song</button>
        </form>
      </div>
    </div>

    <ul class="songs-list">
      <li v-for="song in songs" :key="song.id" class="song-item">
        {{ song.title }} by {{ song.artist }} || Genre: {{ song.genre }}
        <button @click="viewSong(song.id)">View</button>
      </li>
    </ul>
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
      playlistTitle: "My Playlist",
      playlist: [],
      songs: [],
      availableSongs: [],
      showAddSongModal: false,
      playlistId: null,
      newSong: {
        id: "",
      },
    };
  },
  methods: {
    fetchSongs() {
      fetch(`http://127.0.0.1:5001/api/playlists/${this.playlistId}`, {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          this.playlistTitle = data.title;
          this.songs = data.songs || [];
        })
        .catch((error) => console.error("Error fetching songs:", error));
    },
    fetchAvailableSongs() {
      fetch("http://127.0.0.1:5001/api/songs", {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          this.availableSongs = data;
        })
        .catch((error) =>
          console.error("Error fetching available songs:", error)
        );
    },
    viewSong(id) {
      this.$router.push({ name: "song", params: { id } });
    },
    goBack() {
      this.$router.push({ name: "userdashboard" });
    },
    submitSong() {
      const payload = {
        songs: [this.newSong.id], // Backend now expects an array of song IDs
      };
      fetch(`http://127.0.0.1:5001/api/playlists/${this.playlistId}`, {
        method: "PUT",
        headers: getHeaders(),
        body: JSON.stringify(payload),
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((err) => {
              throw new Error(err.error || "Failed to add song to playlist");
            });
          }
          return response.json();
        })
        .then(() => {
          this.showAddSongModal = false;
          this.newSong = { id: "" };
          this.fetchSongs(); // Refresh the song list after adding
        })
        .catch((error) => {
          console.error("Error adding song to playlist:", error);
          alert("Failed to add song to playlist");
        });
    },
  },
  mounted() {
    this.playlistId = this.$route.params.id;
    this.fetchSongs();
    this.fetchAvailableSongs();
  },
};
</script>

<style scoped>
.playlist-container {
  background-color: lightgreen;
  padding: 20px;
  border-radius: 5px;
}

.back-button,
.add-song-button {
  margin-bottom: 10px;
  cursor: pointer;
}

.songs-list {
  list-style: none;
  padding: 0;
}

.song-item {
  margin-bottom: 5px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
}

.close {
  float: right;
  font-size: 28px;
  cursor: pointer;
}
</style>
