<script lang="ts">
	import '../app.css';
	import { afterNavigate, goto } from '$app/navigation';

	let { children } = $props();
</script>

<header class="sticky top-0 bg-surface-950 shadow-[0px_5px_5px_0px_rgba(17,17,17,0.8)]">
	<div class="h-2"></div>
	<div class="flex justify-center">
		<div class="text-3xl">
			<a href="/">NutriGuard</a>
		</div>
	</div>
	<div class=" mt-2 h-0.5 primary-500"></div>
</header>

<main class="px-72 mt-26">
	{@render children()}
</main>

<footer class="px-72 pt-64 pb-16 justify-center">
	<div class="flex justify-between">
		<div>
			© 2025 Nils Ostertag
		</div>
		<a href="/#">
			AGBs
		</a>
		<a href="/#">
			Impressum
		</a>
		<a href="/#">
			Datenschutz
		</a>
		<a href="/#">
			Kontakt
		</a>
	</div>
	<div class="mt-32 sticky bottom-0 flex justify-center">
		<div class="text-xl">STICKY BOTTOM</div>
	</div>
</footer>