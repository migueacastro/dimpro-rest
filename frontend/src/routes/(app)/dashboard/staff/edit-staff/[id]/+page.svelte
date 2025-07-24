<script lang="ts">
	import Form from '$lib/components/Form.svelte';

	export let data;
	let {user} = data;
	let {reqUser} = data;
	let fields = [
		{ type: 'text', value: '', name: 'card_id', label: 'Cédula' },
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{ type: 'longtext', value: '', name: 'address', label: 'Dirección' },
		{ type: 'select', value: data.reqUser.groups[0], name: 'groups', label: 'Tipo de usuario', options: data.groups},
	];
</script>

<h1 class="h2 my-4">Editar Empleado</h1>
<Form fields={fields} edit={true} user={reqUser} endpoint={'staff'} table_name={'Empleado/Administrador'}/>