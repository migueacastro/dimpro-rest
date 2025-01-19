<script lang="ts">
    import { LightSwitch } from "@skeletonlabs/skeleton";
</script>

<!-- modificado de 6 a 3.75 porque el formulario de registro sobresalia la pantalla -->
<div class="h-full w-full shadow-xl"> 
    <div class="flex justify-end mx-[2rem] mt-[2rem]">
        <LightSwitch/>
        <!-- TODO: Arreglar modo oscuro -->
    </div>
    <div class="mx-auto my-[3.75rem] card p-[3rem] max-w-[45rem] text-center dark:variant-ghost-surface variant-outline-tertiary shadow-xl">
        <slot/>
    </div>
</div>