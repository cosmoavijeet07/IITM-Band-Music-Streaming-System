<template>
  <div class="song-page">
    <header>
      <button @click="goBack">
        {{
          userRole === "creator"
            ? "Back to Creator Dashboard"
            : "Back to User Dashboard"
        }}
      </button>
      <h1>{{ song.title }}</h1>
      <button v-if="userRole === 'creator'" @click="editSong">Edit</button>
    </header>
    <div class="song-info">
      <p><strong>Artist:</strong> {{ song.artist }}</p>
      <p><strong>Genre:</strong> {{ song.genre }}</p>
      <p><strong>Release Date:</strong> {{ song.releasedate }}</p>
      <p><strong>Average Rating:</strong> {{ song.rating_count }}</p>
      <p><strong>Album Name:</strong> {{ song.album_title }}</p>
    </div>
    <div v-if="!hasRated">
      <h2>Rate this song</h2>
      <select v-model="rating">
        <option disabled value="">Choose a rating</option>
        <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
      </select>
      <button @click="submitRating">Rate</button>
    </div>
    <div v-else>
      <p>You rated this song: {{ userRating }}</p>
    </div>
    <div class="lyrics">
      <h2>Lyrics</h2>
      <p>{{ song.lyrics }}</p>
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
      song: {},
      songid: null,
      hasRated: false,
      rating: "",
      userRating: null,
      userRole: "user",
    };
  },
  mounted() {
    this.songid = this.$route.params.id;
    this.fetchSongDetails();
    this.userRole = sessionStorage.getItem("user_role");
  },
  methods: {
    goBack() {
      this.$router.push(
        this.userRole === "creator" ? "/creatordashboard" : "/userdashboard"
      );
    },
    editSong() {
      this.$router.push(`/editsong/${this.songid}`);
    },
    fetchSongDetails() {
      fetch(`http://127.0.0.1:5001/api/songs/${this.songid}`, {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          this.song = data;
          this.hasRated = data.hasRated;
          if (this.hasRated) {
            this.userRating = data.rating;
          }
        })
        .catch((error) => console.error("Error fetching song details:", error));
    },
    submitRating() {
      if (!this.rating) {
        alert("Please select a rating.");
        return;
      }
      const payload = {
        rating: this.rating,
        user_id: sessionStorage.getItem("user_id"),
        song_id: this.songid,
      };
      fetch(`http://127.0.0.1:5001/api/ratings`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(payload),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            alert("You have already rated this song.");
          }
        })
        .then((data) => {
          this.hasRated = true;
          this.userRating = this.rating;
          alert(`You have rated this song: ${data.rating} .`);
        })
        .catch((error) => console.error("Error rating song:", error));
    },
  },
};
</script>

<style scoped>
.song-page {
  background-color: #ebf9eb;
  padding: 20px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.lyrics {
  margin-top: 20px;
  border: 1px solid #c4e3c3;
  padding: 10px;
}
</style>
