import axios from "@/services/axios.js";

/**
 * Generalized function to fetch lists from a given API path.
 * @param {string} apiPath - The API endpoint to fetch data from.
 * @returns {Promise<Array>} - Returns the data array from the response.
 * @throws {Error} - Throws an error if the request fails.
 */
export async function fetchList(apiPath) {
  try {
    const response = await axios.get(apiPath);
    return response.data;
  } catch (error) {
    console.error(`Error fetching data from ${apiPath}:`, error);
    throw error;
  }
}
