import { describe, expect, it, vi } from "vitest";

vi.mock("@capacitor/core", () => ({
    Capacitor: { isNativePlatform: () => false },
}));

import { initWebPush, webPushConfigured } from "$lib/webPush";

describe("web push disabled build", () => {
    it("has no effective VAPID key", () => {
        expect(webPushConfigured()).toBe(false);
    });

    it("cannot register a third-party web pusher", async () => {
        const setPusher = vi.fn();
        await initWebPush({ setPusher } as never);
        expect(setPusher).not.toHaveBeenCalled();
    });
});
