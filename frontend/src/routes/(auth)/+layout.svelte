<script lang="ts">
	import { LightSwitch } from '@skeletonlabs/skeleton';
</script>

<!-- cambios: mt de 2.5 y my a auto -->
<div class="h-full w-full shadow-xl overflow-auto p-6" style="max-height: 120vh;">
	<div class="flex justify-end mx-[2rem] mt-[2rem]">
		<LightSwitch />
	</div>
	<div
		class="mx-auto my-[1.5rem] card p-[3rem] max-w-[45rem] text-center dark:variant-ghost-surface variant-outline-tertiary shadow-xl"
	>
		<slot />
	</div>
</div>

