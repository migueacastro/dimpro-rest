<script lang="ts">
	import Form from '$lib/components/Form.svelte';
	export let data;
	let {user} = data;
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' }
	];
</script>

<Form
	{fields}
	edit={false}
	endpoint={'staff'}
	table_name={'empleado/administrador'}
/>
