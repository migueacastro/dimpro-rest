<script lang="ts">
	import { goto } from '$app/navigation';
	import { apiURL } from '$lib/api_url';
	import { authenticate, fetchStaff } from '$lib/auth';
	import Cookies from 'js-cookie';

	interface FormErrors {
		email: any;
		password: any;
	}
	let errors: FormErrors = { email: null, password: null };

	let email = '';
	let password = '';

	async function handleStaff() {
		let formData = {
			email: email,
			password: password
		};
		const response = await fetchStaff(formData);
		const data = await response.json();
		if (response.ok) {
			const token = data?.token;
			Cookies.set('token', token, { expires: 365, secure: true });
			await authenticate();
			goto('/');
		} else {
			errors = data;
		}
	}
	let showPassword = false;
	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}
	let inputType = 'password';
	$: inputType = showPassword ? 'text' : 'password';
</script>

<title>Inicio Sesión</title>

<div class="flex flex-col">
	<ol class="breadcrumb mb-[3rem]">
		<li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
		<li class="crumb-separator" aria-hidden>/</li>
		<li class="crumb">Empleado</li>
	</ol>

	<form>
		<h3 class="text-4xl mb-[2rem]">Iniciar Sesión</h3>
		<input class="input my-2" title="Email" type="text" placeholder="Email" bind:value={email} />

		{#if errors.email}
			<div class="card variant-ghost-error p-2 text-sm text-left">
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
					bind:value={password}
				/>
				<button type="button" on:click={togglePasswordVisibility}
					><i class="fa-regular fa-eye"></i></button
				>
			{/if}
		</div>

		{#if errors.password}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.password as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		<button class="btn btn-xl variant-filled-tertiary my-2 w-full shadow-xl" on:click={handleStaff}
			>Iniciar Sesión</button
		>
	</form>
</div>
