// for fetching stuff (reusable functions)

import { useFetch } from "@vueuse/core"; // alternative to axios (vueuse.org)

/**
 * Takes in URL of microservice
 * Returns Promise of parsed response data or null if no response received
 */
export const handleUseFetchGet = async (url) => {
  const { data, error, statusCode } = await useFetch(url).json().get();
  if (error.value) {
    console.log("err:", error.value);
    console.log("statusCode:", statusCode.value);
    return null;
  }
  // returns { data }
  return data.value;
}

/**
 * Takes in URL of microservice
 * Takes in Object containing json body data
 * Returns Promise of confirmation data or microservice error message, or null if no response received
 */
export const handleUseFetchPost = async (url, postData) => {
  const { data, error, statusCode } = await useFetch(url).json().post(postData);
  if (error.value) {
    console.log("err:", error.value);
    console.log("statusCode:", statusCode.value);
    return null;
  }
  // returns { code, ... } <-- could be message, or confirmation
  return data.value;
}