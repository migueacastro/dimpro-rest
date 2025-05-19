<script lang="ts">
	import Form from '$lib/components/Form.svelte';
	export let data;
	let {user} = data;
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' }
		];
</script>

<Form fields={fields} edit={true} user={user} endpoint={'users'} reload={true} table_name={'usuario'}/>