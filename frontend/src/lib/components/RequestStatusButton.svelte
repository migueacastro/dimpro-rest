<script lang="ts">
	import type { ToastSettings, ModalSettings } from '@skeletonlabs/skeleton';
	import { getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	export let request: any;
	import { enhance } from '$app/forms';

	let modalStore = getModalStore();
	let toastStore = getToastStore();
	let body: any = {};
	export let saved: boolean = true;

	function handleSubmit() {
		return async ({ update, result }: any) => {
			if (result?.type == 'success') {
				request.status = request?.status == 'pendiente' ? 'aprobado' : 'pendiente';
				const toast: ToastSettings = {
					message: 'Estatus cambiado con exito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
				toastStore.trigger(toast);
			} else {
				const toast: ToastSettings = {
					message: `¡ERROR! El estatus no se pudo cambiar. `+result.data?.error?.message,
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
		if (!saved) {
				toastStore.trigger({
					message: 'Por favor, guarde los cambios antes de aprobar.',
					background: 'variant-ghost-info',
					timeout: 1500
				});
				return;
			} 
		const form = (event.target as HTMLElement).closest('form') as HTMLFormElement;

		const modal: ModalSettings = {
			type: 'confirm',
			title: `Aprobar solicitud`,
			body: `¿Confirma aprobar la solicitud?`,
			response: async (r: boolean) => {
				if (r && form) {
					form.requestSubmit(); // Programmatically submit the form
				}
			}
		};
		modalStore.trigger(modal);
	}
</script>
<form action="?/approve" method="post" use:enhance={handleSubmit} class="capitalize btn max-w-fit px-[2rem] h-fit p-4 my-4 ml-2" class:variant-filled={request?.status === 'pendiente' && saved}
		class:variant-filled-primary={request?.status === 'aprobado' && saved}
		class:variant-glass-primary={!saved}>
	<input type="hidden" name="requestId" value={request?.id} />
	<button
		type="button"
		on:click={handleClick}
		disabled={request?.status === 'aprobado'}
		
	>
		{request?.status == 'pendiente' ? 'Aprobar' : 'Aprobado'}
	</button>
</form>
