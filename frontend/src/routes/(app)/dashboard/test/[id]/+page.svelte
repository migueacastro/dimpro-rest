<script>
	import Form from '$lib/components/Form.svelte';
	let fieldss = [
		{ type: 'text', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' }
	];
</script>


<!--try with id 3, 32, 21-->
<Form fields={fieldss} method={'get'} edit={true} endpoint={'users'} />
