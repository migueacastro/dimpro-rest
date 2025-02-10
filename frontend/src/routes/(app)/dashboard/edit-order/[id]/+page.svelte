<script lang="ts">
	import { checkAdminGroup } from '$lib/auth';
	import { user } from '../../../../../stores/stores';

	export let data;
	interface Item {
		id: number;
		item: String;
		reference: String;
		quantity: number;
		availability: number;
		price: number;
		cost: number;
		index: number;
	}

	let items: Array<Item> = [
		{
			id: 1,
			item: 'Bombillo',
			reference: 'BOMTL20',
			quantity: 200,
			availability: 5104,
			price: 6.5,
			cost: 245.4,
			index: 0
		}
	];

	function addRow() {
		// carefull here, reactiviy works this way
		let index = items[items.length - 1].index + 1;
		let newRow = {
			id: 7,
			item: 'Bombillo',
			reference: 'AAA',
			quantity: 200,
			availability: 5104,
			price: 6.5,
			cost: 245.4,
			index: index
		};

		items = [...items, newRow]; // Here the array value is changed to another array with different  content
		//items.push(newRow); // You see? this just updates the content, not the value
	}

	function removeRow(index: number) {
		items = items.filter((item) => item.index !== index);
		updateIndex();
		//items.splice(index,1); // this would work well if instead of id, it would be the current index inside of the items array
	}

	function updateIndex() {
		items.forEach((item, index) => {
			item.index = index;
		});
	}

	// id does not depend on the table, it merely depends on the item
</script>

<title>Editar Ordenes</title>

<h1 class="h2 my-4">
	Editar Pedido #{data.id}
</h1>

<div class="flex flex-row justify-between">
	<h3 class="h3 my-[2rem]">Items: {items.length}</h3>
	<div class="flex flex-col">
		<label for="" class="h4 my-2">Tipo de precio</label>
		<select class="select" name="pricetype" id="pricetype"> </select>
	</div>
</div>
<!-- Responsive Container (recommended) -->
<div class="table-container">
	<!-- Native Table Element -->
	<table class="table table-hover">
		<thead>
			<tr>
				<th>ID</th>
				<th>Item</th>
				<th>Referencia</th>
				<th>Cantidad</th>
				<th>Disponibilidad</th>
				<th>Precio</th>
				<th>Costo</th>
				<th></th>
			</tr>
		</thead>
		<tbody>
			{#each items as row}
				<tr>
					<td>{row.id}</td>
					<td><input type="text" class="input" /></td>
					<td>{row.reference}</td>
					<td><input type="number" class="input" min="1" /></td>
					<td>{row.availability}</td>
					<td>{row.price}</td>
					<td>{row.cost}</td>
					<td class="flex flex-row">
						<button class="btn variant-filled" on:click={() => removeRow(row.index)}>
							<i class="fa-solid fa-trash"></i>
						</button>
						<button class="btn ml-2 variant-filled" on:click={addRow}>
							<i class="fa-solid fa-plus"></i>
						</button>
					</td>
				</tr>
			{/each}
		</tbody>
		<tfoot>
			<tr>
				<th colspan="3">Totales</th>
				<td class="font-bold">45</td>
				<td></td>
				<td class="font-bold">6.5</td>
				<td class="font-bold">245.4</td>
				<td></td>
			</tr>
		</tfoot>
	</table>
	<div class="flex flex-row justify-center mt-[2rem]">
		<button class="btn ml-2 variant-filled" on:click={addRow}>
			<i class="fa-solid fa-plus mr-2"></i> Añadir item
		</button>
		<button class="btn ml-2 variant-filled" on:click={addRow}>
			<i class="fa-solid fa-floppy-disk mr-2"></i> Guardar
		</button>
		<button class="btn ml-2 variant-filled" on:click={addRow}>
			<i class="fa-solid fa-trash mr-2"></i> Eliminar Pedido
		</button>
	</div>
	<div class="flex justify-end flex-row">
		<h1 class="h2 mt-[2rem]">Total: 9.40$</h1>
	</div>
	<div class="card p-[2rem] mt-[2rem]">
		<h1 class="h3">Recordatorio</h1>
		<p class="p">Texto de ejemplo</p>
		{#if checkAdminGroup($user)}
			<button class="btn mt-[2rem] variant-filled" on:click={addRow}>
				<i class="fa-solid fa-floppy-disk"></i>
			</button>
		{/if}
	</div>
</div>
