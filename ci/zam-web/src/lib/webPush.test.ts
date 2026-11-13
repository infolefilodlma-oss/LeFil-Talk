import { describe, expect, it, vi } from "vitest";

vi.mock("@capacitor/core", () => ({
    Capacitor: { isNativePlatform: () => false },
}));

import { initWebPush, webPushConfigured } from "$lib/webPush";

describe("Le Fil Talk configured web push build", () => {
    it("has an effective public VAPID key", () => {
        expect(webPushConfigured()).toBe(true);
    });

    it("does not register when browser push APIs are absent", async () => {
        const setPusher = vi.fn();
        await initWebPush({ setPusher } as never);
        expect(setPusher).not.toHaveBeenCalled();
    });
});
