<script lang="ts">
	import { authenticate } from '$lib/auth';
	import Form from '$lib/components/Form.svelte';
	import { onMount } from 'svelte';
	import { user } from '../../../../../stores/stores';
	import { goto } from '$app/navigation';
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{ type: 'hidden', value: [1, 2], name: 'groups', label: '' }
	];
	onMount(async () => {
		await authenticate();
		let isAdmin = false;
		$user['groups'].forEach((group: any) => {
			if (group['name'] === 'admin') {
				isAdmin = true;
			}
		});
		if (!isAdmin) {
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
