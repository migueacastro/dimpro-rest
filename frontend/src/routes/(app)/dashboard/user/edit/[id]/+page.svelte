<script lang="ts">
	import { checkStaffGroup } from '$lib/auth.js';
	import Form from '$lib/components/Form.svelte';
	export let data;
	let {user} = data;
	let fields = data.fields;
</script>

<Form fields={fields} edit={true} user={user} endpoint={'user'} reload={true} table_name={'usuario'}/>