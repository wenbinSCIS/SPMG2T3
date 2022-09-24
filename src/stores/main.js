// global store, alternative to Vuex 4

import { defineStore, acceptHMRUpdate } from "pinia";
import { useFetch } from "@vueuse/core"; // alternative to axios (vueuse.org)
import { handleUseFetch } from "../Reusables/common_read";

export const useMainStore = defineStore("main-store", {
  state: () => ({
    /**
     * Array<role>
     * role:
     *  CreatedBy: String,
     *  Description: String,
     *  Fulfilled: String,
     *  RoleID: Number,
     *  RoleName: String,
     */
    roles: [],
    /**
     * Array<skill>
     * skill:
     *  RoleID: Number,
     *  SRBR: Number,
     *  SkillsID: Number,
     */
    requiredSkills: [],
  }),
  getters: {},
  actions: {
    // random redundancy (will remove later)
    async fetchRoles() {
      const { data, error, statusCode } = await useFetch("http://localhost:5000/roles");
      if (error.value) {
        console.log("err:", error.value);
        console.log("statusCode:", statusCode.value);
        return; // break out of function if error returned
      }
      // parsing stringified JSON to javascript object
      this.roles = JSON.parse(data.value).data;
    },

    // attempt at abstracted option for the above
    async fetchRoles2() {
      const res = await handleUseFetch("http://localhost:5000/roles");
      if (res == null) return;
      this.roles = res.data;
    },
  },
});


// hot module replacement with pinia
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMainStore, import.meta.hot));
}