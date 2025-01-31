<template>
  <div id="app">
    <div class="header" style="background-color: lightgreen; padding: 20px">
      <span
        >Welcome,
        <h1 style="margin: 3px; color: #00695c">{{ userName }}</h1>
        <span v-if="userFlag" class="emoji-flag">Flagged!!⚠️</span>
        <span v-if="isCreator" style="color: blueviolet">Creator</span></span
      ><br />
      <button @click="navigateToDashboard">User Dashboard</button>
      <button @click="showCreateSongModal = true">Create Song</button>
      <button @click="showCreateAlbumModal = true">Create Album</button>
      <button @click="logout">Logout</button>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <div class="main-content">
      <div class="songs-column">
        <h2>Songs</h2>
        <ul>
          <li v-for="song in songs" :key="song.id">
            <span v-if="song.flag" class="emoji-flag">⚠️</span>
            {{ song.title }} by: {{ song.artist }} in {{ song.genre }}
            <button @click="viewSong(song.id)">View</button>
            <button @click="editSong(song.id)">Edit</button>
            <button @click="deleteSong(song.id)">Delete</button>
          </li>
        </ul>
      </div>

      <div class="albums-column">
        <h2>Albums</h2>
        <ul>
          <li v-for="album in albums" :key="album.id">
            {{ album.title }}
            <button @click="viewAlbum(album.id)">View</button>
            <button @click="editAlbum(album.id)">Edit</button>
            <button @click="deleteAlbum(album.id)">Delete</button>
          </li>
        </ul>
      </div>
    </div>

    <!-- Modals for creating/editing songs and albums would go here -->

    <!-- Modal for Creating Songs -->
    <div v-if="showCreateSongModal" class="modal">
      <div class="modal-content">
        <span @click="toggleCreateSongModal" class="close">&times;</span>
        <h2>Create Song</h2>
        <form @submit.prevent="createSong">
          <input
            class="createsong"
            type="text"
            v-model="newSong.title"
            placeholder="Title"
            required
          />
          <input
            type="text"
            class="createsong"
            v-model="newSong.artist"
            placeholder="Artist"
            required
          />
          <textarea
            v-model="newSong.lyrics"
            placeholder="Lyrics"
            class="createsong"
            rows="10"
            required
          ></textarea>
          <input
            type="text"
            class="createsong"
            v-model="newSong.genre"
            placeholder="Genre"
            required
          />
          <select v-model="newSong.album_id">
            <option value="" disabled selected>Select Album</option>
            <option v-for="album in albums" :value="album.id" :key="album.id">
              {{ album.title }}
            </option>
          </select>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>

    <!-- Modal for Creating Albums -->
    <div v-if="showCreateAlbumModal" class="modal">
      <div class="modal-content">
        <span @click="toggleCreateAlbumModal" class="close">&times;</span>
        <h2>Create Album</h2>
        <form @submit.prevent="createAlbum">
          <input
            type="text"
            class="createalbum"
            v-model="newAlbum.title"
            placeholder="Title"
            required
          />
          <textarea
            v-model="newAlbum.description"
            class="createalbum"
            placeholder="Description"
            rows="5"
          ></textarea>
          <button type="submit">Submit</button>
        </form>
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
      userName: "User Name",
      userFlag: false,
      userId: null,
      isCreator: true, // This should be set based on the user's role
      songs: [],
      albums: [],
      showCreateSongModal: false,
      showCreateAlbumModal: false,
      errorMessage: "",
      newSong: {
        title: "",
        artist: "",
        lyrics: "",
        genre: "",
        album_id: null,
      },
      newAlbum: {
        title: "",
        description: "",
      },
    };
  },
  methods: {
    navigateToDashboard() {
      this.$router.push({ name: "userdashboard" });
    },
    logout() {
      fetch(`http://127.0.0.1:5001/logout`, {
        method: "POST",
        headers: getHeaders(),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Logout failed.");
          }
          sessionStorage.removeItem("auth-token");
          this.$router.push("/");
        })
        .catch((error) => {
          console.error("Logout failed:", error);
        });
    },
    async fetchUser() {
      try {
        const email = sessionStorage.getItem("email");
        const response = await fetch(
          `http://127.0.0.1:5001/api/user/${email}`,
          {
            method: "GET",
            headers: getHeaders(),
          }
        );
        if (!response.ok) {
          if (response.status === 404) {
            this.errorMessage = "User not found.";
          } else {
            throw new Error("Failed to fetch user.");
          }
        }
        const data = await response.json();
        this.userFlag = data.flag;
      } catch (error) {
        console.error(error);
        this.errorMessage = "Failed to load. Please try again later.";
      }
    },
    fetchSongs() {
      // Ensure that only songs related to the logged-in user are fetched
      // const userId = sessionStorage.getItem("user_id");
      fetch("http://127.0.0.1:5001/api/songs", {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data, this.userId);
          this.songs = data.filter((song) => song.user_id == this.userId);
        })
        .catch((error) => {
          console.error(error);
          this.errorMessage = "Failed to fetch songs. Please try again later.";
        });
    },

    fetchAlbums() {
      fetch("http://127.0.0.1:5001/api/albums", {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data, this.userId);
          this.albums = data.filter((album) => album.user_id == this.userId);
        })
        .catch((error) => {
          console.error(error);
          this.errorMessage = "Failed to fetch albums. Please try again later.";
        });
    },

    deleteSong(songId) {
      fetch(`http://127.0.0.1:5001/api/songs/${songId}`, {
        method: "DELETE",
        headers: getHeaders(),
      })
        .then(() => this.fetchSongs())
        .catch((error) => {
          console.error(error);
          this.errorMessage = "Failed to delete song. Please try again later.";
        });
    },

    deleteAlbum(albumId) {
      fetch(`http://127.0.0.1:5001/api/albums/${albumId}`, {
        method: "DELETE",
        headers: getHeaders(),
      })
        .then(() => this.fetchAlbums())
        .catch((error) => {
          console.error(error);
          this.errorMessage = "Failed to delete album. Please try again later.";
        });
    },

    editSong(songId) {
      this.$router.push({ name: "editsong", params: { id: songId } });
    },

    editAlbum(albumId) {
      this.$router.push({ name: "editalbum", params: { id: albumId } });
    },

    viewSong(id) {
      this.$router.push({ name: "song", params: { id } });
    },
    viewAlbum(id) {
      this.$router.push({ name: "album", params: { id } });
    },

    createSong() {
      const songData = {
        title: this.newSong.title,
        artist: this.newSong.artist,
        lyrics: this.newSong.lyrics,
        genre: this.newSong.genre,
        album_id: this.newSong.album_id || undefined, // Handle cases where no album is selected
        user_id: sessionStorage.getItem("user_id"),
      };

      fetch("http://127.0.0.1:5001/api/songs", {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(songData),
      })
        .then((response) => {
          if (!response.ok) throw new Error("Failed to create song");
          return response.json();
        })
        .then(() => {
          this.fetchSongs(); // Refresh the list of songs
          this.showCreateSongModal = false; // Close the modal
          this.newSong = {
            title: "",
            artist: "",
            lyrics: "",
            genre: "",
            album_id: null,
            user_id: null,
          }; // Reset the form
        })
        .catch((error) => {
          console.error("Create song error:", error);
          this.errorMessage = "Failed to create song. " + error.message;
        });
    },

    createAlbum() {
      const albumData = {
        title: this.newAlbum.title,
        description: this.newAlbum.description,
        user_id: sessionStorage.getItem("user_id"),
      };

      fetch("http://127.0.0.1:5001/api/albums", {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(albumData),
      })
        .then((response) => {
          if (!response.ok) throw new Error("Failed to create album");
          return response.json();
        })
        .then(() => {
          this.fetchAlbums(); // Refresh the list of albums
          this.showCreateAlbumModal = false; // Close the modal
          this.newAlbum = { title: "", description: "" }; // Reset the form
        })
        .catch((error) => {
          console.error("Create album error:", error);
          this.errorMessage = "Failed to create album. " + error.message;
        });
    },

    toggleCreateSongModal() {
      this.showCreateSongModal = !this.showCreateSongModal;
      if (this.showCreateSongModal) {
        this.fetchAlbums(); // Make sure albums are up to date when opening the modal
      }
    },

    toggleCreateAlbumModal() {
      this.showCreateAlbumModal = !this.showCreateAlbumModal;
    },
  },
  mounted() {
    this.fetchUser();
    this.userId = sessionStorage.getItem("user_id");
    this.fetchSongs();
    this.fetchAlbums();
    this.userName = sessionStorage.getItem("user_name");
  },
};
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.header {
  background-color: #e0f2f1; /* A softer shade of green for the header */
  color: white;
  padding: 20px;
  text-align: center;
}

.main-content {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #f0f0f0;
}

.songs-column,
.albums-column {
  flex: 1;
  margin-right: 20px;
  background-color: #e6f2e6; /* Light green background for columns */
  padding: 10px;
  border-radius: 8px;
}

button {
  background-color: #4caf50;
  border: none;
  border-radius: 4px;
  color: white;
  padding: 10px 20px;
  cursor: pointer;
  margin-left: 10px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #66bb6a; /* Slightly darker green on hover */
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 8px 0;
  border-bottom: 1px solid #ddd;
}

.error-message {
  color: #ff0000; /* Red color for errors */
  background-color: #ffdada; /* Light red background */
  padding: 10px;
  margin: 20px;
  border-radius: 5px;
  text-align: center;
}

.modal {
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
