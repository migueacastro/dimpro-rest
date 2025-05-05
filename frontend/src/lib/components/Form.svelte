<script lang="ts">
	//@ts-nocheck
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { fetchData } from '$lib/utils.ts';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import {
		getToastStore,
		getModalStore,
		type ModalSettings,
		type ToastSettings
	} from '@skeletonlabs/skeleton';
	import { enhance } from '$app/forms';

	const modalStore = getModalStore();
	const toastStore = getToastStore();
	export let user = {};
	export let fields: any = null;
	export let endpoint = '';
	export let edit = false;
	export let table_name = '';
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
	function validateFields() {
		let valid: Boolean = false;
		valid =
			error.validateEmail(email) &&
			error.validatePhoneNumber(phoneNumber) &&
			error.validatePasswords(password, confirmPassword);
		validatedFields = valid;
		return valid;
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
			goto(`/dashboard/${endpoint}`);
		};
	}

	onMount(() => {
		isEditable();
	});
</script>

<form
	action={!edit ? '?/add' : `?/edit`}
	method="post"
	class="gap-10 flex flex-col ml-[13rem] lg:flex-row"
	use:enhance={sendData}
>
	<div class="card my-3 p-10 text-start lg:w-[75%] space-y-6">
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
								<div class="card variant-ghost-error p-2 text-sm text-left">
									{error.NotValidPhone}
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
					{:else}
						<input class="input" type="text" bind:value={field.value} name={field.name} />
						{#if field.value.length > 0}
						{#if !error.validateText(field.value)}
							<div class="card variant-ghost-error p-2 text-sm text-left">
								{error.hasSpecials}
							</div>
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
							<div class="card variant-ghost-error p-2 text-sm text-left">
								{error.NotValidEmail}
							</div>
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
					<input class="input" type="password" bind:value={field.value} name={field.name} />
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
					<p>bool</p>
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
				{/if}
			</label>
		{/each}
		{#if !edit}
			<button type="submit" class="btn variant-filled h-fit w-fit mx-auto btn-xl">Guardar</button>
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
