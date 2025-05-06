<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';

	const fields = new FormErrors();

	interface FormErrors {
		oldPassword: any;
	}

	let errors: FormErrors = {
		oldPassword: []
	};

	let oldPassword = '';
	function togglePasswordInput(event: Event) {
		let button = event.target as HTMLElement;
		if (button.tagName !== 'BUTTON') {
			// just in case the event.target is the icon and not the button
			button = button.closest('button') as HTMLElement;
		}
		const input = button.closest('.input-group')?.querySelector('input') as HTMLInputElement;
		input.type = input.type === 'password' ? 'text' : 'password';
		const icon = button.querySelector('i') as HTMLElement;
		icon.classList.toggle('fa-eye');
		icon.classList.toggle('fa-eye-slash');
	}

	async function handleEnhance() {
		return ({ result }: any) => {
			if (result?.data?.success) {
				return goto('/dashboard/user/change-password');
			} else {
				errors.oldPassword = ['La contraseña actual es incorrecta. Por favor, inténtelo de nuevo.'];
			}
		};
	}
</script>

<div class=" mx-auto flex flex-col lg:w-1/2 w-full">
	<p class="h2 mb-5">Introduzca su contraseña actual</p>
	<form action="?/verifypassword" method="post" use:enhance={handleEnhance}>
		<div class="input-group mb-2 input-group-divider grid-cols-[1fr_auto] p-0">
			<input
				class="input"
				title="Contraseña"
				type="password"
				id="old_password"
				name="old_password"
				placeholder="Contraseña"
				bind:value={oldPassword}
			/>
			<button type="button" on:click={togglePasswordInput}
				><i class="fa-regular fa-eye-slash"></i></button
			>
		</div>
		{#if errors?.oldPassword?.length > 0}
			<div class="card mb-2 variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.oldPassword as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		<button type="submit" class="btn btn-xl variant-filled-primary my-2 w-fit shadow-xl">
			Guardar
		</button>
	</form>
</div>
