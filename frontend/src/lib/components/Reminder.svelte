<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { checkAdminGroup } from '$lib/auth';

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
</script>

{#if reminders && reminders.length > 0}
	{#if buttonAction === 'create'}
		<div class="card p-[2rem] grid grid-cols-[auto_1fr_auto] gap-4 items-center w-full">
			<form action="?/addReminder" method="post">
				<label class="label" for="object">
					<p class="capitalize">NOTA</p>
					<input type="text" class="input mb-5" name="note" placeholder="Nota" />
					<div class="flex gap-5">
					<button type="submit" class="btn variant-filled"
						><i class="fa-solid fa-floppy-disk"></i></button
					>
					<button
					type="button"
					class="btn variant-filled"
					on:click={() => {
						buttonAction = '';
					}}><i class="fa-solid fa-x"></i></button
				>
			</div>
				</label>
			</form>
		</div>
	{:else}
		<div class="card p-[2rem] grid grid-cols-[auto_1fr_auto] gap-4 items-center w-full">
			<button type="button" class="btn-icon variant-filled" on:click={carouselLeft}>
				<i class="fa-solid fa-arrow-left" />
			</button>
			<div bind:this={elemCarousel} class="scroll-smooth flex overflow-hidden w-[60rem] h-[10rem]">
				{#each reminders as reminder}
					<div class="card flex-none w-[60rem] snap-start items-center">
						<header class="card-header text-center font-bold">{reminder.note}</header>
						<div class="p-2 text-center">{reminder.name}</div>
						<footer class="card-footer text-center font-thin">
							{convertToDate(reminder.date)}
						</footer>
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
