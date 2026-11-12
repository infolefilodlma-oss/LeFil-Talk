import { describe, it, expect } from 'vitest';
import { SETTINGS_GROUPS, SETTINGS_TABS, DEFAULT_SETTINGS_TAB } from './settingsNav';

describe('settingsNav - Phase 2A UI Simplification', () => {
	it('should have exactly 3 core groups', () => {
		expect(SETTINGS_GROUPS).toHaveLength(3);
	});

	it('should have Account group as first', () => {
		expect(SETTINGS_GROUPS[0].tabs.map(t => t.id)).toContain('account');
		expect(SETTINGS_GROUPS[0].tabs.map(t => t.id)).toContain('security');
		expect(SETTINGS_GROUPS[0].tabs.map(t => t.id)).toContain('privacy');
	});

	it('should have App group as second (main features)', () => {
		const appTabs = SETTINGS_GROUPS[1].tabs.map(t => t.id);
		expect(appTabs).toContain('notifications');
		expect(appTabs).toContain('messages-media');
		expect(appTabs).toContain('voice');
		expect(appTabs).toContain('appearance');
	});

	it('should have Advanced group as third (hidden by default)', () => {
		const advancedTabs = SETTINGS_GROUPS[2].tabs.map(t => t.id);
		expect(advancedTabs).toContain('debug');
		expect(advancedTabs).toContain('plugins');
		expect(advancedTabs).toContain('server');
		expect(advancedTabs).toContain('about');
	});

	it('should preserve all standard tabs (Phase 1 unchanged)', () => {
		const allIds = SETTINGS_TABS.map(t => t.id);
		expect(allIds).toContain('account');
		expect(allIds).toContain('security');
		expect(allIds).toContain('privacy');
		expect(allIds).toContain('debug');
		expect(allIds).toContain('plugins');
		expect(allIds).toContain('appearance');
		expect(allIds).toContain('notifications');
		expect(allIds).toContain('voice');
	});

	it('should have accessible Advanced settings despite hiding', () => {
		const advancedGroup = SETTINGS_GROUPS[2];
		expect(advancedGroup.tabs.length).toBeGreaterThan(0);
		// All tabs remain in the group; AppSettings toggles visibility
		advancedGroup.tabs.forEach(tab => {
			expect(tab.id).toBeDefined();
			expect(tab.label).toBeDefined();
		});
	});

	it('should preserve default tab selection', () => {
		expect(DEFAULT_SETTINGS_TAB).toBe('account');
	});

	it('should maintain tab lookups', () => {
		const allTabs = SETTINGS_TABS;
		expect(allTabs.length).toBeGreaterThan(10);
		// Verify no duplicate IDs
		const ids = allTabs.map(t => t.id);
		const uniqueIds = new Set(ids);
		expect(uniqueIds.size).toBe(ids.length);
	});
});
