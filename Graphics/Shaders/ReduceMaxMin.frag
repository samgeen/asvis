
// Sample a texture and return the max of a square of values
// NOTE - USES RED VALUE TO CALCULATE MAX AND GREEN VALUE TO CALCULATE MIN; BLUE/ALPHA ARE UNUSED
uniform sampler2D    tex;
uniform float        dt;

float mincompare(float v1, float v2)
{
	if (v1 == 0.0) return v2;
	if (v2 == 0.0) return v1;
	return min(v1,v2);
}

void main(void)
{
    vec4 col0 = texture2D(tex, gl_TexCoord[0].st);
    vec4 col1 = texture2D(tex, gl_TexCoord[0].st - vec2(dt, 0.0));
    vec4 col2 = texture2D(tex, gl_TexCoord[0].st - vec2(0.0, dt));
    vec4 col3 = texture2D(tex, gl_TexCoord[0].st - vec2(dt, dt));
    // Find max of 4 colours
    float r = max(max(col0.r, col1.r), max(col2.r, col3.r));
    // Min is a little trickier as we need to ignore zero values
    vec4 gs = vec4(col0.g,col1.g,col2.g,col3.g);
    float g = mincompare(mincompare(gs[0],gs[1]),mincompare(gs[2],gs[3]));
    // Set the colour to be r = max, g = min (b and a unused)
    gl_FragColor = vec4(r,g,1.0,1.0);
}