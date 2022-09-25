<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
// import { useMainStore } from "@/stores/main"
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { handleUseFetchPost } from "@/Reusables/common_read";

// const store = useMainStore();
// console.log(store.getRoleNames);
const router = useRouter();

// setting up variables for v-model
const role_name = ref("");
const created_by = ref("");
const description = ref("");

// using vuelidate for the form validations
const validation_rules = computed(() => ({
  role_name: { required },
  created_by: { required },
  description: { required },
}));
// for validation on submission
const v$ = useVuelidate(validation_rules, { role_name, created_by, description });

// submit function
async function handleSubmit() {
  // when click, validate form inputs
  v$.value.$validate();

  // break out of function given that there are invalid properties
  if (v$.value.$error) {
    alert("Invalid properties"); // alert because lazy to do actual nice thing
    return;
  }

  // run the post method if no error
  const res = await handleUseFetchPost("http://localhost:5000/roles/create", {
    "Role Name": role_name.value,
    "Created By": created_by.value,
    "Description": description.value,
  });
  if (res == null) return; // if there is an error, will console log
  // for errors like: item exists in db already (based on RoleID for example)
  if (res.code === 500) {
    alert(res.message); // error message -- will change it later probably, maybe not idk
    return;
  }

  // return to "/roles" given all is good
  router.push({ name: "AvailableRoles" });
}


</script>

<template>
  <main>
    <div class="input-group mt-3">
      <span class="input-group-text">Role Name</span>
      <input type="text" class="form-control" placeholder="Enter role name..." v-model="role_name" />
    </div>

    <br>

    <div class="input-group mt-3">
      <span class="input-group-text">Created By</span>
      <input type="text" class="form-control" placeholder="Enter creator name..." v-model="created_by" />
    </div>

    <br>

    <div class="input-group mt-3">
      <span class="input-group-text">Description</span>
      <input type="text" class="form-control" placeholder="Enter role description..." v-model="description" />
    </div>

    <br>

    <div class="container mt-3 d-flex justify-content-center">
      <button @click="handleSubmit" class="btn btn-primary px-5">Save</button>
    </div>
  </main>
</template>

<style scoped></style>