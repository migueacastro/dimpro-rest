<script>
  import {page} from '$app/state';
</script>
<div class="flex flex-col space-y-4 justify-center w-full text-center">
  <h1 class="h1">{page.status} {page.error?.message}</h1>
  <p class="p">Contacte al administrador</p>
  <button class="btn variant-filled-primary w-fit mx-auto text-2xl" on:click={()=> {
    window.history.back();
  }}>Volver</button>
</div>
