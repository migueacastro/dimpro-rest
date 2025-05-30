<script lang="ts">
	import { checkStaffGroup } from '$lib/auth.js';
	import Form from '$lib/components/Form.svelte';
	export let data;
	let {user} = data;
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		];
</script>

<Form fields={fields} edit={true} user={user} endpoint={(checkStaffGroup(user)) ? 'staff' : 'users'} reload={true} table_name={'usuario'}/>