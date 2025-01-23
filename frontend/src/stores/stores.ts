import { writable } from "svelte/store";

export const user: any = writable({}); // Almacenar variables entre paginas del sitio
export const users: any = writable({});