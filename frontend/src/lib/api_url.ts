export const mode = import.meta.env
export let apiURL = "";
if (mode.toString() === "production") {
    apiURL = import.meta.env.VITE_API_URL;
} else {
    apiURL = "http://localhost:8000/api/";
}