// FRAGMENT SHADER
// --------------------------------------
#version 150
uniform mat4 rectVec;
out vec4 fragcolor;

void main() {
  fragcolor.rgb = 0.5 + 0.5 * v_norm;   // note that we are directly using the normals as colors and don't convert it to eye coords
}