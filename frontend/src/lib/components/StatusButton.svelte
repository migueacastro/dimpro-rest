<script lang="ts">
	import { fetchData } from '$lib/utils';
	import type { ToastSettings, ModalSettings } from '@skeletonlabs/skeleton';
	import { getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	export let order: any;
	let modalStore = getModalStore();
	let toastStore = getToastStore();
	let body: any = {};
	async function saveStatus() {
		if (order?.status === 'preparado') {
			body = {
				status: 'pendiente'
			};
		} else {
			body = {
				status: 'preparado'
			};
		}

		let response = await fetchData('orders', 'PATCH', body, order?.id);
		if (response.ok) {
			order.status = body.status;
			const toast: ToastSettings = {
				message: 'Estatus cambiado con exito.',
				background: 'variant-ghost-success',
				timeout: 7000
			};
			toastStore.trigger(toast);
		} else {
			const toast: ToastSettings = {
				message: `¡ERROR! El estatus del pedido no se pudo cambiar.`,
				background: 'variant-ghost-error',
				timeout: 7000
			};
			toastStore.trigger(toast);
		}
	}
	async function handleClick() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Cambiar estatus`,
			body: `¿Confirma cambiar el estatus del pedido?`,
			response: async (r: boolean) => {
				if (r) {
					await saveStatus();
				}
			}
		};
		modalStore.trigger(modal);
	}
</script>

<button
	class="capitalize btn max-w-fit px-[2rem]"
	on:click={handleClick}
	class:variant-filled={order?.status === 'pendiente'}
	class:variant-filled-primary={order?.status === 'preparado'}
>
	{order?.status}
</button>
