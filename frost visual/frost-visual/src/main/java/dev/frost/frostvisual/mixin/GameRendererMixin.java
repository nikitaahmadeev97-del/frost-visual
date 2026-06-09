package dev.frost.frostvisual.mixin;

import net.minecraft.client.render.GameRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import dev.frost.frostvisual.config.FrostConfig;

/**
 * Hook into the game renderer to apply post-process effects:
 *  • Motion blur shader   (when enabled)
 *  • Chromatic aberration (when enabled)
 *  • Frost screen overlay
 */
@Mixin(GameRenderer.class)
public abstract class GameRendererMixin {

    @Inject(method = "render", at = @At("HEAD"))
    private void frost$onRenderStart(float tickDelta, long startTime,
                                     boolean tick, CallbackInfo ci) {
        if (!FrostConfig.enabled) return;
        // TODO: load / swap post-process shader chain here
        // e.g. FrostShaderManager.apply(motionBlur, chromatic);
    }

    @Inject(method = "render", at = @At("TAIL"))
    private void frost$onRenderEnd(float tickDelta, long startTime,
                                   boolean tick, CallbackInfo ci) {
        // Post-render: chromatic aberration pass
        if (FrostConfig.chromaticAb) {
            // FrostShaderManager.renderChromatic(FrostConfig.chromaticStrength);
        }
    }
}
