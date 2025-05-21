<script lang="ts">
	import {
		getDrawerStore,
		AppBar,
		getModalStore,
		Toast,
		LightSwitch,
		Modal,
		Drawer
	} from '@skeletonlabs/skeleton';
	let expandedSideBar = false;
	import logo from '$lib/assets/logodimpro.svg';
	import logolight from '$lib/assets/logodimprolight.svg';
	import icon from '$lib/assets/iconlight.svg';
	import { checkStaffGroup, checkAdminGroup, checkPermission } from '$lib/auth.ts';
	import { goto } from '$app/navigation';
	import { check } from '@vincjo/datatables';
	let expandedDrawer = false;
	export let data;
	const user = data.user;
	const drawerStore = getDrawerStore();
	const layoutDrawerSettings = {
		id: 'layoutDrawer',
		bgDrawer: 'variant-filled-primary dark:variant-filled-surface'
	}; // Settings for oppening drawer

	const modalStore = getModalStore();

	function hideDrawer() {
		expandedDrawer = false;
		setTimeout(drawerStore.close, 100);
	}
</script>

<Modal height="h-auto" regionBody="h-auto overflow-hidden"></Modal>

<!-- MOBILE DRAWER -->
<Drawer position="top" height="h-[97%] overflow-hidden">
	{#if $drawerStore.id === 'layoutDrawer'}
		<!-- Drawer is always open once the drawerStore loads, depending on the id, it will show different things -->
		<nav class="list-nav m-2 text-center">
			<button
				on:click={() => {
					// Button that activates this drawer section
					expandedDrawer = false;
					setTimeout(drawerStore.close, 400); // close drawer after 400ms so that animation works fine
				}}
			>
				<i class="fa-solid fa-arrow-up h2"></i>
			</button>

			<ul class="my-2 mx-auto">
				<li>
					<a href="/dashboard" class="w-fit my-2 mx-auto h4 font-bold" on:click={hideDrawer}>
						Inicio
					</a>
				</li>
				{#if checkPermission(user, 'add_order')}
					<li>
						<a
							href="/dashboard/add-order"
							class="w-fit my-2 mx-auto h4 font-bold"
							on:click={hideDrawer}
						>
							Crear Pedido
						</a>
					</li>
				{/if}
				{#if checkPermission(user, 'view_own_order')}
					<li>
						<a
							href="/dashboard/orders"
							class="w-fit my-2 mx-auto h4 font-bold"
							on:click={hideDrawer}
						>
							Pedidos
						</a>
					</li>
				{/if}
				{#if checkPermission(user, 'view_product')}
					<li>
						<a
							href="/dashboard/inventory"
							class="w-fit my-2 mx-auto h4 font-bold"
							on:click={hideDrawer}
						>
							Inventario
						</a>
					</li>
				{/if}
				{#if checkPermission(user, 'view_user')}
					<li>
						<a
							href="/dashboard/users"
							class="w-fit my-2 mx-auto h4 font-bold"
							on:click={hideDrawer}
						>
							Vendedores
						</a>
					</li>
				{/if}
				{#if checkPermission(user, 'view_staff_user')}
					<li>
						<a
							href="/dashboard/staff"
							class="w-fit my-2 mx-auto h4 font-bold"
							on:click={hideDrawer}
						>
							Empleados
						</a>
					</li>
				{/if}
				{#if checkPermission(user, 'view_settings_user')}
					<li>
						<a
							href="/dashboard/settings"
							class="w-fit my-2 mx-auto h4 font-bold"
							on:click={hideDrawer}
						>
							Configuración
						</a>
					</li>
				{/if}
				<li>
					<a
						href="salir"
						on:click|preventDefault={() => {
							hideDrawer();
							goto('/logout');
						}}
						class="w-fit my-2 mx-auto h4 font-bold"
					>
						Cerrar Sesión
					</a>
				</li>
				<li>
					<div class="w-fit my-2 mx-auto flex flex-row">
						<p class="mr-6">Tema</p>
						<LightSwitch></LightSwitch>
					</div>
				</li>
			</ul>
		</nav>
	{/if}
</Drawer>
<!-- END MOBILE DRAWER-->

<div class="h-screen animate-show flex flex-col overflow-auto w-full">
	<!-- NAVBAR -->
	<div
		class="lg:ml-auto w-full lg:w-[calc(100%-5rem)] variant-soft-tertiary shadow-lg text-primary-500"
	>
		<Toast />
		<header
			class:show-navbar={expandedDrawer == false}
			class:hide-navbar={expandedDrawer}
			class="w-full mx-auto"
		>
			<div class="flex pb-[1rem]">
				<div class="lg:hidden block w-1/3 pt-[1rem] pl-[1rem] lg:pl-[2rem]">
					<button
						on:click={() => {
							expandedDrawer = true;
							setTimeout(() => drawerStore.open(layoutDrawerSettings), 400);
						}}
					>
						<i class="fa-solid fa-bars text-xl md:text-3xl"></i>
					</button>
				</div>
				<div class="lg:ml-[45%] w-1/3 text-center lg:text-start pt-[1rem] md:ml-[5%]">
					<div class="lg:hidden mx-auto">
						<a href="/dashboard" class="flex dark:hidden md:h-[2rem] md:ml-[5%]">
							<img src={logo} alt="" />
						</a>
						<a href="/dashboard" class="hidden dark:flex md:h-[2rem] md:ml-[5%]">
							<img src={logolight} alt="" />
						</a>
					</div>
				</div>
				<div class="w-1/3 pt-[1rem] pr-[1rem] lg:pr-[2rem] flex flex-row justify-end">
					<div
						class="lg:text-xl text-md capitalize text-end font-bold md:text-xl md:flex md:align-middle"
					>
						<a href="/dashboard/user">
							<div>{user?.name?.split()[0]} <i class="ml-2 fa-solid fa-user"></i></div>
						</a>
					</div>
					<div class="hidden lg:flex w-auto ml-4"><LightSwitch /></div>
				</div>
			</div>
		</header>
	</div>
	<!-- END NAVBAR -->

	<!-- SIDEBAR -->
	<aside
		class="lg:block lg:fixed card w-20 h-screen ease-linear
    rounded-none z-10 hidden hover:show-sidebar hover:w-[16rem] dark:variant-filled-surface variant-filled-primary
    shadow-lg divide-y-2 divide-white
    "
		class:hide-sidebar={!expandedSideBar}
		on:mouseover={() => (expandedSideBar = true)}
		on:mouseleave={() => (expandedSideBar = false)}
		on:focus
	>
		<a href="dimpro" on:click|preventDefault={() => goto('/dashboard')}>
			<div
				class="px-2 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface mt-1"
			>
				<img src={icon} alt="" class="w-[4rem]" />
				{#if expandedSideBar}
					<img src={logolight} alt="" class="mx-auto w-[9rem]" />
				{/if}
			</div>
		</a>

		<hr class="w-[80%] mx-auto my-2" />
		{#if checkPermission(user, 'add_order')}
			<a href="/dashboard/add-order" on:click|preventDefault={() => goto('/dashboard/add-order')}>
				<div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
					<i class="py-5 fa-solid fa-plus h3 w-20"></i>
					<p
						class="font-bold h5 fixed left-20"
						class:opacity-0={!expandedSideBar}
						class:show-text={expandedSideBar}
						class:hide-text={!expandedSideBar}
					>
						Crear Pedido
					</p>
				</div>
			</a>
		{/if}
		{#if checkPermission(user, 'view_own_order')}
			<a href="pedidos" on:click|preventDefault={() => goto('/dashboard/orders')}>
				<div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
					<i class="py-5 fa-solid fa-box h3 w-20"></i>
					<p
						class="font-bold h5 fixed left-20"
						class:opacity-0={!expandedSideBar}
						class:show-text={expandedSideBar}
						class:hide-text={!expandedSideBar}
					>
						Pedidos
					</p>
				</div>
			</a>
		{/if}
		{#if checkPermission(user, 'view_product')}
			<a href="inventario" on:click|preventDefault={() => goto('/dashboard/inventory')}>
				<div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
					<i class="py-5 fa-solid fa-boxes-stacked h3 w-20"></i>
					<p
						class="font-bold h5 fixed left-20"
						class:opacity-0={!expandedSideBar}
						class:show-text={expandedSideBar}
						class:hide-text={!expandedSideBar}
					>
						Inventario
					</p>
				</div>
			</a>
		{/if}

		{#if checkPermission(user, 'view_user')}
			<a href="vendedores" on:click|preventDefault={() => goto('/dashboard/users')}>
				<div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
					<i class="py-5 fa-solid fa-users h3 w-20"></i>
					<p
						class="font-bold h5 fixed left-20"
						class:opacity-0={!expandedSideBar}
						class:show-text={expandedSideBar}
						class:hide-text={!expandedSideBar}
					>
						Vendedores
					</p>
				</div>
			</a>
		{/if}

		{#if checkPermission(user, 'view_staff_user')}
			<a href="empleados" on:click|preventDefault={() => goto('/dashboard/staff')}>
				<div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
					<i class="py-5 fa-solid fa-users-gear h3 w-20"></i>
					<p
						class="font-bold h5 fixed left-20"
						class:opacity-0={!expandedSideBar}
						class:show-text={expandedSideBar}
						class:hide-text={!expandedSideBar}
					>
						Empleados
					</p>
				</div>
			</a>
		{/if}
		{#if checkPermission(user, 'view_settings_user')}
			<a href="configuracion" on:click|preventDefault={() => goto('/dashboard/settings')}>
				<div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
					<i class="py-5 fa-solid fa-gear h3 w-20"></i>
					<p
						class="font-bold h5 fixed left-20"
						class:opacity-0={!expandedSideBar}
						class:show-text={expandedSideBar}
						class:hide-text={!expandedSideBar}
					>
						Configuración
					</p>
				</div>
			</a>
		{/if}

		<a href="salir" on:click|preventDefault={() => goto('/logout')}>
			<div class="px-7 flex flex-row items-center bg-gradient-to-br hover:variant-soft-surface">
				<i class="py-5 fa-solid fa-arrow-right-from-bracket h3 w-20"></i>
				<p
					class="font-bold h5 fixed left-20"
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
	<div class="m-[2rem] lg:m-[3rem] lg:ml-[8rem]">
		<slot />
	</div>
	<Toast />
</div>
