<script lang="ts">
	
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getData } from '$lib/components/data';
	import { fetchData } from '$lib/utils.ts';
	import { goto } from '$app/navigation';

	export let fields = [{ type: null, value: null, name: null, label: null }];
	export let endpoint = '';
	export let edit = false;
	export let method = '';
	let id = $page.params.id;

    let manyToManyListsDict = {};
    let inputChipListsDict = {};
    let valueChipListsDict = {};
    let inputChipDict = {};


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
		let response = await fetchData(endpoint, method, body);
		if(response.ok){
			goto("/dashboard/users");
		}
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
					<InputChip bind:input={inputChipDict[field.table]} bind:value={inputChipListsDict[field.table]} name="chips" on:remove={({ detail }) => removeChip(detail, field.table)} addChip={(event) => addChip(event.detail, field.table)} validation={InputChipValidation} invalid={''}/>
                        <div class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto" tabindex="-1">
                            <Autocomplete
                                bind:input={inputChipDict[field.table]}
                                options={manyToManyListsDict[field.table]}
                                on:selection={({ detail }) => addChip(detail, field.table)}
                                
                            />
                        </div>
				{/if}
			</label>
		{/each}
		<button type="submit" class="btn variant-filled h-fit w-fit mx-auto btn-xl" on:click={sendData}
			>Guardar</button
		>
	</div>
</form>
