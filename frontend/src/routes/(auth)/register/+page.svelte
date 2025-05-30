<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	$: loaded = true; 
	const fields = new FormErrors();

	interface FormErrors {
		email: any;
		password: any;
		name: any;
		confirmPassword: any;
		phoneNumber: any;
	}

	let errors: FormErrors = {
		email: [],
		password: [],
		confirmPassword: [],
		name: [],
		phoneNumber: []
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

	function handleEnhance() {
		loaded = false;
		return ({ update, result }: any) => {
			if (result?.type == 'success') {
				goto("/dashboard/");
			} else  {
				errors = result.data.error;
				loaded = true;
				return update({ reset: false });
			}
		};
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

{#if loaded }
<div class="flex flex-col">
	<ol class="breadcrumb mb-[3rem]">
		<li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
		<li class="crumb-separator" aria-hidden>/</li>
		<li class="crumb">Vendedor</li>
	</ol>

	<form class="flex flex-col space-y-2" method="post" action="?/register" use:enhance={handleEnhance}>
		<h3 class="text-4xl mb-[2rem]">Regístre su Vendedor</h3>

		<input
			class="input mb-2"
			title="Nombre"
			type="text"
			id="name"
			name="name"
			placeholder="Usuario"
			bind:value={name}
			on:input={validateFields}
		/>

		{#if errors?.name?.length > 0}
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
			id="email"
			name="email"
			placeholder="Email"
			bind:value={email}
			on:input={validateFields}
		/>

		{#if email.length > 0}
			{#if !fields.validateEmail(email)}
				<div class="card variant-ghost-error mb-2 p-2 text-sm text-left">
					{fields.NotValidEmail}
				</div>
			{/if}
		{/if}

		{#if errors?.email?.length > 0}
			<div class="card variant-ghost-error mb-2 p-2 text-sm text-left">
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
					id="password"
					name="password"
					placeholder="Contraseña"
					bind:value={password}
				/>
				<button type="button" on:click={togglePasswordVisibility}
					><i class="fa-regular fa-eye"></i></button
				>
			{/if}
		</div>
		{#if errors?.password?.length > 0}
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
					id="confirmPassword"
					name="confirmPassword"
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
					id="confirmPassword"
					name="confirmPassword"
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
		{#if errors?.confirmPassword?.length > 0 }
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
			id="phonenumber"
			name="phonenumber"
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
		{#if errors?.phoneNumber?.length > 0}
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
			disabled={!validatedFields}>Registrarse</button
		>
		<p class="mt-4">
			¿Ya posees una cuenta? <a class="anchor no-underline" href="/login/user">Inicie sesión</a>
		</p>
	</form>
</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}