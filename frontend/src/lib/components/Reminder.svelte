<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { checkAdminGroup } from '$lib/auth';

	let elemCarousel: HTMLDivElement;
	//TODO: change with real data
	export let reminders: any;
	let date: any;
	export let user;
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
	<div class="card p-[4rem] grid grid-cols-[auto_1fr_auto] gap-4 items-center w-full">
		<button type="button" class="btn-icon variant-filled" on:click={carouselLeft}>
			<i class="fa-solid fa-arrow-left" />
		</button>
		<div bind:this={elemCarousel} class="scroll-smooth flex overflow-hidden w-[30rem] h-[15rem]">
			{#each reminders as reminder}
				<div class="card flex-none w-full snap-start items-center">
					<header class="card-header text-center font-bold">{reminder.note}</header>
					<div class="p-4 text-center">{reminder.name}</div>
					<footer class="card-footer text-center font-thin">{convertToDate(reminder.date)}</footer>
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
					console.log('whoosh');
				}}
			>
				<i class="fa-solid fa-floppy-disk"></i>
			</button>
		{/if}
	</div>
{/if}
