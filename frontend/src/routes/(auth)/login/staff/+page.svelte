<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	$: loaded = true
	interface FormErrors {
		email: any;
		password: any;
	}
	let errors: FormErrors = { email: [], password: [] };

	let email = '';
	let password = '';

	let showPassword = false;
	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}
	let inputType = 'password';
	$: inputType = showPassword ? 'text' : 'password';

	function handleEnhance() {
		// outside the return update
		loaded = false;
		return ({ update, result }: any) => {
			if (result.type == 'success') {
				goto("/dashboard/");
			} else  {
				// after the result
				loaded = true;
				console.error('Error al iniciar sesión:', result.data);
				errors.email = ['El correo electrónico o la contraseña son incorrectos.'];
				return update({ reset: false }); // this line will apply the changes
			}
		};
	}
</script>

<title>Inicio Sesión</title>
{#if loaded}
<div class="flex flex-col">
	<ol class="breadcrumb mb-[3rem]">
		<li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
		<li class="crumb-separator" aria-hidden>/</li>
		<li class="crumb">Empleado</li>
	</ol>

	<form action="?/login" method="post" use:enhance={handleEnhance}>
		<h3 class="text-4xl mb-[2rem]">Iniciar Sesión</h3>
		<input
			id="email"
			name="email"
			class="input my-2"
			title="Email"
			type="text"
			placeholder="Email"
		/>

		{#if errors.email.length > 0}
			<div class="card variant-ghost-error p-2 text-sm text-left mb-2">
				<ul>
					{#each errors?.email as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		<div class="input-group input-group-divider grid-cols-[1fr_auto] p-0">
			{#if showPassword}
				<input
					class="input"
					title="Contraseña"
					type="text"
					id="password"
					name="password"
					placeholder="Contraseña"
					bind:value={password}
				/>
				<button type="button" on:click={togglePasswordVisibility}
					><i class="fa-regular fa-eye-slash"></i></button
				>
			{:else}
				<input
					class="input"
					title="Contraseña"
					type="password"
					placeholder="Contraseña"
					id="password"
					name="password"
					bind:value={password}
				/>
				<button type="button" on:click={togglePasswordVisibility}
					><i class="fa-regular fa-eye"></i></button
				>
			{/if}
		</div>

		{#if errors.password.length > 0}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.password as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		<p class="text-start mt-4">
			<a class="anchor no-underline" href="/password-reset">¿Olvidaste tu contraseña? </a>
		</p>
		<button class="btn btn-xl variant-filled-tertiary my-2 w-full shadow-xl" type="submit"
			>Iniciar Sesión</button
		>
	</form>
</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}