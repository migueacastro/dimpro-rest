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

<Form fields={fields} edit={false} endpoint={'users/'} table_name={'vendedor'}/>