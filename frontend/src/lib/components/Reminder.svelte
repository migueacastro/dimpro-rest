<script lang="ts">
	import {
		getModalStore,
		getToastStore,
		ProgressRadial,
		type ModalSettings,
		type ToastSettings
	} from '@skeletonlabs/skeleton';
	import { checkAdminGroup, checkPermission } from '$lib/auth';
	import { enhance } from '$app/forms';

	const modalStore = getModalStore();
	const toastStore = getToastStore();
	let elemCarousel: HTMLDivElement;
	export let reminders: any = [];
	export let user;
	let loading: boolean = false;

	$: sortedReminders = (reminders || [])
		?.slice() // evitar modificar in-place
		.sort((a: any, b: any) => new Date(b.date).getTime() - new Date(a.date).getTime())
		.map((reminder: any, index: number) => ({ ...reminder, index }));
	let reminderSelected: any;
	$: if (sortedReminders && !reminderSelected) {
		reminderSelected = sortedReminders[0] || null;
	}
	let buttonAction = '';
	function carouselLeft(): void {
		const x =
			elemCarousel.scrollLeft === 0
				? elemCarousel.clientWidth * (elemCarousel.childElementCount - 1)
				: elemCarousel.scrollLeft - elemCarousel.clientWidth;
		reminderSelected =
			reminderSelected.index - 1 < 0
				? sortedReminders[sortedReminders.length - 1]
				: sortedReminders[reminderSelected.index - 1];
		scrollToReminder(reminderSelected);
	}

	function carouselRight(): void {
		const isAtEnd = elemCarousel.scrollLeft >= elemCarousel.scrollWidth - elemCarousel.clientWidth;
		const x = isAtEnd ? 0 : elemCarousel.scrollLeft + elemCarousel.clientWidth;
		reminderSelected =
			reminderSelected.index + 1 === sortedReminders.length
				? sortedReminders[0]
				: sortedReminders[reminderSelected.index + 1];
		scrollToReminder(reminderSelected);
	}

	function scrollToReminder(reminder: any) {
		const cardWidth = elemCarousel.clientWidth;
		elemCarousel.scrollTo({ left: reminder.index * cardWidth, behavior: 'smooth' });
	}

	function convertToDate(date: any) {
		date = date.split('T')[0];
		return date;
	}
	function handleResult() {
		loading = true;
		return async ({ update, result }: any) => {
			if (result.data.success) {
				const toast: ToastSettings = {
					message: `El recordatorio se ${result.data.action}ó con exito.`,
					background: 'variant-ghost-success',
					timeout: 3500
				};
				toastStore.trigger(toast);

				reminders = result.data.reminders;
			} else {
				const toast: ToastSettings = {
					message: `¡ERROR! El recordatorio no se pudo ${result.data.action}ar.
							mensaje:${result.data.error}`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
			loading = false;
			return update({ reset: false });
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
	function updateConfirmation(event: any) {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Actualizar recordatorio`,
			body: `¿Está seguro de querer actualizar este recordatorio?`,
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

<div class="mx-auto w-full lg:w-3/4 my-2">
	<div class="flex flex-row space-x-2 items-center">
		<h2 class="h2 my-4">Información</h2>
		{#if buttonAction !== 'create'}{#if checkPermission(user, 'add_note')}
				<button
					class="btn variant-filled px-6 h-[2rem]"
					on:click={() => {
						buttonAction = 'create';
					}}
				>
					<i class="fa-solid fa-plus"></i>
				</button>
			{/if}
		{/if}
	</div>
</div>
{#if loading}
	<div class="flex flex-row justify-center mt-5">
		<ProgressRadial />
	</div>
{:else}
	<div class="grid grid-cols-[auto_1fr_auto] gap-4 items-center w-full">
		{#if buttonAction === 'create' || !reminders || reminders.length < 1}
			{#if checkPermission(user, 'add_note')}
				<form
					action="?/addReminder"
					method="post"
					class="w-full mx-auto lg:ml-[10rem]"
					use:enhance={handleResult}
				>
					<input type="hidden" name="name" bind:value={user.name} />
					<textarea
						class="textarea w-[40rem] h-[10rem] mx-auto mb-5"
						name="note"
						placeholder="Recordatorio"
					></textarea>

					<div class="flex gap-5">
						<button type="submit" class="btn variant-filled">
							<i class="fa-solid fa-floppy-disk"></i>
						</button>
						{#if reminders && reminders.length > 0}
							<button
								type="button"
								class="btn variant-filled"
								on:click={() => {
									buttonAction = '';
								}}
							>
								<i class="fa-solid fa-arrow-left"></i>
							</button>
						{/if}
					</div>
				</form>
				{/if}
			{:else if buttonAction === 'edit'}
				<form
					action="?/editReminder"
					class="mx-auto lg:ml-[10rem]"
					method="post"
					use:enhance={handleResult}
				>
					<label class="label" for="object">
						<input type="hidden" name="id" bind:value={reminderSelected.id} />
						<input type="hidden" name="name" bind:value={user.name} />
						<textarea
							class="textarea w-[40rem] mx-auto h-[10rem] mb-5"
							name="note"
							placeholder="Recordatorio">{reminderSelected.note}</textarea
						>
						<div class="flex gap-5">
							<button
								type="button"
								class="btn variant-filled"
								on:click={(e) => updateConfirmation(e)}
							>
								<i class="fa-solid fa-floppy-disk"></i>
							</button>
							{#if reminders.length > 0}
								<button
									type="button"
									class="btn variant-filled"
									on:click={() => {
										buttonAction = '';
									}}
								>
									<i class="fa-solid fa-arrow-left"></i>
								</button>
							{/if}
						</div>
					</label>
				</form>
			{:else}
				<div class="w-[3rem]">
					{#if reminders.length > 1}
						<button
							type="button"
							class="h-[3rem] w-[3rem] btn-icon variant-filled"
							on:click={carouselLeft}
						>
							<i class="fa-solid fa-arrow-left" />
						</button>
					{/if}
				</div>

				<div
					bind:this={elemCarousel}
					class="scroll-smooth flex overflow-hidden w-full mx-auto h-auto"
				>
					{#each sortedReminders as reminder}
						<div class="card p-4 flex-none h-auto snap-start items-center w-full">
							<header class="text-xl text-start font-bold py-5 px-2 whitespace-pre-wrap">
								{reminder.note}
							</header>

							<div class="flex justify-between">
								<form action="?/deleteReminder" method="post" use:enhance={handleResult}>
									<input type="hidden" name="id" bind:value={reminder.id} />
									{#if checkPermission(user, 'delete_note')}
										<button
											type="button"
											class="btn-icon variant-filled h-[3rem] w-[3rem]"
											on:click={(e) => deleteConfirmation(reminder.note, e)}
										>
											<i class="fa-solid fa-trash" />
										</button>
									{/if}
								</form>
								<div class="flex flex-col mx-auto">
									<footer class="card-footer text-center font-thin">
										{convertToDate(reminder.date)}
									</footer>
								</div>

								{#if checkPermission(user, 'change_note')}
									<button
										class="btn-icon variant-filled h-[3rem] w-[3rem]"
										on:click={() => {
											buttonAction = 'edit';
											reminderSelected = { note: reminder.note, id: reminder.id };
										}}
									>
										<i class="fa-solid fa-pencil" />
									</button>
								{/if}
							</div>
						</div>
					{/each}
				</div>

				<div class="w-[3rem]">
					{#if reminders.length > 1}
						<button
							type="button"
							class="h-[3rem] w-[3rem] btn-icon variant-filled"
							on:click={carouselRight}
						>
							<i class="fa-solid fa-arrow-right" />
						</button>
					{/if}
				</div>
			{/if}
	</div>
	{#if reminders.length > 1 && buttonAction !== 'create'}
		<div class="flex flex-row justify-center w-full mt-3 space-x-2">
			{#each sortedReminders as reminder}
				<button
					class="rounded-2xl w-[1rem] h-[1rem]"
					class:variant-outline={!reminderSelected || reminderSelected.index !== reminder.index}
					class:variant-filled={reminderSelected && reminderSelected.index === reminder.index}
					on:click={() => {
						reminderSelected = reminder;
						scrollToReminder(reminder);
					}}
				>
				</button>
			{/each}
		</div>
	{/if}
{/if}
