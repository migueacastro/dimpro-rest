<script>
    import Datatable from '$lib/components/Datatable.svelte';
  </script>
<h1 class="h2 my-4">Usuarios</h1>
<Datatable editable={true} endpoint={"users"} fields={["name","email","phonenumber"]}/>
