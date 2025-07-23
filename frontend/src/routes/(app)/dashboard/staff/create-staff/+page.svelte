<script lang="ts">
	import Form from '$lib/components/Form.svelte';
	export let data: any;
	let {user} = data;
	let fields = [
		{ type: 'text', value: '', name: 'card_id', label: 'Cédula' },
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{ type: 'longtext', value: '', name: 'address', label: 'Dirección' },
		{
			type: 'select',
			value: data?.groups[0].value,
			name: 'groups',
			label: 'Tipo de usuario',
			options: data?.groups,
		}
	];
</script>
<h1 class="h2 my-4">Crear Empleado</h1>
<Form
	{fields}
	edit={false}
	endpoint={'staff/'}
	table_name={'empleado/administrador'}
/>
