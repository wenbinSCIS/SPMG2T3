// for error handling common resusable functions

import { useFetch } from "@vueuse/core";

/**
 * Takes in URL of microservice
 * Returns Promise of parsed response data or null if no response received
 */
export const handleUseFetch = async (url) => {
  const { data, error, statusCode } = await useFetch(url);
  if (error.value) {
    console.log("err:", error.value);
    console.log("statusCode:", statusCode.value);
    return null; // break out of function if error returned
  } 

  // if no error, return parsed data (from stringified JSON to javascript object)
  return JSON.parse(data.value);
}