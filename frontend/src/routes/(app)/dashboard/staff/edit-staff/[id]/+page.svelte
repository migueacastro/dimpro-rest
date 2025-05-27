<script lang="ts">
	import Form from '$lib/components/Form.svelte';

	export let data;
	let {user} = data;
	let {reqUser} = data;
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{ type: 'select', value: data.reqUser.groups[0], name: 'groups', label: 'Tipo de usuario', options: data.groups},
	];
</script>

<Form fields={fields} edit={true} user={reqUser} endpoint={'staff'} table_name={'Empleado/Administrador'}/>