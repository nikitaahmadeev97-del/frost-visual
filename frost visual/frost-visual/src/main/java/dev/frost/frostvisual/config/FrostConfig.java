package dev.frost.frostvisual.config;

/**
 * Runtime configuration holder for Frost Visual.
 * Persisted to config/frostvisual.json via Gson.
 */
public class FrostConfig {

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

    public static void load()  { /* TODO: read from JSON with Gson */ }
    public static void save()  { /* TODO: write to JSON with Gson  */ }
}
