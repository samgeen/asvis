
varying vec4 vertex_color;
void main() 
{
	//float em1 = 1.71828183.0;
	//vec4 veminus1 = vec4(em1,em1,em1,em1);
	//vec4 ones = vec4(1.0,1.0,1.0,1.0);
	//gl_FragColor = log(vertex_color*vec4(1.718,1.718,1.718,1.718)+vec4(1.0,1.0,1.0,1.0));
	vec4 colour = vertex_color.aaar*10.0;
	gl_FragColor = log((colour*1.718)+1.0);
	//gl_FragColor = vertex_color;
}


// TODO: USE http://aras-p.info/blog/2008/06/20/encoding-floats-to-rgba-again/
//       THIS ALLOWS US TO USE THE TEXTURE TO BUFFER UP VALUES + LOG THEM
//       OR DO WE PREFER TO USE THE BLEND FUNCTIONS??
// inline float4 EncodeFloatRGBA( float v ) {
//  return frac( float4(1.0, 255.0, 65025.0, 160581375.0) * v ) + bias;
// }
// inline float DecodeFloatRGBA( float4 rgba ) {
//  return dot( rgba, float4(1.0, 1/255.0, 1/65025.0, 1/160581375.0) );
// }