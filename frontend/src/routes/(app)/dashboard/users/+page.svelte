<script>
    import Datatable from '$lib/components/Datatable.svelte';
    import { apiURL } from '$lib/api_url';
  </script>
<Datatable editable={true} endpoint={`${apiURL}users`} fields={["name","email","phonenumber"]}/>