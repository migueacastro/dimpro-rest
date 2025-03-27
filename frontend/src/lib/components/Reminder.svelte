<script lang="ts">
	let elemCarousel: HTMLDivElement;
	//TODO: change with real data
    const reminders = [
    { note: "Don't forget to submit the report!", name: "Alice", date: "2023-10-01" },
    { note: "Team meeting at 3 PM", name: "Bob", date: "2023-10-02" },
    { note: "Lunch with John", name: "Carol", date: "2023-10-03" },
    { note: "Prepare presentation", name: "Dave", date: "2023-10-04" },
    { note: "Don't forget to submit the report!", name: "Alice", date: "2023-10-01" },
    { note: "Team meeting at 3 PM", name: "Bob", date: "2023-10-02" },
    { note: "Lunch with John", name: "Carol", date: "2023-10-03" },
    { note: "Prepare presentation", name: "Dave", date: "2023-10-04" },
    { note: "Don't forget to submit the report!", name: "Alice", date: "2023-10-01" },
    { note: "Team meeting at 3 PM", name: "Bob", date: "2023-10-02" },
    { note: "Lunch with John", name: "Carol", date: "2023-10-03" },
    { note: "Prepare presentation", name: "Dave", date: "2023-10-04" },
    { note: "Don't forget to submit the report!", name: "Alice", date: "2023-10-01" },
    { note: "Team meeting at 3 PM", name: "Bob", date: "2023-10-02" },
    { note: "Lunch with John", name: "Carol", date: "2023-10-03" },
    { note: "Prepare presentation", name: "Dave", date: "2023-10-04" },
  ];

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
</script>

<div class="card p-4 grid grid-cols-[auto_1fr_auto] gap-4 items-center" style="width: 40rem;height: 15rem;">
    <button type="button" class="btn-icon variant-filled" on:click={carouselLeft}>
        <i class="fa-solid fa-arrow-left" />
    </button>
    <div bind:this={elemCarousel} class="scroll-smooth flex overflow-hidden" style="width: 30rem;height: 10rem;">
        {#each reminders as reminder}
        <div class="card flex-none w-full snap-start items-center">
            <header class="card-header text-center font-bold">{reminder.note}</header>
            <div class="p-4 text-center">{reminder.name}</div>
            <footer class="card-footer text-center font-thin">{reminder.date}</footer>
        </div>
        {/each}
    </div>
    <button type="button" class="btn-icon variant-filled" on:click={carouselRight}>
        <i class="fa-solid fa-arrow-right" />
    </button>
</div>