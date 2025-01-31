<template>
  <div class="album-page">
    <button @click="navigateBack">
      {{
        userRole === "creator"
          ? "Back to Creator Dashboard"
          : "Back to User Dashboard"
      }}
    </button>
    <h1>{{ album.title }}</h1>
    <p>{{ album.description }}</p>
    <div class="songs-list">
      <h2>Songs</h2>
      <div class="song" v-for="song in songs" :key="song.id">
        <p>{{ song.title }}</p>
        <button @click="viewSong(song.id)">View Song</button>
        <button v-if="userRole === 'creator'" @click="editSong(song.id)">
          Edit
        </button>
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
  name: "AlbumPage",
  data() {
    return {
      album: {},
      songs: [],
      userRole: "user",
      albumId: null,
    };
  },
  methods: {
    fetchAlbumDetails(albumId) {
      fetch(`http://127.0.0.1:5001/api/albums/${albumId}`, {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          this.album = data;
          this.songs = data.songs || [];
        })
        .catch((error) => console.error("Error:", error));
    },
    viewSong(songId) {
      this.$router.push(`/song/${songId}`);
    },
    editSong(songId) {
      this.$router.push(`/editsong/${songId}`);
    },
    navigateBack() {
      this.$router.push(
        this.userRole === "creator" ? "/creatordashboard" : "/userdashboard"
      );
    },
  },
  mounted() {
    this.albumId = this.$route.params.id; // Properly accessing route params
    this.userRole = sessionStorage.getItem("user_role"); // Assuming roles are stored in session storage
    this.fetchAlbumDetails(this.albumId);
  },
};
</script>

<style scoped>
.album-page {
  background-color: #ebf9eb;
  padding: 20px;
  border-radius: 8px;
}

.songs-list {
  margin-top: 20px;
}

.song {
  margin-bottom: 10px;
}

button {
  background-color: #a2d5a2;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 5px;
}

button:hover {
  background-color: #8cc98c;
}
</style>
