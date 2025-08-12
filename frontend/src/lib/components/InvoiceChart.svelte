<script lang="ts">
	import { LineChart } from '@carbon/charts-svelte';
	import '@carbon/charts-svelte/styles.css';

	export let invoices: any = {};
	let selectedYear: any =
		Object.keys(invoices)[Object.keys(invoices).length - 1] || new Date().getFullYear();

	export let options: any = {
		title: 'Ventas facturadas (en USD)',
		fileDownload: {
			
				fileName: `ventas_facturadas_${selectedYear}.csv`
		},
		axes: {
			bottom: {
				title: 'Fecha',
				scaleType: 'time',
				mapsTo: 'date'
			},
			timeScale: {
				timeInterval: 'monthly'
			},
			left: {
				mapsTo: 'value',
				title: 'Ventas facturadas (en USD)'
			}
		},
		legend: {
			clickable: true
		},
		height: '400px'
	};

	// Destroy chart before creating a new one

	// Handle year changes
</script>

{#if Object.keys(invoices).length > 0}
	<div class="card p-[3rem] mb-[2rem] flex flex-row justify-between shadow-md w-full">
		<div class="flex flex-col w-full">
			<h4 class="h2 font-bold capitalize my-2">Facturas de venta</h4>

			<div class="w-full flex-col items-start">
				<div class="flex flex-col space-y-4 w-fit">
					<label for="year-select" class="h2 text-xl">Seleccione año:</label>
					<select id="year-select" class="select w-[8rem]" bind:value={selectedYear}>
						{#each Object.keys(invoices) as year}
							<option value={year}>{year}</option>
						{/each}
					</select>
				</div>

				<div class="w-full">
					<LineChart data={invoices[selectedYear]} {options} />
				</div>
			</div>
		</div>
	</div>
{/if}
