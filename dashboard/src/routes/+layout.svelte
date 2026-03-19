<script>
	/* Root layout — loads global CSS and wraps all pages */
	import '../app.css';
	let { children } = $props();
</script>

{@render children()}
