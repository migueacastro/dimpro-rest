<script lang="ts">
	//@ts-nocheck
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getData } from '$lib/components/data';
	import { fetchData } from '$lib/utils.ts';

	export let fields = [{ type: null, value: null, name: null, label: null }];
	export let endpoint = '';
	export let edit = false;
	export let method = '';
	let id = $page.params.id;
	async function isEditable() {
		if (edit) {
			let response = await fetchData(endpoint, 'GET');
			let data = await response.json();
			let value = data.filter((values: { id: string }) => values.id == id);
			for (let i = 0; i < fields.length; i++) {
				fields[i].value = value[0][`${fields[i].name}`];
			}
		}
	}
	async function sendData() {
		let body = {};
		fields.forEach((field) => {
			body[field.name] = field.value;
		});
		console.log(body);
		let response = await fetchData(endpoint, method, body);
		let data = await response.json();
		// TODO: Handle success, and errors
	}

	onMount(async () => {
		await isEditable();
	});
</script>

<form class=" gap-10 flex flex-col lg:flex-row">
	<div class="card my-3 p-10 text-start lg:w-[75%] space-y-6">
		{#each fields as field}
			<label
				class="label"
				for={field?.type == 'object' ? 'file' : field?.name}
				class:hidden={field?.type === 'hidden'}
			>
				<p class="capitalize">{field.label}</p>
				{#if field?.type === 'text'}
					<input class="input" type="text" bind:value={field.value} id={field.name} />
				{:else if field?.type === 'password'}
					<input class="input" type="password" bind:value={field.value} id={field.name} />
				{:else if field?.type === 'decimal'}
					<input
						class="input w-[25%]"
						type="number"
						min="0"
						step="0.01"
						bind:value={field.value}
						id={field.name}
					/>
				{:else if field?.type === 'integer'}
					<input
						class="input w-[25%]"
						type="number"
						min="0"
						bind:value={field.value}
						id={field.name}
					/>
				{:else if field?.type === 'boolean'}
					<p>bool</p>
				{:else if field?.type === 'hidden'}
					<input class="input" type="hidden" bind:value={field.value} id={field.name} />
				{:else if field?.type === 'date'}
					<input class="input" type="date" bind:value={field.value} id={field.name} />
				{:else if field?.type === 'datetime'}
					<input
						class="input"
						type="datetime-local"
						placeholder=""
						bind:value={field.value}
						id={field.name}
					/>
				{:else if field?.type === 'textarea'}
					<textarea class="textarea" bind:value={field.value} id={field.name} />
				{:else if field?.type == 'foreignKey'}
					<p>algo foraneo</p>
				{:else if field?.type == 'manyToMany'}
					<p>algo</p>
				{/if}
			</label>
		{/each}
		<button type="submit" class="btn variant-filled h-fit w-fit mx-auto btn-xl" on:click={sendData}
			>Guardar</button
		>
	</div>
</form>
