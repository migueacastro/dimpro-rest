<script lang="ts">
    import { getDrawerStore, AppBar, getModalStore, Toast, LightSwitch } from "@skeletonlabs/skeleton";
    let expandedSideBar = false;
    import logo from "$lib/assets/logodimpro.svg" 
    import logolight from "$lib/assets/logodimprolight.svg"
    import icon from "$lib/assets/iconlight.svg"
	import { onMount } from "svelte";
	import { authenticate } from "$lib/auth";
    import { user } from "../../stores/stores";
	import { goto } from "$app/navigation";
    let expandedDrawer = false;
    
    const modalStore = getModalStore();
    onMount(async () => {
        if (!user) {
            await goto("/");
        }
    });
</script>

<!-- TODO: Drawer / Cajon para navegacion en movil -->


<div class="h-screen animate-show flex flex-col overflow-auto w-full">
    <!-- NAVBAR -->
    <div class="lg:ml-auto w-full lg:w-[calc(100%-5rem)] variant-soft-tertiary shadow-lg text-primary-500">
        <Toast/>
        <header class:show-navbar={expandedDrawer == false} 
        class:hide-navbar={expandedDrawer} class="w-full mx-auto"
        >
            <div class="flex pb-[1rem]">
                <div class="lg:hidden block w-1/3 pt-[1rem] pl-[1rem] lg:pl-[2rem]">
                    <i class="fa-solid fa-bars text-xl"></i>
                </div>
                <div class="lg:ml-[45%] w-1/3 text-center lg:text-start pt-[1rem]">
                    <div class="lg:hidden">
                        <a href="/dashboard" class="flex dark:hidden">
                            <img src={logo} alt="">
                        </a>
                        <a href="/dashboard" class="hidden dark:flex">
                            <img src={logolight} alt="">
                        </a>
                    </div>
                </div>
                <div class="w-1/3 pt-[1rem] pr-[1rem] lg:pr-[2rem] flex flex-row justify-end">
                    <div class="lg:text-xl text-md capitalize text-end font-bold">
                        <div>{$user?.name?.split()[0]} <i class="ml-2 fa-solid fa-user"></i></div>
                    </div>
                    <div class="hidden lg:flex w-auto ml-4"><LightSwitch/></div>
                </div>
            </div>
        </header>
    </div>
    <!-- MOBILE NAVBAR -->

    <!-- SIDEBAR -->
    <aside class="lg:block lg:fixed card w-20 h-screen ease-linear 
    rounded-none z-10 hidden hover:show-sidebar hover:w-[16rem] dark:variant-filled-surface variant-filled-primary
    shadow-lg divide-y-2 divide-white 
    " class:hide-sidebar={!expandedSideBar}
    on:mouseover={() => expandedSideBar = true}
    on:mouseleave={() => expandedSideBar = false}
    on:focus
    >
        <a href="/dashboard">
            <div class="px-2 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface mt-1 ">
                <img src={icon} alt="" class="w-[4rem]">
                {#if expandedSideBar }
                    <img src={logolight} alt="" class="mx-auto w-[9rem]">
                {/if}
            </div>
        </a>

        <hr class="w-[80%] mx-auto my-2">
       
        <a href="/add">
            <div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
                <i class="py-5 fa-solid fa-plus h3 w-20"></i>
                <p class="font-bold h5 fixed left-20"
                    class:opacity-0={!expandedSideBar}
                    class:show-text={expandedSideBar}
                    class:hide-text={!expandedSideBar}
                >
                    Crear Pedido
                </p>
            </div>
            
        </a>
        <a href="/orders">
            <div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
                <i class="py-5 fa-solid fa-box h3 w-20"></i>
                <p class="font-bold h5 fixed left-20"
                    class:opacity-0={!expandedSideBar}
                    class:show-text={expandedSideBar}
                    class:hide-text={!expandedSideBar}
                >
                    Pedidos
                </p>
            </div>
            
        </a>
        <a href="/inventory">
            <div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
                <i class="py-5 fa-solid fa-boxes-stacked h3 w-20"></i>
                <p class="font-bold h5 fixed left-20"
                    class:opacity-0={!expandedSideBar}
                    class:show-text={expandedSideBar}
                    class:hide-text={!expandedSideBar}
                >
                    Inventario
                </p>
            </div>
            
        </a>
        <a href="/logout">
            <div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
                <i class="py-5 fa-solid fa-arrow-right-from-bracket h3 w-20"></i>
                <p class="font-bold h5 fixed left-20"
                    class:opacity-0={!expandedSideBar}
                    class:show-text={expandedSideBar}
                    class:hide-text={!expandedSideBar}
                >
                    Cerrar Sesión
                </p>
            </div>
            
        </a>



    </aside>
    <!-- END SIDEBAR -->
    <slot/>
</div>






