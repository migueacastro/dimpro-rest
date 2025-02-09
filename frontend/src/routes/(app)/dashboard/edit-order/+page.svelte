<title>Editar Pedidos</title>

<script lang="ts">
  
  interface Item {
    id:number;
    item:String;
    reference:String;
    quantity:number;
    availability:number;
    price:number;
    cost:number;
    index:number;
  }

  let items: Array<Item> = [
    {
      'id': 1,
      'item': 'Bombillo',
      'reference': 'BOMTL20',  
      'quantity': 200,
      'availability': 5104,
      'price': 6.5,
      'cost': 245.4,
      'index': 0,
    }
  ];

  function addRow() {
  // carefull here, reactiviy works this way
    let index = items[items.length - 1].index + 1;
    let newRow = {
      'id': 7,
      'item': 'Bombillo',
      'reference': 'AAA',  
      'quantity': 200,
      'availability': 5104,
      'price': 6.5,
      'cost': 245.4,
      'index': index
    };
    
    items = [...items,newRow]; // Here the array value is changed to another array with different  content
    //items.push(newRow); // You see? this just updates the content, not the value
  }

  function removeRow(index:number) {
    items = items.filter((item) => item.index !== index)
    updateIndex();
    //items.splice(index,1); // this would work well if instead of id, it would be the current index inside of the items array
  } 
  
 
  function updateIndex() {
    items.forEach((item, index) => {
      item.index = index;
    })
  }


  // id does not depend on the table, it merely depends on the item
</script>

 

<h1 class="h2 my-4">
  Editar Pedido
</h1>
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
					<td>{row.item}</td>
					<td>{row.reference}</td>
					<td>{row.quantity}</td>

					<td>{row.availability}</td>
					<td>{row.price}</td>
					<td>{row.cost}</td>
          <td class="flex flex-row">
            <button class="btn variant-filled" on:click={() => removeRow(row.index)}>
              <i class="fa-solid fa-trash"></i>
            </button>
            <button class="btn ml-2 variant-filled" on:click={addRow} >
              <i class="fa-solid fa-plus"></i>
            </button>
          </td>
				</tr>
			{/each}
		</tbody>
		<tfoot>
			<tr>
				<th colspan="3">Calculated Total Weight</th>
				<td>Total: 45</td>
			</tr>
		</tfoot>
	</table>
</div>



