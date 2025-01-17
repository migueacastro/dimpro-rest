<script lang="ts">
	import { user } from "../stores/stores";
</script>
<div class="m-[6rem]">
	<button type="button" class="btn btn-xl variant-filled-primary">Hola {$user?.name}</button>
</div>