<script lang="ts">
	import { checkPermission, checkStaffGroup } from '$lib/auth.js';
	import Form from '$lib/components/Form.svelte';
	export let data: any;
	let {user} = data;
	let fields: any = data.fields;
		

</script>

<Form fields={fields} edit={true} user={user} endpoint={'user'} reload={true} table_name={'usuario'}/>