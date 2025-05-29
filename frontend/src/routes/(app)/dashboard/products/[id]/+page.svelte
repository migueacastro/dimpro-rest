<script lang="ts">
	export let data;
	const { product } = data;
</script>

<p class="h2 text-center">Información del producto: {product.item}</p>

<div class="card my-3 p-10 text-start lg:w-[75%] space-y-6 mx-auto">
	<p>ID del producto: {product.id}</p>
	<p>Referencia del producto: {product.reference}</p>
	<p>Nombre del producto: {product.item}</p>
	<p>Cantidad disponible: {product.available_quantity}</p>
</div>
