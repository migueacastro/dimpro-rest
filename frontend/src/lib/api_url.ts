export const mode = import.meta.env.VITE_MODE
export let apiURL = "";
if (mode == "production") {
    apiURL = import.meta.env.VITE_API_URL;
} else {
    apiURL = "http://api:8000/api/";
}