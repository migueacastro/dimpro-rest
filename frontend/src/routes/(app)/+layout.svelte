<script lang="ts">
    import { getDrawerStore, AppBar, getModalStore, Toast } from "@skeletonlabs/skeleton";
    let expandedSideBar = false;
    import { user } from "../../stores/stores";
    let expandedDrawer = false;
    const modalStore = getModalStore();
</script>


<!-- TODO: Drawer / Cajon para navegacion en movil -->


<div class="h-screen animate-show flex flex-col overflow-auto">
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
                    <a href="/dashboard">
                        <strong class="text-2xl uppercase">Dimpro</strong>
                    </a>
                </div>
                <div class="w-1/3 pt-[1rem] pr-[1rem] lg:pr-[2rem]">
                    <div class="lg:text-xl text-md capitalize text-end font-bold">
                        <div>{$user?.name.split()[0]} <i class="ml-2 fa-solid fa-user"></i></div>
                    </div>
                </div>
            </div>
        </header>
    </div>
    <!-- MOBILE NAVBAR -->

    <!-- SIDEBAR -->
    <aside class="lg:block lg:fixed card w-20 h-screen ease-linear 
    rounded-none z-10 hidden hover:show-sidebar hover:w-[14rem] dark:variant-filled-surface variant-filled-primary
    shadow-lg
    " class:hide-sidebar={!expandedSideBar}
    on:mouseover={() => expandedSideBar = true}
    on:mouseleave={() => expandedSideBar = false}
    on:focus
    >
        <a href="/dashboard">
            <div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
                <i class="py-5 fa-solid fa-house h3 w-20"></i>
                <p class="font-bold h5 fixed left-20"
                    class:opacity-0={!expandedSideBar}
                    class:show-text={expandedSideBar}
                    class:hide-text={!expandedSideBar}
                >
                    Inicio
                </p>
            </div>
        </a>
        <a href="/add">
            <div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
                <i class="py-5 fa-solid fa-plus h3 w-20"></i>
                <p class="font-bold h5 fixed left-20"
                    class:opacity-0={!expandedSideBar}
                    class:show-text={expandedSideBar}
                    class:hide-text={!expandedSideBar}
                >
                    Agregar
                </p>
            </div>
            
        </a>



    </aside>
    <!-- END SIDEBAR -->
    <slot/>
</div>






