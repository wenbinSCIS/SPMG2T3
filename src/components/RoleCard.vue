<!-- Individual card components for the Role lists -->

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import { handleUseFetchGet } from "@/Reusables/common_read";

// props 
defineProps({
  roleId: Number,
  roleName: String,
  description: String,
  fulfilled: String,
});

const skills = ref([]); // list of skills for each card component (to list down)

/**
 * Takes in current card's role ID
 * Fetches current linked skills (related to current role)
 * Loops through linked skills list and fetches the names of the skills
 * Pushes objects of skill id and skill name into skills list for each card component
 */
async function fetchRequiredSkills(roleID) {
  const res = await handleUseFetchGet(`http://localhost:5001/getSRBRbyRoleID?RoleID=${roleID}`);
  if (res == null) return;

  // for each of the linked Skills... (also using destructuring to get only the SkillsID)
  res.data.forEach(async ({ SkillsID }) => {
    const res2 = await handleUseFetchGet(`http://localhost:5002/getSkillbyId?skillid=${SkillsID}`);
    if (res2 == null) return;
    skills.value.push({ SkillsID, Skillname: res2.data[0].Skillname }); // pushing data into the skills list
  });
}
</script>

<template>
  <div class="card" style="width: 20rem;">
    <img class="card-img-top" src="#" alt="Card image cap">
    <div class="card-body">
      <h5 class="card-title">{{ roleName }}</h5>
      <p class="card-text" :id="'text-' + roleId">{{ description }}</p>
      <p class="card-text">{{ fulfilled.trim() === "" ? "Unfulfilled" : "Fulfilled" }}</p>
    </div>
    <div class="card-footer">
      <button @click="fetchRequiredSkills(roleId)">View Skills</button>
      <ul class="" v-if="skills.length !== 0">
        <strong>Skills Required</strong>
        <li v-for="{ SkillsID, Skillname } in skills" :key="SkillsID">
          <RouterLink :to="{
            name: 'ViewCourseBySkill',
            params: { nameid: `${Skillname}-${SkillsID}` }
          }">{{ Skillname }}</RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
/* scoped card styling (wen bin's) */
.card {
  display: inline-block;
  margin-left: 20px;
  margin-right: 20px;
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
