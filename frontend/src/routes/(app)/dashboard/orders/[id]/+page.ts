import { fetchData } from "$lib/utils";
import Cookies from "js-cookie";

export async function load({ params }) {
  return {
    id: params.id,
  };
}
