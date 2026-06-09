package dev.frost.frostvisual.mixin;

import net.minecraft.client.gui.hud.InGameHud;
import net.minecraft.client.gui.DrawContext;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import dev.frost.frostvisual.config.FrostConfig;

/** Injects snow particle overlay into the vanilla HUD render pass. */
@Mixin(InGameHud.class)
public abstract class InGameHudMixin {

    @Inject(method = "render", at = @At("TAIL"))
    private void frost$onHudRender(DrawContext ctx, float tickDelta, CallbackInfo ci) {
        if (!FrostConfig.enabled || !FrostConfig.snowParticles) return;
        // FrostParticleRenderer.render(ctx, FrostConfig.snowCount, tickDelta);
    }
}
