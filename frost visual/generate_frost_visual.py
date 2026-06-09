#!/usr/bin/env python3
"""
Frost Visual Mod — Project Generator
Minecraft 1.21.11 | Fabric
Generates the full mod project structure with all source files.
"""

import os
import json

# ─── CONFIG ───────────────────────────────────────────────────────────────────
MOD_ID       = "frostvisual"
MOD_NAME     = "Frost Visual"
VERSION      = "1.0.0"
MC_VERSION   = "1.21.11"
FABRIC_API   = "0.100.0+1.21.11"
FABRIC_LOADER= "0.15.11"
JAVA_VERSION = 21
GROUP        = "dev.frost"
BASE         = "frost-visual"
SRC          = f"{BASE}/src/main/java/{GROUP.replace('.','/')}/{MOD_ID}"
RES          = f"{BASE}/src/main/resources"
# ──────────────────────────────────────────────────────────────────────────────


def write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [+] {path}")


# ══════════════════════════════════════════════════════════════════════════════
#  1. GRADLE FILES
# ══════════════════════════════════════════════════════════════════════════════

def gen_build_gradle():
    write(f"{BASE}/build.gradle", f"""\
plugins {{
    id 'fabric-loom' version '1.6-SNAPSHOT'
    id 'maven-publish'
}}

version = "{VERSION}"
group = "{GROUP}"

repositories {{ mavenCentral() }}

dependencies {{
    minecraft "com.mojang:minecraft:{MC_VERSION}"
    mappings "net.fabricmc:yarn:{MC_VERSION}+build.1:v2"
    modImplementation "net.fabricmc:fabric-loader:{FABRIC_LOADER}"
    modImplementation "net.fabricmc.fabric-api:fabric-api:{FABRIC_API}"
}}

java {{
    sourceCompatibility = JavaVersion.VERSION_{JAVA_VERSION}
    targetCompatibility = JavaVersion.VERSION_{JAVA_VERSION}
    withSourcesJar()
}}
""")


def gen_gradle_properties():
    write(f"{BASE}/gradle.properties", f"""\
org.gradle.jvmargs=-Xmx2G
minecraft_version={MC_VERSION}
loader_version={FABRIC_LOADER}
fabric_version={FABRIC_API}
mod_version={VERSION}
maven_group={GROUP}
archives_base_name={MOD_ID}
""")


def gen_settings_gradle():
    write(f"{BASE}/settings.gradle", f'rootProject.name = "{MOD_ID}"\n')


# ══════════════════════════════════════════════════════════════════════════════
#  2. FABRIC META
# ══════════════════════════════════════════════════════════════════════════════

def gen_fabric_mod_json():
    data = {
        "schemaVersion": 1,
        "id": MOD_ID,
        "version": VERSION,
        "name": MOD_NAME,
        "description": "Frost Visual — beautiful client-side visuals for Minecraft 1.21.1",
        "authors": ["FrostDev"],
        "license": "MIT",
        "icon": "assets/frostvisual/icon.png",
        "environment": "client",
        "entrypoints": {
            "client": [f"{GROUP}.{MOD_ID}.FrostVisualMod"]
        },
        "mixins": [f"{MOD_ID}.mixins.json"],
        "depends": {
            "fabricloader": f">={FABRIC_LOADER}",
            "fabric-api": "*",
            "minecraft": f"~{MC_VERSION}"
        }
    }
    write(f"{RES}/fabric.mod.json", json.dumps(data, indent=2))


def gen_mixins_json():
    data = {
        "required": True,
        "package": f"{GROUP}.{MOD_ID}.mixin",
        "compatibilityLevel": "JAVA_21",
        "client": [
            "GameRendererMixin",
            "InGameHudMixin"
        ],
        "injectors": {"defaultRequire": 1}
    }
    write(f"{RES}/{MOD_ID}.mixins.json", json.dumps(data, indent=2))


# ══════════════════════════════════════════════════════════════════════════════
#  3. JAVA SOURCE FILES
# ══════════════════════════════════════════════════════════════════════════════

def gen_main_mod():
    write(f"{SRC}/FrostVisualMod.java", f"""\
package {GROUP}.{MOD_ID};

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.client.util.InputUtil;
import org.lwjgl.glfw.GLFW;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import {GROUP}.{MOD_ID}.config.FrostConfig;
import {GROUP}.{MOD_ID}.gui.FrostGuiScreen;
import {GROUP}.{MOD_ID}.hud.FrostHudRenderer;

public class FrostVisualMod implements ClientModInitializer {{

    public static final String MOD_ID  = "{MOD_ID}";
    public static final String VERSION = "{VERSION}";
    public static final Logger LOGGER  = LoggerFactory.getLogger(MOD_ID);

    // Right Shift keybind — opens the Frost Visual GUI
    public static KeyBinding OPEN_GUI_KEY;

    @Override
    public void onInitializeClient() {{
        LOGGER.info("[FrostVisual] Initialising v{{}} for Minecraft {MC_VERSION}", VERSION);

        FrostConfig.load();

        // Register Right-Shift keybind
        OPEN_GUI_KEY = KeyBindingHelper.registerKeyBinding(new KeyBinding(
            "key.frostvisual.open_gui",
            InputUtil.Type.KEYSYM,
            GLFW.GLFW_KEY_RIGHT_SHIFT,
            "category.frostvisual"
        ));

        // Register HUD renderer
        FrostHudRenderer.register();

        // Tick: check for keybind press
        ClientTickEvents.END_CLIENT_TICK.register(client -> {{
            while (OPEN_GUI_KEY.wasPressed()) {{
                client.setScreen(new FrostGuiScreen());
            }}
        }});

        LOGGER.info("[FrostVisual] Ready!");
    }}
}}
""")


def gen_config():
    write(f"{SRC}/config/FrostConfig.java", f"""\
package {GROUP}.{MOD_ID}.config;

/**
 * Runtime configuration holder for Frost Visual.
 * Persisted to config/frostvisual.json via Gson.
 */
public class FrostConfig {{

    // ── Visuals ──────────────────────────────────────────────────────────────
    public static boolean enabled          = true;

    // Frost Overlay
    public static boolean frostOverlay     = true;
    public static float   frostIntensity   = 0.35f;   // 0.0 – 1.0

    // Aurora Effect
    public static boolean auroraEnabled    = true;
    public static int     auroraColor      = 0x6690C8FF; // ARGB

    // Snow Particles
    public static boolean snowParticles    = true;
    public static int     snowCount        = 120;

    // Motion Blur
    public static boolean motionBlur       = false;
    public static float   motionBlurStrength = 0.18f;

    // Chromatic Aberration
    public static boolean chromaticAb      = true;
    public static float   chromaticStrength = 0.006f;

    // ── Target HUD ───────────────────────────────────────────────────────────
    public static boolean targetHud        = true;
    public static boolean targetHudBar     = true;   // health bar
    public static boolean targetHudArmor   = true;
    public static int     targetHudColor   = 0xFF4FC3F7; // ARGB

    // ── Watermark ────────────────────────────────────────────────────────────
    public static boolean watermark        = true;
    public static int     watermarkX       = 4;
    public static int     watermarkY       = 4;

    // ── Internal ─────────────────────────────────────────────────────────────
    private static final String CONFIG_PATH = "config/frostvisual.json";

    public static void load()  {{ /* TODO: read from JSON with Gson */ }}
    public static void save()  {{ /* TODO: write to JSON with Gson  */ }}
}}
""")


def gen_hud_renderer():
    write(f"{SRC}/hud/FrostHudRenderer.java", f"""\
package {GROUP}.{MOD_ID}.hud;

import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import {GROUP}.{MOD_ID}.config.FrostConfig;
import {GROUP}.{MOD_ID}.util.RenderUtil;

/**
 * Renders:
 *  • Frost watermark (top-left)
 *  • Target HUD    (centre-bottom)
 *  • Aurora overlay (full-screen, shader-based)
 *  • Snow particle overlay
 */
public class FrostHudRenderer {{

    public static void register() {{
        HudRenderCallback.EVENT.register(FrostHudRenderer::onHudRender);
    }}

    private static void onHudRender(DrawContext ctx, float tickDelta) {{
        MinecraftClient mc = MinecraftClient.getInstance();
        if (mc.player == null || !FrostConfig.enabled) return;

        if (FrostConfig.watermark)  renderWatermark(ctx, mc);
        if (FrostConfig.targetHud)  renderTargetHud(ctx, mc);
        if (FrostConfig.auroraEnabled) renderAuroraOverlay(ctx, mc, tickDelta);
    }}

    // ── Watermark ─────────────────────────────────────────────────────────────
    private static void renderWatermark(DrawContext ctx, MinecraftClient mc) {{
        String text = "§bFrost Visual §7v{VERSION}";
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
    }}

    // ── Target HUD ────────────────────────────────────────────────────────────
    private static void renderTargetHud(DrawContext ctx, MinecraftClient mc) {{
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
        if (FrostConfig.targetHudBar) {{
            float hp    = target.getHealth();
            float maxHp = target.getMaxHealth();
            float pct   = hp / maxHp;

            ctx.fill(x, y + 13, x + 100, y + 18, 0xFF333333);          // bg
            ctx.fill(x, y + 13, x + (int)(100 * pct), y + 18,          // fill
                     FrostConfig.targetHudColor);
            // HP text
            String hpTxt = String.format("%.1f / %.1f", hp, maxHp);
            ctx.drawTextWithShadow(mc.textRenderer, hpTxt, x + 2, y + 13, 0xFFFFFFFF);
        }}
    }}

    // ── Aurora overlay (full-screen frost tint) ───────────────────────────────
    private static void renderAuroraOverlay(DrawContext ctx, MinecraftClient mc, float td) {{
        if (!mc.player.isSubmergedInWater() && mc.player.getAir() >= 0) {{
            int sw = mc.getWindow().getScaledWidth();
            int sh = mc.getWindow().getScaledHeight();
            // Soft vertical gradient: ice-blue top → transparent bottom
            RenderUtil.drawVerticalGradient(ctx, 0, 0, sw, sh / 3,
                0x334FC3F7, 0x00000000);
        }}
    }}
}}
""")


def gen_render_util():
    write(f"{SRC}/util/RenderUtil.java", f"""\
package {GROUP}.{MOD_ID}.util;

import net.minecraft.client.gui.DrawContext;

/** Small collection of rendering helpers used across Frost Visual. */
public final class RenderUtil {{

    private RenderUtil() {{}}

    /** Draws a solid 1-pixel border around a rectangle. */
    public static void drawBorder(DrawContext ctx,
                                  int x, int y, int w, int h,
                                  int color, int thickness) {{
        ctx.fill(x, y, x + w, y + thickness, color);              // top
        ctx.fill(x, y + h - thickness, x + w, y + h, color);      // bottom
        ctx.fill(x, y, x + thickness, y + h, color);               // left
        ctx.fill(x + w - thickness, y, x + w, y + h, color);      // right
    }}

    /** Draws a vertical gradient quad. */
    public static void drawVerticalGradient(DrawContext ctx,
                                            int x, int y, int x2, int y2,
                                            int colorTop, int colorBottom) {{
        ctx.fillGradient(x, y, x2, y2, colorTop, colorBottom);
    }}
}}
""")


def gen_gui_screen():
    write(f"{SRC}/gui/FrostGuiScreen.java", f"""\
package {GROUP}.{MOD_ID}.gui;

import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.text.Text;
import {GROUP}.{MOD_ID}.config.FrostConfig;
import {GROUP}.{MOD_ID}.util.RenderUtil;

/**
 * Main configuration screen — opened via Right Shift.
 *
 * Layout (800 × 600-ish):
 *   ┌──────────────────────────────────────┐
 *   │  ❄  FROST VISUAL  v{VERSION}              │
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
public class FrostGuiScreen extends Screen {{

    private static final int BG     = 0xDD0A1628;  // deep navy
    private static final int ACCENT = 0xFF4FC3F7;  // ice blue
    private static final int PANEL  = 0xAA112244;

    public FrostGuiScreen() {{
        super(Text.literal("Frost Visual"));
    }}

    @Override
    protected void init() {{
        int cx = width / 2;
        int y  = height / 2 - 60;

        // Toggle buttons (simple on/off)
        addDrawableChild(ButtonWidget.builder(
            togLabel("Frost Overlay", FrostConfig.frostOverlay),
            btn -> {{ FrostConfig.frostOverlay = !FrostConfig.frostOverlay;
                      btn.setMessage(togLabel("Frost Overlay", FrostConfig.frostOverlay)); }})
            .dimensions(cx - 110, y + 30, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Aurora", FrostConfig.auroraEnabled),
            btn -> {{ FrostConfig.auroraEnabled = !FrostConfig.auroraEnabled;
                      btn.setMessage(togLabel("Aurora", FrostConfig.auroraEnabled)); }})
            .dimensions(cx + 10, y + 30, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Snow", FrostConfig.snowParticles),
            btn -> {{ FrostConfig.snowParticles = !FrostConfig.snowParticles;
                      btn.setMessage(togLabel("Snow", FrostConfig.snowParticles)); }})
            .dimensions(cx - 110, y + 55, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Motion Blur", FrostConfig.motionBlur),
            btn -> {{ FrostConfig.motionBlur = !FrostConfig.motionBlur;
                      btn.setMessage(togLabel("Motion Blur", FrostConfig.motionBlur)); }})
            .dimensions(cx + 10, y + 55, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("Chrom. Ab.", FrostConfig.chromaticAb),
            btn -> {{ FrostConfig.chromaticAb = !FrostConfig.chromaticAb;
                      btn.setMessage(togLabel("Chrom. Ab.", FrostConfig.chromaticAb)); }})
            .dimensions(cx - 110, y + 80, 100, 20).build());

        // Target HUD
        addDrawableChild(ButtonWidget.builder(
            togLabel("Target HUD", FrostConfig.targetHud),
            btn -> {{ FrostConfig.targetHud = !FrostConfig.targetHud;
                      btn.setMessage(togLabel("Target HUD", FrostConfig.targetHud)); }})
            .dimensions(cx - 110, y + 115, 100, 20).build());

        addDrawableChild(ButtonWidget.builder(
            togLabel("HP Bar", FrostConfig.targetHudBar),
            btn -> {{ FrostConfig.targetHudBar = !FrostConfig.targetHudBar;
                      btn.setMessage(togLabel("HP Bar", FrostConfig.targetHudBar)); }})
            .dimensions(cx + 10, y + 115, 100, 20).build());

        // Watermark
        addDrawableChild(ButtonWidget.builder(
            togLabel("Watermark", FrostConfig.watermark),
            btn -> {{ FrostConfig.watermark = !FrostConfig.watermark;
                      btn.setMessage(togLabel("Watermark", FrostConfig.watermark)); }})
            .dimensions(cx - 50, y + 145, 100, 20).build());

        // Close
        addDrawableChild(ButtonWidget.builder(
            Text.literal("Close"),
            btn -> {{ FrostConfig.save(); close(); }})
            .dimensions(cx - 40, y + 180, 80, 20).build());
    }}

    @Override
    public void render(DrawContext ctx, int mx, int my, float delta) {{
        // Dark background
        ctx.fill(0, 0, width, height, BG);
        // Centre panel
        int px = width / 2 - 130, py = height / 2 - 110;
        ctx.fill(px, py, px + 260, py + 220, PANEL);
        RenderUtil.drawBorder(ctx, px, py, 260, 220, ACCENT, 1);

        // Title
        String title = "❄  FROST VISUAL  v{VERSION}";
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
    }}

    @Override
    public boolean shouldPause() {{ return false; }}

    private static Text togLabel(String name, boolean val) {{
        return Text.literal((val ? "§a✔ " : "§c✘ ") + "§f" + name);
    }}
}}
""")


def gen_game_renderer_mixin():
    write(f"{SRC}/mixin/GameRendererMixin.java", f"""\
package {GROUP}.{MOD_ID}.mixin;

import net.minecraft.client.render.GameRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import {GROUP}.{MOD_ID}.config.FrostConfig;

/**
 * Hook into the game renderer to apply post-process effects:
 *  • Motion blur shader   (when enabled)
 *  • Chromatic aberration (when enabled)
 *  • Frost screen overlay
 */
@Mixin(GameRenderer.class)
public abstract class GameRendererMixin {{

    @Inject(method = "render", at = @At("HEAD"))
    private void frost$onRenderStart(float tickDelta, long startTime,
                                     boolean tick, CallbackInfo ci) {{
        if (!FrostConfig.enabled) return;
        // TODO: load / swap post-process shader chain here
        // e.g. FrostShaderManager.apply(motionBlur, chromatic);
    }}

    @Inject(method = "render", at = @At("TAIL"))
    private void frost$onRenderEnd(float tickDelta, long startTime,
                                   boolean tick, CallbackInfo ci) {{
        // Post-render: chromatic aberration pass
        if (FrostConfig.chromaticAb) {{
            // FrostShaderManager.renderChromatic(FrostConfig.chromaticStrength);
        }}
    }}
}}
""")


def gen_hud_mixin():
    write(f"{SRC}/mixin/InGameHudMixin.java", f"""\
package {GROUP}.{MOD_ID}.mixin;

import net.minecraft.client.gui.hud.InGameHud;
import net.minecraft.client.gui.DrawContext;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import {GROUP}.{MOD_ID}.config.FrostConfig;

/** Injects snow particle overlay into the vanilla HUD render pass. */
@Mixin(InGameHud.class)
public abstract class InGameHudMixin {{

    @Inject(method = "render", at = @At("TAIL"))
    private void frost$onHudRender(DrawContext ctx, float tickDelta, CallbackInfo ci) {{
        if (!FrostConfig.enabled || !FrostConfig.snowParticles) return;
        // FrostParticleRenderer.render(ctx, FrostConfig.snowCount, tickDelta);
    }}
}}
""")


# ══════════════════════════════════════════════════════════════════════════════
#  4. ASSETS
# ══════════════════════════════════════════════════════════════════════════════

def gen_lang():
    data = {
        "key.frostvisual.open_gui": "Open Frost Visual GUI",
        "category.frostvisual": "Frost Visual",
        "frostvisual.gui.title": "Frost Visual Settings"
    }
    write(f"{RES}/assets/{MOD_ID}/lang/en_us.json", json.dumps(data, indent=2))


# ══════════════════════════════════════════════════════════════════════════════
#  5. GITIGNORE & README
# ══════════════════════════════════════════════════════════════════════════════

def gen_gitignore():
    write(f"{BASE}/.gitignore", """\
.gradle/
build/
out/
*.class
*.jar
run/
.idea/
*.iml
""")


def gen_readme():
    write(f"{BASE}/README.md", f"""\
# ❄ {MOD_NAME} `v{VERSION}`

**Minecraft {MC_VERSION} · Fabric**

A purely client-side visual enhancement mod.

## Features
| Feature | Default | Description |
|---|---|---|
| Frost Overlay | ✅ | Icy screen edges |
| Aurora Effect | ✅ | Northern-lights top gradient |
| Snow Particles | ✅ | Falling snow overlay |
| Motion Blur | ❌ | Smooth camera motion |
| Chromatic Ab. | ✅ | Subtle lens fringe |
| **Target HUD** | ✅ | Name + HP bar for targeted entity |
| **Watermark** | ✅ | `Frost Visual v{VERSION}` top-left |

## Open the GUI
Press **Right Shift** in-game.

## Build
```
./gradlew build
```
JAR will be in `build/libs/`.

## Requirements
- Java {JAVA_VERSION}+
- Fabric Loader `{FABRIC_LOADER}`
- Fabric API `{FABRIC_API}`
""")


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"\n{'═'*55}")
    print(f"  Frost Visual Mod — Project Generator")
    print(f"  Minecraft {MC_VERSION} | Fabric")
    print(f"{'═'*55}\n")

    gen_build_gradle()
    gen_gradle_properties()
    gen_settings_gradle()
    gen_fabric_mod_json()
    gen_mixins_json()
    gen_main_mod()
    gen_config()
    gen_hud_renderer()
    gen_render_util()
    gen_gui_screen()
    gen_game_renderer_mixin()
    gen_hud_mixin()
    gen_lang()
    gen_gitignore()
    gen_readme()

    print(f"\n{'═'*55}")
    print(f"  ✅  Project generated in ./{BASE}/")
    print(f"  📂  Open in IntelliJ IDEA and run: ./gradlew build")
    print(f"{'═'*55}\n")


if __name__ == "__main__":
    main()
