<script lang="ts">
	//@ts-nocheck
	//TODO: clean this form in the end
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import {
		getToastStore,
		getModalStore,
		type ModalSettings,
		type ToastSettings,

		SlideToggle

	} from '@skeletonlabs/skeleton';
	import { enhance } from '$app/forms';

	const modalStore = getModalStore();
	const toastStore = getToastStore();
	export let user = {};
	export let fields: any = null;
	export let endpoint = '';
	export let edit = false;
	export let table_name = '';
	export let reload = false;
	let ogValue: any = null;
	let id = page.params.id;
	let action = '';

	let manyToManyListsDict = {};
	let inputChipListsDict = {};
	let valueChipListsDict = {};
	let inputChipDict = {};

	const error = new FormErrors();

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
	let passwordError: any = null;
	let repPasswordError: any = null;
	let hasErrors: boolean = false;
	function validateFields() {
		let valid: Boolean = false;
		valid =
			error.validateEmail(email) &&
			error.validatePhoneNumber(phoneNumber) &&
			error.validatePasswords(password, confirmPassword);
		validatedFields = valid;
		return valid;
	}
	$: console.log('fields', fields);
	function activatedErrors() {
		hasErrors = true;
		return '';
	}
	function deactivatedErrors() {
		hasErrors = false;
		return '';
	}
	function isEditable() {
		if (edit) {
			action = 'edit';
			let value = user;
			ogValue = value[`${fields[0].name}`];
			for (let i = 0; i < fields.length; i++) {
				if (fields[i].name !== 'groups') {
					fields[i].value = user[fields[i].name];
				}
			}
		} else {
			action = 'agreg';
		}
	}

	function updateConfirmation(event: any) {
		if (hasErrors) {
			const toast: ToastSettings = {
				message: 'No es posible proceder si hay errores.',
				background: 'variant-ghost-error',
				timeout: 7000
			};
			toastStore.trigger(toast);
		} else {
			const modal: ModalSettings = {
				type: 'confirm',
				title: `Modificar: de ${ogValue} a ${fields[0].value}`,
				body: `¿Está seguro de querer modificar este ${table_name}?`,
				response: (r: boolean) => {
					if (r) {
						const form = event.target.closest('form');
						if (form) {
							form.requestSubmit();
						}
					}
				}
			};
			modalStore.trigger(modal);
		}
	}

	function sendData() {
		return async ({ update, result }: any) => {
			if (result.data.success) {
				const toast: ToastSettings = {
					message: `El ${table_name} se ${action}ó con exito.`,
					background: 'variant-ghost-success',
					timeout: 7000
				};
				toastStore.trigger(toast);
			} else {
				const toast: ToastSettings = {
					message: `¡ERROR! El ${table_name} no se pudo ${action}ar.
							mensaje:${result.data.error}`,
					background: 'variant-ghost-error',
					timeout: 7000
				};
				toastStore.trigger(toast);
			}
			if (reload) {
				goto(`/dashboard/user`);
				setTimeout(() => {
					window.location.reload();
				},1000);
			} else {
				goto(`/dashboard/${endpoint}`);
			}
		};
	}
	function handleForm(event: Event) {
		if (hasErrors) {
			const toast: ToastSettings = {
				message: 'No es posible proceder si hay errores.',
				background: 'variant-ghost-error',
				timeout: 7000
			};
			toastStore.trigger(toast);
		} else {
			const form = event.target.closest('form');
			if (form) {
				form.requestSubmit();
			}
		}
	}
	function togglePassword(event: Event) {
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
	function validateRepPassword(event: Event) {
		let target = event.target as HTMLElement;
		const input = target.closest('input');
		let password = (input as HTMLInputElement).value;
		const originalPassword = (document.getElementsByName('password') as HTMLFormElement)[0].value;
		if (password.length > 0) {
			if (password.length <= 5) {
				repPasswordError = error.shortPass;
			} else if (!error.hasNumbers(password)) {
				repPasswordError = error.NotNumbers;
			} else if (!error.hasUpperCase(password)) {
				repPasswordError = error.NotUpperCase;
			} else if (password !== originalPassword) {
				repPasswordError = error.NotMatchingPass;
			} else {
				repPasswordError = null;
			}
		} else {
			repPasswordError = null;
		}
	}
	function validatePassword(event: Event) {
		let target = event.target as HTMLElement;
		const input = target.closest('input');
		let password = (input as HTMLInputElement).value;
		if (password.length > 0) {
			if (password.length <= 5) {
				passwordError = error.shortPass;
			} else if (!error.hasNumbers(password)) {
				passwordError = error.NotNumbers;
			} else if (!error.hasUpperCase(password)) {
				passwordError = error.NotUpperCase;
			} else {
				passwordError = null;
			}
		} else {
			passwordError = null;
		}
	}
	onMount(() => {
		isEditable();
	});
</script>

<form
	action={!edit ? '?/add' : `?/edit`}
	method="post"
	class="gap-5 flex flex-col mx-4 lg:mx-0 lg:flex-row"
	use:enhance={sendData}
>
	<div class="card my-3 p-5 text-start lg:w-[75%] space-y-4">
		{#if edit}
			<input class="input" type="hidden" bind:value={id} name="id" />
		{/if}
		<input class="input" type="hidden" bind:value={endpoint} name="endpoint" />
		{#each fields as field}
			<label
				class="label"
				for={field?.type == 'object' ? 'file' : field?.name}
				class:hidden={field?.type === 'hidden'}
			>
				<p class="capitalize">{field.label}</p>
				{#if field?.type === 'text'}
					{#if field.name === 'phonenumber'}
						<input
							class="input"
							title="telefono"
							type="text"
							name="phonenumber"
							placeholder="Número de telefono"
							bind:value={field.value}
							on:input={validateFields}
						/>
						{#if field?.value?.length > 0}
							{#if !error.validatePhoneNumber(field.value)}
								{activatedErrors()}
								<div class="card variant-ghost-error p-2 text-sm text-left">
									{error.NotValidPhone}
								</div>
							{:else}
								{deactivatedErrors()}
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
					{:else}
						<input class="input" type="text" bind:value={field.value} name={field.name} />
						{#if field.value.length > 0}
							{#if !error.validateText(field.value)}
								{activatedErrors()}
								<div class="card variant-ghost-error p-2 text-sm text-left">
									{error.hasSpecials}
								</div>
							{:else if field.value.length > 70}
								{activatedErrors()}
								<div class="card variant-ghost-error p-2 text-sm text-left">
									{error.tooLong}
								</div>
							{:else}
								{deactivatedErrors()}
							{/if}
						{/if}
					{/if}
				{:else if field?.type === 'email'}
					<input
						class="input my-2"
						title="Email"
						type="text"
						placeholder="Email"
						bind:value={field.value}
						name={field.name}
						on:input={validateFields}
					/>

					{#if field?.value?.length > 0}
						{#if !error.validateEmail(field.value)}
							{activatedErrors()}
							<div class="card variant-ghost-error p-2 text-sm text-left">
								{error.NotValidEmail}
							</div>
						{:else}
							{deactivatedErrors()}
						{/if}
					{/if}

					{#if errors?.field?.value.length > 0}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							<ul>
								{#each errors?.field?.value as error}
									<li>{error}</li>
								{/each}
							</ul>
						</div>
					{/if}
				{:else if field?.type === 'password'}
					<div class="input-group mb-2 input-group-divider grid-cols-[1fr_auto] p-0">
						<input
							class="input"
							type="password"
							bind:value={field.value}
							name={field.name}
							on:input={field.name === 'password' ? validatePassword : validateRepPassword}
						/>
						<button type="button" on:click={togglePassword}
							><i class="fa-regular fa-eye-slash"></i></button
						>
					</div>
					{#if passwordError && field.name === 'password'}
						{activatedErrors()}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							<ul>
								<li>{passwordError}</li>
							</ul>
						</div>
					{:else if repPasswordError && field.name === 'confirmPassword'}
						{activatedErrors()}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							<ul>
								<li>{repPasswordError}</li>
							</ul>
						</div>
					{:else}
						{deactivatedErrors() && ''}
					{/if}
				{:else if field?.type === 'decimal'}
					<input
						class="input w-[25%]"
						type="number"
						min="0"
						step="0.01"
						bind:value={field.value}
						name={field.name}
					/>
				{:else if field?.type === 'integer'}
					<input
						class="input w-[25%]"
						type="number"
						min="0"
						bind:value={field.value}
						name={field.name}
					/>
				{:else if field?.type === 'boolean'}
					<SlideToggle checked={field.value}>{field.label}</SlideToggle>
				{:else if field?.type === 'hidden'}
					<input class="input" type="text" bind:value={field.value} name={field.name} />
				{:else if field?.type === 'date'}
					<input class="input" type="date" bind:value={field.value} name={field.name} />
				{:else if field?.type === 'datetime'}
					<input
						class="input"
						type="datetime-local"
						placeholder=""
						bind:value={field.value}
						name={field.name}
					/>
				{:else if field?.type === 'textarea'}
					<textarea class="textarea" bind:value={field.value} name={field.name} />
				{:else if field?.type == 'foreignKey'}
					<p>algo foraneo</p>
				{:else if field?.type == 'manyToMany'}
					<!--<InputChip
						bind:input={inputChipDict[field.table]}
						bind:value={inputChipListsDict[field.table]}
						name="chips"
						on:remove={({ detail }) => removeChip(detail, field.table)}
						addChip={(event) => addChip(event.detail, field.table)}
						validation={InputChipValidation}
						invalid={''}
					/>
					<div class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto" tabindex="-1">
						<Autocomplete
							bind:input={inputChipDict[field.table]}
							options={manyToManyListsDict[field.table]}
							on:selection={({ detail }) => addChip(detail, field.table)}
						/>
					</div>-->
				{:else if field?.type == 'select'}
						<select class="select capitalize" bind:value={field.value} name={field?.name} id={field?.name}>
							{#each field?.options as option}
								<option class="capitalize" value={option.value}>
									{option.label}
								</option>
							{/each}
						</select>
				{/if}
			</label>
		{/each}
		{#if !edit}
			<button
				type="button"
				class="btn variant-filled h-fit w-fit mx-auto btn-xl"
				on:click={handleForm}>Guardar</button
			>
		{:else}
			<button
				type="button"
				class="btn variant-filled h-fit w-fit mx-auto btn-xl"
				on:click={(e) => {
					updateConfirmation(e);
				}}>Guardar</button
			>
		{/if}
	</div>
</form>
