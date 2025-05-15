<script lang="ts">
	import {
		getModalStore,
		getToastStore,
		ProgressRadial,
		type ModalSettings,
		type ToastSettings
	} from '@skeletonlabs/skeleton';
	import { checkAdminGroup } from '$lib/auth';
	import { enhance } from '$app/forms';

	const modalStore = getModalStore();
	const toastStore = getToastStore();
	let elemCarousel: HTMLDivElement;
	//TODO: change with real data
	export let reminders: any;
	let date: any;
	export let user;
	let buttonAction = '';
	function carouselLeft(): void {
		const x =
			elemCarousel.scrollLeft === 0
				? elemCarousel.clientWidth * (elemCarousel.childElementCount - 1)
				: elemCarousel.scrollLeft - elemCarousel.clientWidth;

		elemCarousel.scrollTo({ left: x, behavior: 'smooth' });
	}

	function carouselRight(): void {
		const x =
			elemCarousel.scrollLeft === elemCarousel.scrollWidth - elemCarousel.clientWidth
				? 0
				: elemCarousel.scrollLeft + elemCarousel.clientWidth;

		elemCarousel.scrollTo({ left: x, behavior: 'smooth' });
	}
	function convertToDate(date: any) {
		date = date.split('T')[0];
		return date;
	}
	function handleResult() {
		return async ({ update, result }: any) => {
			if (result.data.success) {
				const toast: ToastSettings = {
					message: `El recordatorio se ${result.data.action}ó con exito.`,
					background: 'variant-ghost-success',
					timeout: 7000
				};
				toastStore.trigger(toast);

				setTimeout(() => {
					window.location.reload();
				}, 1000);
			} else {
				const toast: ToastSettings = {
					message: `¡ERROR! El recordatorio no se pudo ${result.data.action}ar.
							mensaje:${result.data.error}`,
					background: 'variant-ghost-error',
					timeout: 7000
				};
				toastStore.trigger(toast);
			}
		};
	}
	function deleteConfirmation(name: any, event: any) {
		// that button will trigger the confirmation popup, if it has response. Then it will trigger the formSubmission with this little one
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Eliminar: ${name}`,
			body: `¿Está seguro de querer eliminar este recordatorio?`,
			response: async (r: boolean) => {
				if (r) {
					const form = event.target.closest('form');
					if (form) {
						form.requestSubmit();
					}
				}
			}
		};
		modalStore.trigger(modal);
	}
</script>

<div class="mx-auto max-w-3xl my-2">
	{#if reminders && reminders.length > 0}
		{#if buttonAction === 'create'}
			<div class="card p-[2rem] grid grid-cols-[auto_1fr_auto] gap-4 items-center w-full">
				<form action="?/addReminder" method="post" use:enhance={handleResult}>
					<label class="label" for="object">
						<p class="capitalize">Recordatorio</p>
						<input type="text" class="input mb-5" name="note" placeholder="Recordatorio" />
						<div class="flex gap-5">
							<button type="submit" class="btn variant-filled">
								<i class="fa-solid fa-floppy-disk"></i>
							</button>
							<button
								type="button"
								class="btn variant-filled"
								on:click={() => {
									buttonAction = '';
								}}
							>
								<i class="fa-solid fa-x"></i>
							</button>
						</div>
					</label>
				</form>
			</div>
		{:else}
			<div class="card p-[2rem] grid grid-cols-[auto_1fr_auto] gap-4 items-center w-full">
				<button type="button" class="btn-icon variant-filled" on:click={carouselLeft}>
					<i class="fa-solid fa-arrow-left" />
				</button>
				<div
					bind:this={elemCarousel}
					class="scroll-smooth flex overflow-hidden w-[35rem] h-[10rem]"
				>
					{#each reminders as reminder}
						<div class="card flex-none w-[35rem] snap-start items-center">
							<header class="card-header text-center font-bold">{reminder.note}</header>
							<div class="p-2 text-center">{reminder.name}</div>
							<footer class="card-footer text-center font-thin">
								{convertToDate(reminder.date)}
							</footer>
							{#if checkAdminGroup(user)}
								<div class="flex">
									<form action="?/deleteReminder" method="post" use:enhance={handleResult}>
										<input type="hidden" name="id" bind:value={reminder.id} />
										<button
											type="button"
											class="btn-icon variant-filled"
											on:click={(e) => deleteConfirmation(reminder.note, e)}
										>
											<i class="fa-solid fa-trash" />
										</button>
									</form>
									<button
										class="btn-icon variant-filled ml-[29rem]"
										on:click={() => (buttonAction = 'edit')}
									>
										<i class="fa-solid fa-pencil" />
									</button>
								</div>
							{/if}
						</div>
					{/each}
				</div>
				<button type="button" class="btn-icon variant-filled" on:click={carouselRight}>
					<i class="fa-solid fa-arrow-right" />
				</button>
				{#if checkAdminGroup(user)}
					<button
						class="btn variant-filled"
						on:click={() => {
							buttonAction = 'create';
						}}
					>
						<i class="fa-solid fa-plus"></i>
					</button>
				{/if}
			</div>
		{/if}
	{/if}
</div>
