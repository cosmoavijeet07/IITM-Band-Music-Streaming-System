<template>
  <div class="edit-song-page">
    <h1>Edit Song</h1>
    <form @submit.prevent="submitForm">
      <label for="title">Title:</label>
      <input v-model="song.title" type="text" id="title" required />

      <label for="artist">Artist:</label>
      <input v-model="song.artist" type="text" id="artist" required />

      <label for="lyrics">Lyrics:</label>
      <textarea v-model="song.lyrics" id="lyrics" required></textarea>

      <label for="genre">Genre:</label>
      <input v-model="song.genre" type="text" id="genre" required />

      <button type="submit">Submit</button>
    </form>
    <button @click="goBack">Back to Dashboard</button>
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
      song: {
        title: "",
        artist: "",
        lyrics: "",
        genre: "",
      },
      songId: this.$route.params.id,
    };
  },
  methods: {
    fetchSong() {
      fetch(`http://127.0.0.1:5001/api/songs/${this.songId}`, {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          this.song = data;
        })
        .catch((error) => console.error("Error fetching song details:", error));
    },
    submitForm() {
      fetch(`http://127.0.0.1:5001/api/songs/${this.songId}`, {
        method: "PUT",
        headers: getHeaders(),
        body: JSON.stringify(this.song),
      })
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not ok");
          alert("Song updated successfully!");
        })
        .catch((error) => {
          console.error("Error updating song:", error);
          alert("Failed to update song.");
        });
    },
    goBack() {
      this.$router.push("/creatordashboard");
    },
  },
  mounted() {
    this.fetchSong();
  },
};
</script>

<style scoped>
.edit-song-page {
  background-color: #e4f9f5;
  padding: 20px;
  border-radius: 10px;
}

label {
  margin-top: 10px;
  display: block;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #b8e994;
  color: #333;
  padding: 10px 20px;
  margin-top: 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #a9db8f;
}
</style>
