<!-- incomplete page for displaying recommended courses by the skills -->

<script setup>
// the route parameter, taken in as a prop (check "/viewcoursebyskill" in the index.js file in router folder)
const props = defineProps({
  nameid: String,
});

// for example: /viewcoursebyskill/skillname-skillid
const [name, id] = props.nameid.split("-");
</script>

<template>
  <div>
    <span>SkillsID: {{ id }}</span>
    <br>
    <span>Skillname: {{ name }}</span>
  </div>
</template>

<style scoped></style>