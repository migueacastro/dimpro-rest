<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { getToastStore, ProgressRadial, type ToastSettings } from '@skeletonlabs/skeleton';
	$: loading = false;
	$: success = false;
	let email = '';
	let error = '';
	const toastStore = getToastStore();

	function triggerSuccessToast() {
		let toast: ToastSettings = {
			message: 'Correo enviado exitosamente',
			background: 'variant-ghost-success',
			timeout: 3500
		};
		toastStore.trigger(toast);
	}
	function triggerErrorToast() {
		let toast: ToastSettings = {
			message: '¡ERROR! No se pudo enviar el correo.',
			background: 'variant-ghost-error',
			timeout: 3500
		};
		toastStore.trigger(toast);
	}

	function handleEnhance() {
		loading = true;

		return async ({ update, result }: any) => {
			if (result.type === 'success') {
				triggerSuccessToast();
				success = true;
			} else {
				triggerErrorToast();
				error = 'Error al enviar el correo. ';
			}
			loading = false;
			return update({ reset: false });
		};
	}
</script>

<title>Reestablecer contraseña</title>

{#if !loading}
	<div class="flex flex-col">
		<ol class="breadcrumb mb-[3rem]">
			<li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
			<li class="crumb-separator" aria-hidden>/</li>
			<li class="crumb">Reestablecer Contraseña</li>
		</ol>
		{#if !success}
			{#if error !== ""}
			<div class="card variant-ghost-error p-2 text-sm text-left mb-2">
				{error}
			</div>
			{/if}
			<form action="?/send" method="post" use:enhance={handleEnhance}>
				<h3 class="text-4xl mb-[2rem]">Reestablecer Contraseña</h3>
				<input
					id="email"
					name="email"
					class="input my-2"
					title="Email"
					type="text"
					placeholder="Email"
					bind:value={email}
				/>

				<button class="btn btn-xl variant-filled-primary my-2 w-full shadow-xl" type="submit"
					>Enviar Correo</button
				>
			</form>
		{:else}
			<div class="flex justify-center mt-[8rem] flex-col">
				<div class="my-auto">
					<h2 class="h2 text-center mb-8">Enlace enviado a tu correo</h2>
				</div>
				<button
					type="button"
					class="btn btn-xl variant-filled-primary my-2 w-fit shadow-xl mx-auto"
					on:click={() => goto('/start')}>Volver a inicio</button
				>
			</div>
		{/if}
	</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}
