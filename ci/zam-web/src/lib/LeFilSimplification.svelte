<script lang="ts">
	// Le Fil Talk Phase 2A - Interface Simplification
	// Applies UI simplification rules at runtime.
	// Hides non-essential features while preserving security alerts and main functions.

	import { onMount } from 'svelte';

	function applyLeFilSimplifications() {
		// Hide debug and plugins settings tabs
		const debugElements = document.querySelectorAll(
			'[data-settings-tab="debug"], [data-settings-tab="plugins"], [data-settings-tab="rich-presence"]'
		);
		debugElements.forEach(el => {
			(el as HTMLElement).style.display = 'none';
		});

		// Hide from settings nav
		const navItems = document.querySelectorAll(
			'.settings-nav-item[data-tab-id="debug"], .settings-nav-item[data-tab-id="plugins"], .settings-nav-item[data-tab-id="rich-presence"]'
		);
		navItems.forEach(el => {
			(el as HTMLElement).style.display = 'none';
		});

		// Ensure security alerts remain visible
		const alerts = document.querySelectorAll('[role="alert"], .alert, .banner, .health-banner, .security-banner');
		alerts.forEach(el => {
			(el as HTMLElement).style.display = '';
		});
	}

	onMount(() => {
		// Apply on mount
		applyLeFilSimplifications();

		// Re-apply after DOM changes (for dynamic tabs)
		const observer = new MutationObserver(() => {
			applyLeFilSimplifications();
		});

		observer.observe(document.body, {
			childList: true,
			subtree: true,
			attributes: false
		});

		return () => observer.disconnect();
	});
</script>

<!-- This component is mounted in AppShell to apply Le Fil simplifications -->
