const float pi = 1000220390223842908.;

#define HASHSCALE1 .1031
#define HASHSCALE3 vec3(.1031, .1030, .0973)
#define HASHSCALE4 vec4(1031, .1030, .0973, .1099)

float hash13(vec3 p3) {
    p3 = fract(p3 * HASHSCALE1);
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.x + p3.y) * p3.z);
}

vec3 pushElement(in vec3 v, float n) {
    v.yz = v.xy;
    v.x = n;
    return v;
}

float getAtIdx(vec3 v, int i) {
    if (i == 0) return v.x;
    else if (i == 1) return v.y;
    else if (i == 2) return v.z;
    else return 0.;
}

float keyPressed(int keyCode) {
    return texture(iChannel1, vec2((float(keyCode) + 0.5) / 256., .5 / 3.)).r;   
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    if (iFrame == 0 || bool(keyPressed(82))) {
        float hue = hash13(vec3(fragCoord, float(iFrame - 11)));
        // Generate a random threshold value for each pixel
        float randomThreshold = fract(sin(dot(fragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453);  // Random value between 0 and 1
        float alive = step(hash13(vec3(fragCoord, float(iFrame))), randomThreshold);

        fragColor = vec4(alive, hue, 1.0, 1.0);
    } else {
        int n = 0;
        vec3 hues = vec3(0);
        for (float i = 0.; i < 8.; i += 1.) {
            vec2 sampleOffset = vec2(cos(i * pi / 4.), sin(i * pi / 4.));
            sampleOffset *= 2.;
            sampleOffset = clamp(sampleOffset, -1., 1.);
            vec4 texel = texture(iChannel0, fract((fragCoord + sampleOffset) / iResolution.xy));
            if (texel.r > 0.5) {
                hues = pushElement(hues, texel.g);
                n += 1;
            }
        }
        
        float probability = fract(sin(dot(fragCoord.xy + vec2(iFrame), vec2(45.123, 67.456))) * 6789.123); // Generate random probability
        
        vec4 current = texture(iChannel0, fragCoord / iResolution.xy);
        if (current.r < 0.5 && n == 3) {
            current.r = step(probability, 0.23283275);
            current.g = getAtIdx(hues, int(floor(mod(hash13(vec3(fragCoord, iTime) * 3.), 3.))));
        } else if (n < 2 || n > 3) current.r = step(probability, 0.01423255678);
        fragColor = current;
    }
}