<script lang="ts">
	import type { ToastSettings, ModalSettings } from '@skeletonlabs/skeleton';
	import { getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	export let order: any;
	import { enhance } from '$app/forms';

	let modalStore = getModalStore();
	let toastStore = getToastStore();
	let body: any = {};

	function handleSubmit() {
		return async ({ update, result }: any) => {
			if (result?.type == 'success') {
				order.status = order?.status == 'pendiente' ? 'preparado' : 'pendiente';
				const toast: ToastSettings = {
					message: 'Estatus cambiado con exito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
				toastStore.trigger(toast);
			} else if (result?.type == 'failure') {
				const toast: ToastSettings = {
					message: `¡ERROR! El estatus del pedido no se pudo cambiar.`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
			await update({ reset: false });
		};
	}

	function handleClick(event: Event) {
		// Find the form element
		const form = (event.target as HTMLElement).closest('form') as HTMLFormElement;

		const modal: ModalSettings = {
			type: 'confirm',
			title: `Cambiar estatus`,
			body: `¿Confirma cambiar el estatus del pedido?`,
			response: async (r: boolean) => {
				if (r && form) {
					form.requestSubmit(); // Programmatically submit the form
				}
			}
		};
		modalStore.trigger(modal);
	}
</script>

<form action="?/changestatus" method="post" use:enhance={handleSubmit}>
	<input type="hidden" name="orderId" value={order?.id} />
	<input type="hidden" name="orderStatus" value={order?.status} />
	<button
		type="button"
		on:click={handleClick}
		class="capitalize btn max-w-fit px-[2rem]"
		class:variant-filled={order?.status === 'pendiente'}
		class:variant-filled-primary={order?.status === 'preparado'}
	>
		{order?.status}
	</button>
</form>
