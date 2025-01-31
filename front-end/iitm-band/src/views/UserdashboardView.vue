<template>
  <div id="user-dashboard">
    <header class="dashboard-header">
      <h1>{{ userName }}</h1>
      <span v-if="userFlag" class="emoji-flag">Flagged!!⚠️</span>
      <div class="dashboard-actions">
        <button v-if="userRole === 'creator'" @click="goToCreatorDashboard">
          Creator Dashboard
        </button>
        <button @click="userProfile">User Profile</button>
        <button @click="createPlaylist">Create Playlist</button>
        <label for="search">Search:</label>
        <input
          type="text"
          id="search"
          v-model="searchQuery"
          @input="search"
          placeholder="Search..."
          class="search-input"
        />
        <button @click="logout">Logout</button>
      </div>
    </header>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <main class="content">
      <div class="column">
        <h2>Songs</h2>
        <ul>
          <li v-for="song in filteredSongs" :key="song.id">
            <span v-if="song.flag" class="emoji-flag">⚠️</span>
            {{ song.title }} - {{ song.artist }} - {{ song.genre }}
            <button @click="toggleSongFlag(song)">
              {{ song.flag ? "Unflag" : "Flag" }}
            </button>
            <button @click="viewSong(song.id)">View</button>
          </li>
        </ul>
      </div>
      <div class="column">
        <h2>Albums</h2>
        <ul>
          <li v-for="album in filteredAlbums" :key="album.id">
            {{ album.title }}
            <button @click="viewAlbum(album.id)">View</button>
          </li>
        </ul>
      </div>
      <div class="column">
        <h2>Playlists</h2>
        <ul>
          <li v-for="playlist in playlists" :key="playlist.id">
            {{ playlist.title }}
            <button @click="viewPlaylist(playlist.id)">View</button>
            <button @click="deletePlaylist(playlist.id)">Delete</button>
          </li>
        </ul>
      </div>
    </main>
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
      userName: "", // Placeholder, should be fetched from auth state or API
      userRole: "",
      userFlag: false,
      songs: [],
      albums: [],
      playlists: [],
      searchQuery: "",
      errorMessage: "",
      filteredSongs: [],
      filteredAlbums: [],
    };
  },
  methods: {
    async fetchSongs() {
      try {
        const response = await fetch("http://127.0.0.1:5001/api/songs", {
          method: "GET",
          headers: getHeaders(),
        });
        if (!response.ok) {
          if (response.status === 404) {
            this.errorMessage = "Songs not found.";
          } else {
            throw new Error("Failed to fetch songs.");
          }
        }
        const data = await response.json();
        this.songs = data;
        this.filteredSongs = this.songs;
      } catch (error) {
        console.error(error);
        this.errorMessage = "Failed to load songs. Please try again later.";
      }
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
    async fetchAlbums() {
      try {
        const response = await fetch("http://127.0.0.1:5001/api/albums", {
          method: "GET",
          headers: getHeaders(),
        });
        if (!response.ok) {
          if (response.status === 404) {
            this.errorMessage = "Albums not found.";
          } else {
            throw new Error("Failed to fetch albums.");
          }
        }
        const data = await response.json();
        this.albums = data;
        this.filteredAlbums = this.albums;
      } catch (error) {
        console.error(error);
        this.errorMessage = "Failed to load albums. Please try again later.";
      }
    },
    async fetchPlaylists() {
      try {
        const response = await fetch("http://127.0.0.1:5001/api/playlists", {
          method: "GET",
          headers: getHeaders(),
        });
        if (!response.ok) {
          if (response.status === 404) {
            this.errorMessage = "Playlists not found.";
          } else {
            throw new Error("Failed to fetch playlists.");
          }
        }
        const data = await response.json();
        this.playlists = data;
      } catch (error) {
        console.error(error);
        this.errorMessage = "Failed to load playlists. Please try again later.";
      }
    },
    viewSong(id) {
      this.$router.push({ name: "song", params: { id } });
    },
    async toggleSongFlag(song) {
      await fetch(`http://127.0.0.1:5001/api/flag-song/${song.id}`, {
        method: "PUT",
        headers: getHeaders(),
      });
      this.fetchSongs(); // Refresh the list after toggling
    },
    viewAlbum(id) {
      this.$router.push({ name: "album", params: { id } });
    },
    viewPlaylist(id) {
      this.$router.push({ name: "playlist", params: { id } });
    },
    deletePlaylist(id) {
      fetch(`http://127.0.0.1:5001/api/playlists/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });
      this.fetchPlaylists();
    },
    createPlaylist() {
      this.$router.push({ name: "createplaylist" });
    },
    userProfile() {
      this.$router.push({ name: "userprofile" });
    },
    goToCreatorDashboard() {
      this.$router.push({ name: "creatordashboard" }); // Ensure this route is defined in your router
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
    search() {
      console.log("Searching for:", this.searchQuery);

      // Check if searchQuery is defined and is a string
      const query = this.searchQuery ? this.searchQuery.toLowerCase() : "";

      this.filteredSongs = this.songs.filter((song) => {
        // Ensure song properties are defined and are strings before calling toLowerCase()
        return (
          (song.title && song.title.toLowerCase().includes(query)) ||
          (song.genre && song.genre.toLowerCase().includes(query)) ||
          (song.lyrics && song.lyrics.toLowerCase().includes(query)) ||
          (song.artist && song.artist.toLowerCase().includes(query))
        );
      });

      this.filteredAlbums = this.albums.filter((album) => {
        // Check if album.title is defined and is a string before calling toLowerCase()
        return album.title && album.title.toLowerCase().includes(query);
      });
    },
  },
  mounted() {
    this.fetchSongs();
    this.fetchUser();
    this.fetchAlbums();
    this.fetchPlaylists();
    this.userName = sessionStorage.getItem("user_name");
    this.userRole = sessionStorage.getItem("user_role");
  },
};
</script>

<style scoped>
#user-dashboard {
  font-family: "Arial", sans-serif;
}

.dashboard-header {
  background-color: #e0f2f1;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-header h1 {
  margin: 0;
  color: #00695c;
}

.dashboard-actions button,
.search-input {
  margin-left: 10px;
}

button {
  background-color: #4caf50;
  border: none;
  border-radius: 4px;
  color: white;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #66bb6a;
}

.content {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.column {
  flex: 1;
  margin-right: 20px;
}

.column:last-child {
  margin-right: 0;
}

.column h2 {
  color: #2e7d32;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 15%;
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
