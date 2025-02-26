<script>
	import Form from '$lib/components/Form.svelte';
	let fieldss = [
		{ type: 'text', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{ type: 'hidden', value: [1], name: 'groups', label: '' }
	];
</script>


<!--try with id 3, 32, 21-->
<Form fields={fieldss} method={'post'} edit={false} endpoint={'users'} />
