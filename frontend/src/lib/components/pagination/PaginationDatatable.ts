import { apiURL } from '$lib/api_url';
import type { Actions } from '@sveltejs/kit';

export async function handleDelete({ fetch }: any, endpoint: any) {
	const response = await fetch(apiURL + endpoint, {
		method: 'DELETE'
	});
	if (response.ok) {
		return { success: true }; // this is the result, you can also pass data inside it
	} else {
		return { success: false };
	}
}

export const actions: Actions = {
	pagination: async () => {},
	rowsperpage: async () => {},
	search: async () => {},
	thfilter: async () => {},
	thsort: async () => {}
};

export class CustomDataHandler {
	results: any;
	rowCount: any;
	pages: any;
  search: string;
  ordering: string;
	not_system: boolean;

	removeDomainFromURL(urlStr: string) {
		try {
			const urlObj = new URL(urlStr);
			return urlObj.pathname.slice(1);
		} catch (error) {
			return urlStr;
		}
	}

	getPages(current: number, total: number) {
		let start = current - 4; // try to center current page in array
		let end = current + 5;
		if (total < 1) return [];
		if (start < 1) {
			start = 1;
			end = Math.min(10, total);
		}
		if (end > total) {
			end = total;
			start = Math.max(1, total - 9);
		}
		const pages: number[] = [];
		for (let i = start; i <= end; i++) {
			pages.push(i);
		}
		if (!pages.includes(total)) {
			pages.push(total);
		}
    if (!pages.includes(1)) {
      pages.unshift(1);
    }
		return pages;
	}

	serialize() {
		return {
			results: this.results,
			rowCount: this.rowCount,
			pages: this.pages,
      search: this.search,
      ordering: this.ordering,
			not_system: this.not_system,
		};
	}

	constructor({ query, url }: any) {
		this.results = query.results;
    this.ordering = url.searchParams.get('ordering') ?? "";
		this.pages = {
      sizes: [5,10,20,50,100],
			current: url.searchParams.get('page') ?? '1'
		};
    this.pages.size = Number(url.searchParams.get('page_size')) || this.pages.sizes[1];
		this.rowCount = {
			start: (parseInt(this.pages.current) - 1) * parseInt(this.pages.size) + 1,
			total: query.count
		};
		this.pages.count = Math.ceil(parseInt(this.rowCount.total) / parseInt(this.pages.size));
		this.pages.list = this.getPages(parseInt(this.pages.current), this.pages.count);
		this.rowCount.end = Math.min(
			this.rowCount.total,
			this.rowCount.start + this.results.length - 1
		);
    this.search = url.searchParams.get('search') || "";
		this.not_system = url.searchParams.get('not_system') ?? false;
	}
}
