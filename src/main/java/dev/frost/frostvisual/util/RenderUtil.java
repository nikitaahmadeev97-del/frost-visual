package dev.frost.frostvisual.util;

import net.minecraft.client.gui.DrawContext;

/** Small collection of rendering helpers used across Frost Visual. */
public final class RenderUtil {

    private RenderUtil() {}

    /** Draws a solid 1-pixel border around a rectangle. */
    public static void drawBorder(DrawContext ctx,
                                  int x, int y, int w, int h,
                                  int color, int thickness) {
        ctx.fill(x, y, x + w, y + thickness, color);              // top
        ctx.fill(x, y + h - thickness, x + w, y + h, color);      // bottom
        ctx.fill(x, y, x + thickness, y + h, color);               // left
        ctx.fill(x + w - thickness, y, x + w, y + h, color);      // right
    }

    /** Draws a vertical gradient quad. */
    public static void drawVerticalGradient(DrawContext ctx,
                                            int x, int y, int x2, int y2,
                                            int colorTop, int colorBottom) {
        ctx.fillGradient(x, y, x2, y2, colorTop, colorBottom);
    }
}
