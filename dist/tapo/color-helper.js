export class ColorUtils {
}
ColorUtils.presetColors = {
    blue: {
        hue: 240,
        saturation: 100,
        color_temp: 0,
    },
    red: {
        hue: 0,
        saturation: 100,
        color_temp: 0
    },
    yellow: {
        hue: 60,
        saturation: 100,
        color_temp: 0
    },
    green: {
        hue: 120,
        saturation: 100,
        color_temp: 0
    },
    white: {
        color_temp: 4500
    },
    daylightwhite: {
        color_temp: 5500
    },
    warmwhite: {
        color_temp: 2700
    }
};
ColorUtils.hexToHsl = (hex) => {
    if (hex.toLowerCase() === '#000000')
        return console.error('Cannot set light to black');
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (null === result)
        return;
    let r = parseInt(result[1], 16);
    let g = parseInt(result[2], 16);
    let b = parseInt(result[3], 16);
    r /= 255, g /= 255, b /= 255;
    let max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0, s = 0, l = (max + min) / 2;
    if (max == min) {
        h = s = 0; // achromatic
    }
    else {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }
        h /= 6;
    }
    s = s * 100;
    s = Math.round(s);
    l = l * 100;
    l = Math.round(l);
    h = Math.round(360 * h);
    return {
        hue: h,
        saturation: s,
        brightness: l
    };
};
ColorUtils.temperature = (temp) => {
    let t = parseInt(temp.slice(0, -1));
    if (t < 2500 || t > 6500)
        return console.error('Color temperature should be between 2500K and 6500K.');
    return {
        color_temp: t
    };
};
ColorUtils.getColor = (color) => {
    color = color.toLowerCase();
    if (color.startsWith('#'))
        return ColorUtils.hexToHsl(color);
    if (color.endsWith('k'))
        return ColorUtils.temperature(color);
    if (Object.keys(ColorUtils.presetColors).includes(color))
        return ColorUtils.presetColors[color] || "";
    throw new Error('Invalid Color');
};
//# sourceMappingURL=color-helper.js.map