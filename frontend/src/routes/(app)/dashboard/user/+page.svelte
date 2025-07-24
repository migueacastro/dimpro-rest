<script lang="ts">
	import { goto } from '$app/navigation';
	import { checkAdminGroup, checkStaffGroup } from '$lib/auth';

	export let data;
	export let { user } = data; // I imported user from data, but notice that, in this route there is no +page.server.ts
	// So, why is the user being imported anyway? ???
	// I was making this before this morning.
	// The intersting very interesting thing i want you to see is this

	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		const opciones: Intl.DateTimeFormatOptions = {
			year: 'numeric',
			month: 'numeric',
			day: 'numeric',
			hour: 'numeric',
			minute: 'numeric',
			hour12: true // Formato de 12 horas (am/pm)
		};
		return new Intl.DateTimeFormat('es-ES', opciones).format(date);
	}
</script>

<div class="flex flex-col">
	<h4 class="h2 font-bold capitalize my-4">Perfil</h4>
	<div class="flex flex-col lg:flex-row">
		<div class="card p-[3rem] w-full mb-[2rem] flex flex-row justify-between shadow-md">
			<div class="flex flex-col">
				<div class="flex flex-col">
					<h4 class="h2 font-bold capitalize my-2">
						{!user?.name || user?.name.trim() == '' ? 'Usuario' : user.name}
					</h4>
					<h3 class="h3 font-bold capitalize my-2">
						{checkStaffGroup(user) ? (checkAdminGroup(user) ? 'Administrador': 'Empleado') : 'Vendedor'}
					</h3>
					<h4 class="h4 my-2">
						<i class="fa-solid fa-envelope text-primary-500 dark:text-surface-50"></i>
						{user?.email ?? 'No definido'}
					</h4>
				</div>
			</div>
			<i class="w-fit text-5xl fa-solid fa-user my-auto text-primary-500 dark:text-surface-50"></i>
		</div>
	</div>
	<div class="lg:flex flex-row space-x-4">
		<div class="card p-[2rem] mb-[2rem] w-auto lg:w-1/3 shadow-md flex flex-row justify-between">
			<div class="flex flex-col text-start pr-2">
				<h4 class="h3 font-bold capitalize">Información</h4>
				<p class="p">Se unió: {formatDate(user.date_joined)}</p>
				<p class="p">Último inicio de sesión: {formatDate(user.date_joined)}</p>
			</div>
			<i class="w-fit text-5xl fa-solid ml-2 fa-info my-auto text-primary-500 dark:text-surface-50"
			></i>
		</div>
		<div class="card p-[2rem] mb-[2rem] w-auto lg:w-1/3 shadow-md flex flex-row justify-between">
			<div class="flex flex-col text-start pr-2">
				<h4 class="h3 font-bold capitalize">Contacto</h4>
				<p class="p">Teléfono: {user?.phonenumber ?? 'No definido'}</p>
				<p class="p">Cédula: {user?.card_id ?? 'No definido'}</p>
				<p class="p">Dirección: {(String(user?.address)?.length > 0 && user?.address?.length) ? user?.address?.length : 'No definida'}</p>
			</div>
			<i
				class="w-fit text-5xl fa-solid ml-2 fa-address-book my-auto text-primary-500 dark:text-surface-50"
			></i>
		</div>
		<div class="card p-[2rem] mb-[2rem] w-auto lg:w-1/3 shadow-md flex flex-row justify-between">
			<div class="flex flex-col text-start pr-2 space-y-2">
				<h4 class="h3 font-bold capitalize">Acciones</h4>
				<div class="flex flex-row space-x-1"></div>
				<a class="text-primary-500 dark:text-surface-50" href="/dashboard/user/edit/{user.id}"
					><i class="fa-solid fa-pen-to-square mr-1"></i>Editar Perfil</a
				>
				<a class="text-primary-500 dark:text-surface-50" href="/dashboard/user/change-password"
					><i class="fa-solid fa-key mr-1"></i>Cambiar Contraseña</a
				>
				<a class="text-error-500" href="/salir" on:click|preventDefault={() => goto("/logout")}
					><i class="fa-solid fa-xmark mr-1"></i>Cerrar Sesión</a
				>
			</div>
			<i class="w-fit text-5xl fa-solid ml-2 fa-flag my-auto text-primary-500 dark:text-surface-50"
			></i>
		</div>
	</div>
</div>
