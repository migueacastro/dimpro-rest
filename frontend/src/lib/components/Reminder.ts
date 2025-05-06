import { apiURL } from "$lib/api_url";

export async function fetchReminders({fetch}: any) {
    let response = await fetch(apiURL+"notes");
    let result = await response.json();
    return result;
}