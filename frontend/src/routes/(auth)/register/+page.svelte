<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchRegister, fetchLogin } from '$lib/auth';
	import { FormErrors } from '$lib/FormErrors';
	import Cookies from 'js-cookie';

	const camps = new FormErrors();

	interface FormErrors {
		email: any;
		password: any;
		name: any;
		confirmPassword: any;
	}

	let errors: FormErrors = { email: null, password: null, confirmPassword: null, name: null };

	let email = '';
	let name = '';
	let password = '';
	let confirmPassword = '';

	function validateCamps() {
		return (
			camps.validateEmail(email) && camps.validatePasswords(password, confirmPassword)
		);
	}

	async function handleRegister() {
		if (!validateCamps()) {
			goto('/register');
			return null;
		}
		let formData = {
			email: email,
			name: name,
			password: password,
			confirmPassword: confirmPassword
		};
		await fetchRegister(formData);
		const response = await fetchLogin(formData);
		const data = await response.json();
		if (response.ok) {
			const token = data?.token;
			Cookies.set('token', token, { expires: 365, secure: true });
			goto('/');
		} else {
			errors = data;
		}
	}
</script>

<div class="flex flex-col">
	<ol class="breadcrumb mb-[3rem]">
		<li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
		<li class="crumb-separator" aria-hidden>/</li>
		<li class="crumb">Vendedor</li>
	</ol>

	<form>
		<h3 class="text-4xl mb-[2rem]">Regístre su usuario</h3>

		<input class="input my-2" title="Nombre" type="text" placeholder="Usuario" bind:value={name} />

		{#if errors.name}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.name as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}

		<input class="input my-2" title="Email" type="text" placeholder="Email" bind:value={email} />

		{#if email.length > 0}
			{#if !camps.validateEmail(email)}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{camps.NotValidEmail}
				</div>
			{/if}
		{/if}

		{#if errors.email}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.email as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}

		<input
			class="input my-2"
			title="Contraseña"
			type="password"
			placeholder="Contraseña"
			bind:value={password}
		/>
		{#if errors.password}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.password as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		{#if password.length > 0}
			{#if password.length <= 5}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{camps.shortPass}
				</div>
			{:else if !camps.hasNumbers(password)}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{camps.NotNumbers}
				</div>
			{:else if !camps.hasUpperCase(password)}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{camps.NotUpperCase}
				</div>
			{/if}
		{/if}

		<input
			class="input my-2"
			title="RepContraseña"
			type="password"
			placeholder="Repita su Contraseña"
			bind:value={confirmPassword}
		/>
		{#if confirmPassword.length > 0}
			{#if password !== confirmPassword}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{camps.NotMatchingPass}
				</div>
			{/if}
		{/if}
		{#if errors.confirmPassword}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.confirmPassword as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		<button
			class="btn btn-xl variant-filled-primary my-2 w-full shadow-xl"
			on:click={handleRegister}>Registrarse</button
		>
		<p class="mt-4">
			¿Ya posees una cuenta? <a class="anchor no-underline" href="/login/user">Inicie sesión</a>
		</p>
	</form>
</div>
