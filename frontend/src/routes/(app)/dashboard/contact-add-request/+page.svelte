<script>
	import { checkPermission } from '$lib/auth';
	import Datatable from '$lib/components/Datatable.svelte';
	export let data;
</script>


{#if (checkPermission(data.user, 'view_contactaddrequest'))}
  <div class="flex justify-between flex-row">
    <h1 class="h2 my-4 w-fit">Solicitudes de agregar Cliente</h1> 

      <a href="/dashboard/contact-add-request/add" class="btn variant-filled w-fit my-[2rem] px-[2rem]">Agregar</a>
  </div>
	
	<Datatable
		editable={false}
		source_data={data.list_all}
		endpoint={{ main: 'contact-add-request'}}
		headings={[ 'Nombre', 'Cédula', 'Email', 'Dirección', 'Teléfono', 'Usuario','Estatus','Fecha']}
		fields={[ 'name', 'identification', 'email', 'address', 'phonePrimary', 'user_name', 'status','date_format']}
	/>
{/if}
