import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("@/views/AboutView.vue"),
    },
    {
      path: "/roles",
      name: "AvailableRoles",
      component: () => import("@/views/AvailableRoles.vue"),
    },
    {
      path: "/viewcoursebyskill/:nameid", // dynamic routing based on name-id mapping
      name: "ViewCourseBySkill",
      component: () => import("@/views/ViewCourseBySkill.vue"),
      props: true, // allowing route parameter to be passed as props
    },
  ],
});

export default router;
