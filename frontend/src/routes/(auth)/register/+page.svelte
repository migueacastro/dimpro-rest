<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchRegister, fetchLogin } from '$lib/auth';
	import { FormErrors } from '$lib/FormErrors';
	import Cookies from 'js-cookie';
	import { authenticate } from '$lib/auth';

	const fields = new FormErrors();

	interface FormErrors {
		email: any;
		password: any;
		name: any;
		confirmPassword: any;
		phoneNumber: any;
	}

	let errors: FormErrors = {
		email: null,
		password: null,
		confirmPassword: null,
		name: null,
		phoneNumber: null
	};

	let email = '';
	let name = '';
	let password = '';
	let confirmPassword = '';
	let phoneNumber = '';
	let validatedFields: Boolean = false;
	function validateFields() {
		let valid: Boolean = false;
		valid =
			fields.validateEmail(email) &&
			fields.validatePhoneNumber(phoneNumber) &&
			fields.validatePasswords(password, confirmPassword);
		validatedFields = valid;
		return valid;
	}

	async function handleRegister() {
		if (!validateFields()) {
			goto('/register');
			window.location.reload();
			return null;
		}
		let formData = {
			email: email,
			name: name,
			password: password,
			confirmPassword: confirmPassword,
			phoneNumber: phoneNumber
		};
		await fetchRegister(formData);
		const response = await fetchLogin(formData);
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
	let showRepPassword = false;
	function toggleRepPasswordVisibility() {
		showRepPassword = !showRepPassword;
	}
	let inputRepType = 'password';
	$: inputRepType = showRepPassword ? 'text' : 'password';
</script>

<title>Registrar Vendedor</title>

<div class="flex flex-col">
	<ol class="breadcrumb mb-[3rem]">
		<li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
		<li class="crumb-separator" aria-hidden>/</li>
		<li class="crumb">Vendedor</li>
	</ol>

	<form>
		<h3 class="text-4xl mb-[2rem]">Regístre su Vendedor</h3>

		<input
			class="input"
			title="Nombre"
			type="text"
			placeholder="Usuario"
			bind:value={name}
			on:input={validateFields}
		/>

		{#if errors.name}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.name as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}

		<input
			class="input my-2"
			title="Email"
			type="text"
			placeholder="Email"
			bind:value={email}
			on:input={validateFields}
		/>

		{#if email.length > 0}
			{#if !fields.validateEmail(email)}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{fields.NotValidEmail}
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
		{#if password.length > 0}
			{#if password.length <= 5}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{fields.shortPass}
				</div>
			{:else if !fields.hasNumbers(password)}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{fields.NotNumbers}
				</div>
			{:else if !fields.hasUpperCase(password)}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{fields.NotUpperCase}
				</div>
			{/if}
		{/if}

		<div class="input-group input-group-divider grid-cols-[1fr_auto] my-2">
			{#if showRepPassword}
				<input
					class="input"
					title="Confirmar Contraseña"
					type="text"
					placeholder="Confirmar Contraseña"
					bind:value={confirmPassword}
				/>
				<button type="button" on:click={toggleRepPasswordVisibility}
					><i class="fa-regular fa-eye-slash"></i></button
				>
			{:else}
				<input
					class="input"
					title="Confirmar Contraseña"
					type="password"
					placeholder="Confirmar Contraseña"
					bind:value={confirmPassword}
				/>
				<button type="button" on:click={toggleRepPasswordVisibility}
					><i class="fa-regular fa-eye"></i></button
				>
			{/if}
		</div>
		{#if confirmPassword.length > 0}
			{#if password !== confirmPassword}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{fields.NotMatchingPass}
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
		<input
			class="input"
			title="telefono"
			type="text"
			placeholder="Número de telefono"
			bind:value={phoneNumber}
			on:input={validateFields}
		/>
		{#if phoneNumber.length > 0}
			{#if !fields.validatePhoneNumber(phoneNumber)}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					{fields.NotValidPhone}
				</div>
			{/if}
		{/if}
		{#if errors.phoneNumber}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.phoneNumber as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		<button
			class="btn btn-xl variant-filled-primary my-2 w-full shadow-xl"
			on:click={handleRegister}
			disabled={!validatedFields}>Registrarse</button
		>
		<p class="mt-4">
			¿Ya posees una cuenta? <a class="anchor no-underline" href="/login/user">Inicie sesión</a>
		</p>
	</form>
</div>
