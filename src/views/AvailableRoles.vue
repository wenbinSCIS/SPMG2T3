<script setup>
import { ref, computed } from "vue";
import { useMainStore } from "@/stores/main";
import RoleCard from "@/components/RoleCard.vue";

const searchQuery = ref("");
const store = useMainStore();
store.fetchRoles2(); // fetching roles, through roles.py

// case sensitive role name filter
const roleList = computed(() => {
  if (searchQuery.value === "") return store.roles;
  else return store.roles.filter(({ RoleName }) => RoleName.toLowerCase().includes(searchQuery.value.toLowerCase()));
});
</script>

<template>
  <main>
    <div class="input-group">
      <span class="input-group-text">Search:</span>
      <input type="text" class="form-control" placeholder="Search role..." v-model="searchQuery" />
    </div>

    <!-- section placeholder for if the roleList is empty -->
    <section class="container msg" v-if="store.roles.length === 0">
      Loading...
    </section>
    <section class="container msg" v-else-if="roleList.length === 0">
      Zero results found
    </section>
    <!-- section main -->
    <section class="container" id="roleList" v-else>
      <!-- destructuring values from the roleList -->
      <div v-for="{ RoleID, RoleName, Description, Fulfilled } in roleList" :key="RoleID">
        <RoleCard
          :role-id="RoleID"
          :role-name="RoleName"
          :description="Description"
          :fulfilled="Fulfilled"
        />
      </div>
    </section>
  </main>
</template>

<style scoped>
section.msg {
  margin-top: 1rem;
}
</style>