<script lang="ts">
import { goto } from "$app/navigation";
import { apiURL } from "$lib/api_url";
import { fetchLogin } from "$lib/auth";
import Cookies from 'js-cookie';
import { authenticate } from "$lib/auth";

interface FormErrors {
    email: any;
    password: any;
}
let errors: FormErrors = {email: null, password: null};

let email = "";
let password = "";

async function handleLogin() {
    let formData = {
        "email": email,
        "password":password
    }
    const response = await fetchLogin(formData);
    const data = await response.json();
    if (response.ok) {
        const token = data?.token;
        Cookies.set('token', token, {expires: 365, secure: true});
        
        
        await authenticate();
        goto('/');
    } else {
        errors = data;
    }
}
</script>

<div class="flex flex-col">

<ol class="breadcrumb mb-[3rem]">
    <li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
    <li class="crumb-separator" aria-hidden>/</li>
    <li class="crumb">Vendedor</li>
</ol>
                
<form>
    <h3 class="text-4xl mb-[2rem]">Iniciar Sesión</h3>
    <input class="input my-2" title="Email" type="text" placeholder="Email" bind:value={email}/>
    
    {#if errors.email}
    <div class="card variant-ghost-error p-2 text-sm text-left">
        <ul>
            {#each errors?.email as error}
                <li>{error}</li>
            {/each}
        </ul>
    </div>
    {/if}

    <input class="input my-2" title="Contraseña" type="password" placeholder="Contraseña" bind:value={password}/>
    {#if errors.password}
    <div class="card variant-ghost-error p-2 text-sm text-left">
        <ul>
            {#each errors?.password as error}
                <li>{error}</li>
            {/each}
        </ul>
    </div>
    {/if}
    <button class="btn btn-xl variant-filled-primary my-2 w-full shadow-xl" on:click={handleLogin}>Iniciar Sesión</button>
    <p class="mt-4">¿Eres nuevo vendedor? <a class="anchor no-underline" href="/register">Registrarse</a></p>
</form>
</div>
