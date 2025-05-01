<script lang="ts">
	import Form from '$lib/components/Form.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { checkAdminGroup } from '$lib/auth';
	export let data;
	let {user} = data;
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{ type: 'hidden', value: [1, 2], name: 'groups', label: '' }
	];
	onMount(async () => {
		if (!checkAdminGroup(user)) {
			goto('/dashboard');
		}
	});
</script>

<Form
	{fields}
	method={'POST'}
	edit={false}
	endpoint={'staff'}
	table_name={'empleado/administrador'}
/>
