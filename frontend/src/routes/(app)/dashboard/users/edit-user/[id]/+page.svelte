<script lang="ts">
	import { checkStaffGroup } from '$lib/auth';
import Form from '$lib/components/Form.svelte';
	export let data;
	let { user } = data;
	let { reqUser } = data;
	let fields = [
		{ type: 'email', value: '', name: 'email', label: 'email' },
		{ type: 'text', value: '', name: 'name', label: 'Nombre' },
		{ type: 'password', value: '', name: 'password', label: 'contraseña' },
		{ type: 'password', value: '', name: 'confirmPassword', label: 'confirmar contraseña' },
		{ type: 'text', value: '', name: 'phonenumber', label: 'telefono' },
		{
			type: 'select',
			value: data.reqUser.groups[0],
			name: 'groups',
			label: 'Tipo de usuario',
			options: data.groups
		}
	];
</script>

<h1 class="h2 my-4">Editar Vendedor</h1>
<Form {fields} edit={true} user={reqUser} endpoint={(checkStaffGroup(user)) ? 'staff' : 'users'} table_name={'vendedor'} />
