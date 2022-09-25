import { createRouter, createWebHistory } from "vue-router";
// import { useUserStore } from "@/stores/user";
import HomeView from "@/views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        requiresAuth: false,
      },
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("@/views/AboutView.vue"),
      meta: {
        requiresAuth: false,
      },
    },
    {
      path: "/roles",
      name: "AvailableRoles",
      component: () => import("@/views/AvailableRoles.vue"),
      meta: {
        requiresAuth: false,
      },
    },
    {
      path: "/roles/create",
      name: "CreateNewRole",
      component: () => import("@/views/CreateNewRole.vue"),
      meta: {
        requiresAuth: false,
      },
    },
    {
      path: "/viewcoursebyskill/:nameid", // dynamic routing based on name-id mapping
      name: "ViewCourseBySkill",
      component: () => import("@/views/ViewCourseBySkill.vue"),
      meta: {
        requiresAuth: false,
      },
      props: true, // allowing route parameter to be passed as props
    },
  ],
});


// not sure if this works actually, disregard for now
// router.beforeEach((to, from, next) => {
//   const store = useUserStore();

//   // if doesn't require auth, then return
//   if (!to.meta.requiresAuth)
//     next();

//   // if does, then check for authentication
//   else if (store.isAuthenticated)
//     next();

//   // if not authenticated
//   else if (to.path !== "/login")
//     next({ name: "Login" });

//   return;
// });


export default router;
