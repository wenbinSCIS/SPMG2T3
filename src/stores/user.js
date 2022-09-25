// global store, alternative to Vuex 4
// assuming we're doing anything user related (to differ Manager, HR, Staff, etc)

import { defineStore, acceptHMRUpdate } from "pinia";
// import { useFetch } from "@vueuse/core"; // alternative to axios (vueuse.org)
import { handleUseFetch } from "../Reusables/common_read";

export const useUserStore = defineStore("user-store", {
  state: () => ({
    /**
     * @type {number | null}
     */
    id: null,
    /**
     * 
     */
    name: "",
    designation: "", // HR, Manager, Staff, etc
  }),
  getters: {
    // checking if user authenticated
    isAuthenticated({ id, name }) {
      return (id == null && name == "");
    },

    // getting all user details
    getDetails({ id, name, designation }) {
      return { id, name, designation };
    },
  },
  actions: {
    async fetchUserDetails() {
      const res = await handleUseFetch("http://localhost:{PORT}/{PATH}");
      if (res == null) return;
      this.id = res.data.id;
      this.name = res.data.name;
      this.designation = res.data.designation;
    },
  },
});


// hot module replacement with pinia
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot));
}