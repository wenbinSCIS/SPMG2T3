// global store, alternative to Vuex 4

import { ref } from "vue";
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
     *  SkillsID: Number,
     *  Skillname: String,
     */
    skills: [],
  }),
  getters: {
    getRoleNames({ roles }) {
      return roles.map(({ RoleName }) => RoleName); // returning a new array of only the RoleName
    },
    getSkillNames({ skills }) {
      return skills.map(({ Skillname }) => Skillname); // return new array of only Skillname
    },
  },
  actions: {
    async fetchRoles() {
      const res = await handleUseFetchGet("http://localhost:5000/roles");
      if (res == null) return ref(0);
      this.roles = res.data;
      return ref(1);
    },
    async fetchSkills() {
      const res = await handleUseFetchGet("http://localhost:5002/getAllSkill");
      if (res == null) return ref(0);
      this.skills = res.data;
      return ref(1);
    },
  },
});


// hot module replacement with pinia
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMainStore, import.meta.hot));
}