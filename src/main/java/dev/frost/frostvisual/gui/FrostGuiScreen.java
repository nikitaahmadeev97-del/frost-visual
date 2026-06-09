package dev.frost.frostvisual.gui;

import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.text.Text;
import dev.frost.frostvisual.config.FrostConfig;
import dev.frost.frostvisual.util.RenderUtil;

/**
 * Main configuration screen — opened via Right Shift.
 *
 * Layout (800 × 600-ish):
 *   ┌──────────────────────────────────────┐
 *   │  ❄  FROST VISUAL  v1.0.0              │
 *   │  ─────────────────────────────────   │
 *   │  [✓] Frost Overlay   intensity ──●  │
 *   │  [✓] Aurora Effect               │
 *   │  [✓] Snow Particles  count  ──●  │
 *   │  [ ] Motion Blur     strength ──● │
 *   │  [✓] Chromatic Ab.   strength ──● │
 *   │  ─────────────────────────────────  │
 *   │  TARGET HUD                         │
 *   │  [✓] Enable  [✓] HP Bar  [✓] Armor │
 *   │  ─────────────────────────────────  │
 *   │  [✓] Watermark                      │
 *   │                         [  Close  ] │
 *   └──────────────────────────────────────┘
 */
public class FrostGuiScreen extends Screen {

    private static final int BG     = 0xDD0A1628;  // deep navy
    private static final int ACCENT = 0xFF4FC3F7;  // ice blue
    private static final int PANEL  = 0xAA112244;

    public FrostGuiScreen() {
        super(Text.literal("Frost Visual"));
    }

    @Override
    protected void init() {
        int cx = width / 2;
        int y  = height / 2 - 60;

        // Toggle buttons (simple on/off)
        addDrawableChild(ButtonWidget.builder(
            togLabel("Frost Overlay", FrostConfig.frostOverlay),
            btn -> { FrostConfig.frostOverlay = !FrostConfig.frostOverlay;
                      btn.setMessage(togLabel("Frost Overlay", FrostConfig.frostOverlay)); })
            .dimensions(cx - 110, y + 30, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Aurora", FrostConfig.auroraEnabled),
            btn -> { FrostConfig.auroraEnabled = !FrostConfig.auroraEnabled;
                      btn.setMessage(togLabel("Aurora", FrostConfig.auroraEnabled)); })
            .dimensions(cx + 10, y + 30, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Snow", FrostConfig.snowParticles),
            btn -> { FrostConfig.snowParticles = !FrostConfig.snowParticles;
                      btn.setMessage(togLabel("Snow", FrostConfig.snowParticles)); })
            .dimensions(cx - 110, y + 55, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Motion Blur", FrostConfig.motionBlur),
            btn -> { FrostConfig.motionBlur = !FrostConfig.motionBlur;
                      btn.setMessage(togLabel("Motion Blur", FrostConfig.motionBlur)); })
            .dimensions(cx + 10, y + 55, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Chrom. Ab.", FrostConfig.chromaticAb),
            btn -> { FrostConfig.chromaticAb = !FrostConfig.chromaticAb;
                      btn.setMessage(togLabel("Chrom. Ab.", FrostConfig.chromaticAb)); })
            .dimensions(cx - 110, y + 80, 100, 20).build());

        // Target HUD
        addDrawableChild(ButtonWidget.builder(
            togLabel("Target HUD", FrostConfig.targetHud),
            btn -> { FrostConfig.targetHud = !FrostConfig.targetHud;
                      btn.setMessage(togLabel("Target HUD", FrostConfig.targetHud)); })
            .dimensions(cx - 110, y + 115, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("HP Bar", FrostConfig.targetHudBar),
            btn -> { FrostConfig.targetHudBar = !FrostConfig.targetHudBar;
                      btn.setMessage(togLabel("HP Bar", FrostConfig.targetHudBar)); })
            .dimensions(cx + 10, y + 115, 100, 20).build());

        // Watermark
        addDrawableChild(ButtonWidget.builder(
            togLabel("Watermark", FrostConfig.watermark),
            btn -> { FrostConfig.watermark = !FrostConfig.watermark;
                      btn.setMessage(togLabel("Watermark", FrostConfig.watermark)); })
            .dimensions(cx - 50, y + 145, 100, 20).build());

        // Close
        addDrawableChild(ButtonWidget.builder(
            Text.literal("Close"),
            btn -> { FrostConfig.save(); close(); })
            .dimensions(cx - 40, y + 180, 80, 20).build());
    }

    @Override
    public void render(DrawContext ctx, int mx, int my, float delta) {
        // Dark background
        ctx.fill(0, 0, width, height, BG);
        // Centre panel
        int px = width / 2 - 130, py = height / 2 - 110;
        ctx.fill(px, py, px + 260, py + 220, PANEL);
        RenderUtil.drawBorder(ctx, px, py, 260, 220, ACCENT, 1);

        // Title
        String title = "❄  FROST VISUAL  v1.0.0";
        ctx.drawCenteredTextWithShadow(textRenderer, "§b" + title, width / 2, py + 8, 0xFFFFFFFF);
        // Divider
        ctx.fill(px + 10, py + 18, px + 250, py + 19, ACCENT);

        // Section labels
        ctx.drawTextWithShadow(textRenderer, "§7VISUALS",
            width / 2 - 120, height / 2 - 68, 0xFFAAAAAA);
        ctx.drawTextWithShadow(textRenderer, "§7TARGET HUD",
            width / 2 - 120, height / 2 - 35, 0xFFAAAAAA);
        ctx.drawTextWithShadow(textRenderer, "§7DISPLAY",
            width / 2 - 120, height / 2 - 5, 0xFFAAAAAA);

        super.render(ctx, mx, my, delta);
    }

    @Override
    public boolean shouldPause() { return false; }

    private static Text togLabel(String name, boolean val) {
        return Text.literal((val ? "§a✔ " : "§c✘ ") + "§f" + name);
    }
}
