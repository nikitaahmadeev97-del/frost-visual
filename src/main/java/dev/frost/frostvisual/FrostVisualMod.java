package dev.frost.frostvisual;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.client.util.InputUtil;
import org.lwjgl.glfw.GLFW;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import dev.frost.frostvisual.config.FrostConfig;
import dev.frost.frostvisual.gui.FrostGuiScreen;
import dev.frost.frostvisual.hud.FrostHudRenderer;

public class FrostVisualMod implements ClientModInitializer {

    public static final String MOD_ID  = "frostvisual";
    public static final String VERSION = "1.0.0";
    public static final Logger LOGGER  = LoggerFactory.getLogger(MOD_ID);

    // Right Shift keybind — opens the Frost Visual GUI
    public static KeyBinding OPEN_GUI_KEY;

    @Override
    public void onInitializeClient() {
        LOGGER.info("[FrostVisual] Initialising v{} for Minecraft 1.21.11", VERSION);

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
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            while (OPEN_GUI_KEY.wasPressed()) {
                client.setScreen(new FrostGuiScreen());
            }
        });

        LOGGER.info("[FrostVisual] Ready!");
    }
}
