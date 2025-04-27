import { fetchData } from "$lib/utils";

export async function fetchReminders() {
    let response = await fetchData("notes", 'GET');
    let result = await response.json();
    return result;
}