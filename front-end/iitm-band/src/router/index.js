import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import UserdashboardView from "../views/UserdashboardView.vue";
import AdminloginView from "../views/AdminloginView.vue";
import AdmindashboardView from "../views/AdmindashboardView.vue";
import CreatorloginView from "../views/CreatorloginView.vue";
import CreatordashboardView from "../views/CreatordashboardView.vue";
import UnauthorisedadminView from "../views/UnauthorisedadminView.vue";
import RegistrationView from "../views/RegistrationView.vue";
import SongView from "../views/SongView.vue";
import AlbumView from "../views/AlbumView.vue";
import PlaylistView from "../views/PlaylistView.vue";
import CreateplaylistView from "../views/CreateplaylistView.vue";
import UserprofileView from "../views/UserprofileView.vue";
import EditsongView from "../views/EditsongView.vue";
import EditalbumView from "../views/EditalbumView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/registration",
    name: "registration",
    component: RegistrationView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/userdashboard",
    name: "userdashboard",
    component: UserdashboardView,
  },
  {
    path: "/userprofile",
    name: "userprofile",
    component: UserprofileView,
  },
  {
    path: "/song/:id?",
    name: "song",
    component: SongView,
  },
  {
    path: "/album/:id?",
    name: "album",
    component: AlbumView,
  },
  {
    path: "/editsong/:id?",
    name: "editsong",
    component: EditsongView,
  },
  {
    path: "/editalbum/:id?",
    name: "editalbum",
    component: EditalbumView,
  },
  {
    path: "/playlist/:id",
    name: "playlist",
    component: PlaylistView,
  },
  {
    path: "/createplaylist",
    name: "createplaylist",
    component: CreateplaylistView,
  },
  {
    path: "/creatorlogin",
    name: "creatorlogin",
    component: CreatorloginView,
  },
  {
    path: "/creatordashboard",
    name: "creatordashboard",
    component: CreatordashboardView,
  },
  {
    path: "/adminlogin",
    name: "adminlogin",
    component: AdminloginView,
  },
  {
    path: "/unauthorisedadmin",
    name: "unauthorisedadmin",
    component: UnauthorisedadminView,
  },
  {
    path: "/admindashboard",
    name: "admindashboard",
    component: AdmindashboardView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
