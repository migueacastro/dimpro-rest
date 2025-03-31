<script lang="ts">
	import { enhance } from '$app/forms';

	interface FormErrors {
		email: any;
		password: any;
	}
	$: errors = { email: [], password: [] };

	let email = '';
	let password = '';

	let showPassword = false;
	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}
	let inputType = 'password';
	$: inputType = showPassword ? 'text' : 'password';

	function handleEnhance({ formData, action }: { formData: FormData; action: URL }) {
		fetch(action, {
			method: 'POST',
			body: formData
		})
			.then(async (response) => {
				const result = await response.json();
				if (result.type !== 'success') {
					// Access errors directly
					console.log(JSON.parse(result.data));
					let data = JSON.parse(result.data);
					data = JSON.parse(data[2]);
					errors = data;
				}
			})
			.catch((error) => {
				console.error('Error al enviar el formulario:', error);
			});
	}
</script>

<title>Inicio Sesión</title>

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
			bind:value={email}
		/>

		{#if errors.email.length > 0}
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
		<button class="btn btn-xl variant-filled-tertiary my-2 w-full shadow-xl" type="submit"
			>Iniciar Sesión</button
		>
	</form>
</div>
