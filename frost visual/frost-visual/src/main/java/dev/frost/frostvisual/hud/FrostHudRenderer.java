package dev.frost.frostvisual.hud;

import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import dev.frost.frostvisual.config.FrostConfig;
import dev.frost.frostvisual.util.RenderUtil;

/**
 * Renders:
 *  • Frost watermark (top-left)
 *  • Target HUD    (centre-bottom)
 *  • Aurora overlay (full-screen, shader-based)
 *  • Snow particle overlay
 */
public class FrostHudRenderer {

    public static void register() {
        HudRenderCallback.EVENT.register(FrostHudRenderer::onHudRender);
    }

    private static void onHudRender(DrawContext ctx, float tickDelta) {
        MinecraftClient mc = MinecraftClient.getInstance();
        if (mc.player == null || !FrostConfig.enabled) return;

        if (FrostConfig.watermark)  renderWatermark(ctx, mc);
        if (FrostConfig.targetHud)  renderTargetHud(ctx, mc);
        if (FrostConfig.auroraEnabled) renderAuroraOverlay(ctx, mc, tickDelta);
    }

    // ── Watermark ─────────────────────────────────────────────────────────────
    private static void renderWatermark(DrawContext ctx, MinecraftClient mc) {
        String text = "§bFrost Visual §7v1.0.0";
        ctx.drawTextWithShadow(
            mc.textRenderer, text,
            FrostConfig.watermarkX, FrostConfig.watermarkY,
            0xFFFFFFFF
        );
        // Decorative ice-blue underline
        int w = mc.textRenderer.getWidth(text);
        ctx.fill(
            FrostConfig.watermarkX, FrostConfig.watermarkY + 10,
            FrostConfig.watermarkX + w, FrostConfig.watermarkY + 11,
            0xFF4FC3F7
        );
    }

    // ── Target HUD ────────────────────────────────────────────────────────────
    private static void renderTargetHud(DrawContext ctx, MinecraftClient mc) {
        if (!(mc.targetedEntity instanceof LivingEntity target)) return;

        int sw = mc.getWindow().getScaledWidth();
        int sy = mc.getWindow().getScaledHeight();
        int x  = sw / 2 - 51;
        int y  = sy - 60;

        // Background panel
        ctx.fill(x - 2, y - 2, x + 104, y + 22, 0xAA000000);
        // Border
        RenderUtil.drawBorder(ctx, x - 2, y - 2, 108, 26, 0xFF4FC3F7, 1);

        // Entity name
        String name = target.getName().getString();
        ctx.drawTextWithShadow(mc.textRenderer, "§b" + name, x + 2, y + 2, 0xFFFFFFFF);

        // Health bar
        if (FrostConfig.targetHudBar) {
            float hp    = target.getHealth();
            float maxHp = target.getMaxHealth();
            float pct   = hp / maxHp;

            ctx.fill(x, y + 13, x + 100, y + 18, 0xFF333333);          // bg
            ctx.fill(x, y + 13, x + (int)(100 * pct), y + 18,          // fill
                     FrostConfig.targetHudColor);
            // HP text
            String hpTxt = String.format("%.1f / %.1f", hp, maxHp);
            ctx.drawTextWithShadow(mc.textRenderer, hpTxt, x + 2, y + 13, 0xFFFFFFFF);
        }
    }

    // ── Aurora overlay (full-screen frost tint) ───────────────────────────────
    private static void renderAuroraOverlay(DrawContext ctx, MinecraftClient mc, float td) {
        if (!mc.player.isSubmergedInWater() && mc.player.getAir() >= 0) {
            int sw = mc.getWindow().getScaledWidth();
            int sh = mc.getWindow().getScaledHeight();
            // Soft vertical gradient: ice-blue top → transparent bottom
            RenderUtil.drawVerticalGradient(ctx, 0, 0, sw, sh / 3,
                0x334FC3F7, 0x00000000);
        }
    }
}
