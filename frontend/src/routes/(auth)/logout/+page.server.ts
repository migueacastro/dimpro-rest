import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export async function load({ cookies }: any) {
  cookies.delete('sessionid', { path: '/' });
  // additional logout logic if needed
  throw redirect(303, '/start');
}