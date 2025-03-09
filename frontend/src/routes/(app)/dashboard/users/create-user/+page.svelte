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
		{ type: 'hidden', value: [1], name: 'groups', label: '' }
	];
	onMount(async () => {
		await authenticate();
		let isStaffOrAdmin = false;
		$user['groups'].forEach((group: any) => {
			if (group['name'] === 'staff' || group['name'] === 'admin') {
				isStaffOrAdmin = true;
			}
		});
		if (!isStaffOrAdmin) {
			goto('/dashboard');
		}
	});
</script>

<Form fields={fields} method={'POST'} edit={false} endpoint={'users'} table_name={'vendedor'}/>