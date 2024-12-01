// From https://github.com/hughsk/glsl-hsv2rgb
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec4 texel = vec4(texture(iChannel0, fragCoord / iResolution.xy));
    fragColor = vec4(hsv2rgb(vec3(texel.g, texel.r * vec2(0.2, 0.8) + vec2(0.8, 0.2))), 1);
}