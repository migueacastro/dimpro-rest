<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();
	

	let password = '';
	let confirmPassword = '';
	const error = new FormErrors();

	function validatePassword() {
		if (password.length < 8) {
			passwordError = true;
		} else if (!error.hasNumbers(password)) {
			passwordError = true;
		} else if (!error.hasUpperCase(password)) {
			passwordError = true;
		} else if (password != confirmPassword) {
			passwordError = true;
		} else {
			passwordError = null;
		}
	}

	let passwordError: any = true;

	async function handleEnhance() {
		return ({ update, result }: any) => {
			let toast: ToastSettings = {
				message: 'Contraseña actualizada con exito.',
				background: 'variant-ghost-success',
				timeout: 7000
			};
			if (result?.type === 'success') {
				toastStore.trigger(toast);
				return goto('/dashboard/user');
			} else {
				toast = {
					message: `¡ERROR! No se pudo actualizar la contraseña.`,
					background: 'variant-ghost-error',
					timeout: 7000
				};
				toastStore.trigger(toast);
			}
			return update({ reset: false });
		};
	}

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
</script>

<title>Cambiar contraseña</title>

<div class=" mx-auto flex flex-col lg:w-1/2 w-full">
	<form method="post" action="?/changepassword" use:enhance={handleEnhance}>
		<h3 class="text-4xl mb-[2rem]">Cambiar contraseña</h3>

		<div class="input-group mb-2 input-group-divider grid-cols-[1fr_auto] p-0">
			<input
				class="input"
				title="Contraseña"
				type="password"
				autocomplete="off"
				id="password"
				name="password"
				placeholder="Nueva Contraseña"
				bind:value={password}
				on:input={validatePassword}
			/>
			<button type="button" on:click={togglePasswordInput}
				><i class="fa-regular fa-eye-slash"></i></button
			>
		</div>
		<div
			class="mt-3 card p-4 text-left text-sm"
			class:variant-ghost-success={!passwordError}
			class:variant-ghost-error={passwordError}
		>
			<ul>
				<li>
					Tiene 8 caractéres o más {#if password.toString()?.length >= 8}
						<i class="fa-solid fa-check"></i>{:else}
						<i class="fa-solid fa-xmark"></i>{/if}
				</li>
				<li>
					Tiene números {#if error?.hasNumbers(password?.toString())}
						<i class="fa-solid fa-check"></i>{:else}
						<i class="fa-solid fa-xmark"></i>{/if}
				</li>
				<li>
					Tiene mayúsculas {#if error?.hasUpperCase(password?.toString())}
						<i class="fa-solid fa-check"></i>{:else}
						<i class="fa-solid fa-xmark"></i>{/if}
				</li>
				<li>
					Las contraseñas coinciden {#if password === confirmPassword && password?.toString().length > 0}
						<i class="fa-solid fa-check"></i>{:else}
						<i class="fa-solid fa-xmark"></i>{/if}
				</li>
			</ul>
		</div>

		<div class="input-group input-group-divider grid-cols-[1fr_auto] my-2">
			<input
				class="input"
				autocomplete="off"
				title="Confirmar Contraseña"
				type="password"
				id="confirm_password"
				name="confirm_password"
				placeholder="Confirmar Contraseña"
				bind:value={confirmPassword}
				on:input={validatePassword}
			/>
			<button type="button" on:click={togglePasswordInput}
				><i class="fa-regular fa-eye-slash"></i></button
			>
		</div>


		<button
			type="submit"
			class="btn btn-xl variant-filled-primary my-2 w-fit shadow-xl"
			disabled={passwordError}>Guardar</button
		>
	</form>
</div>
