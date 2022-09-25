// global store, alternative to Vuex 4

import { defineStore, acceptHMRUpdate } from "pinia";
import { handleUseFetchGet } from "../Reusables/common_read"; // check this for the useFetch

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
  getters: {
    getRoleNames({ roles }) {
      return roles.map(({ RoleName }) => RoleName); // returning a new array of only the RoleName
    },
  },
  actions: {
    // attempt at abstracted option for the above
    async fetchRoles() {
      const res = await handleUseFetchGet("http://localhost:5000/roles");
      if (res == null) return;
      this.roles = res.data;
    },
  },
});


// hot module replacement with pinia
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMainStore, import.meta.hot));
}