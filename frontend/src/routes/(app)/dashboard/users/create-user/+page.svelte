<script lang="ts">
	import Form from '$lib/components/Form.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { checkAdminGroup, checkStaffGroup } from '$lib/auth';
	export let data;
	let {user} = data;
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{ type: 'hidden', value:'[3]', name: 'groups', label: '' }
	];
	onMount( () => {
		if (!(checkAdminGroup(user) || checkStaffGroup(user))) {
			goto('/dashboard');
		}
	});
</script>

<Form fields={fields} edit={false} endpoint={'users/'} table_name={'vendedor'}/>