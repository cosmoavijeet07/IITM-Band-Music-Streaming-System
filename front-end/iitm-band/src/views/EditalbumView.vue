<template>
  <div class="edit-album">
    <h1>Edit Album</h1>
    <form @submit.prevent="submitAlbum">
      <div>
        <label for="title">Album Title:</label>
        <input type="text" id="title" v-model="album.title" required />
      </div>
      <div>
        <label for="description">Album Description:</label>
        <textarea id="description" v-model="album.description"></textarea>
      </div>
      <div v-for="(songId, index) in album.songIds" :key="index">
        <input
          type="text"
          placeholder="Search for songs"
          @input="searchSongs($event, index)"
        />
        <select
          v-model="album.songIds[index]"
          v-if="filteredSongs[index] && filteredSongs[index].length"
        >
          <option
            v-for="song in filteredSongs[index]"
            :key="song.id"
            :value="song.id"
          >
            {{ song.title }} by {{ song.artist }}
          </option>
        </select>
        <button type="button" @click="removeSongField(index)">
          Remove Song
        </button>
      </div>
      <button type="button" @click="addSongField">Add Song</button>
      <button type="submit">Submit</button>
      <button type="button" @click="goBack">Back to Dashboard</button>
    </form>
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
      album: {
        title: "",
        description: "",
        songIds: [], // Store only song IDs
      },
      allSongs: [],
      filteredSongs: [], // Array to store filtered songs for each song field
      albumId: this.$route.params.id,
    };
  },
  methods: {
    async fetchAlbum() {
      const response = await fetch(
        `http://127.0.0.1:5001/api/albums/${this.albumId}`,
        {
          method: "GET",
          headers: getHeaders(),
        }
      );
      const data = await response.json();
      this.album = {
        title: data.title,
        description: data.description,
        songIds: data.songs.map((song) => song.id),
      };
      this.album.songIds.forEach(() => {
        this.filteredSongs.push([]);
      });
    },
    async fetchSongs() {
      const response = await fetch(`http://127.0.0.1:5001/api/songs`, {
        method: "GET",
        headers: getHeaders(),
      });
      this.allSongs = await response.json();
      const userId = sessionStorage.getItem("user_id");
      this.allSongs = this.allSongs.filter(
        (song) => song.user_id === parseInt(userId)
      );
    },
    addSongField() {
      this.album.songIds.push(null);
      this.filteredSongs.push([]); // Initialize empty list for new song field
    },
    removeSongField(index) {
      this.album.songIds.splice(index, 1);
      this.filteredSongs.splice(index, 1);
    },
    searchSongs(event, index) {
      const searchQuery = event.target.value.toLowerCase();
      if (searchQuery.length > 0) {
        this.filteredSongs[index] = this.allSongs.filter((song) =>
          song.title.toLowerCase().includes(searchQuery)
        );
      } else {
        this.filteredSongs[index] = [];
      }
    },
    async submitAlbum() {
      const albumData = {
        title: this.album.title,
        description: this.album.description,
        assign_songs: this.album.songIds.filter((id) => id !== null),
      };
      await fetch(`http://127.0.0.1:5001/api/albums/${this.albumId}`, {
        method: "PUT",
        headers: getHeaders(),
        body: JSON.stringify(albumData),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json(); // Assuming the server responds with JSON
        })
        .then((data) => {
          console.log(data);
          alert("Album updated successfully!");
          this.$router.push("/creatordashboard");
        })
        .catch((error) => {
          alert(`Failed to update album${error}`);
        });
    },
    goBack() {
      this.$router.push("/creatordashboard");
    },
  },
  created() {
    this.fetchAlbum();
    this.fetchSongs();
  },
};
</script>

<style scoped>
.edit-album {
  background-color: #d4edda;
  padding: 20px;
  border-radius: 5px;
}

label {
  display: block;
  margin: 10px 0 5px;
}

input,
textarea,
select,
button {
  margin-top: 5px;
}
</style>
