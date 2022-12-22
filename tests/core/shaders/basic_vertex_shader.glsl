// VERTEX SHADER
// --------------------------------------
#version 150
uniform mat4 u_pm;   // projection matrix
uniform mat4 u_vm;   // view matrix 
uniform mat4 u_mm;   // model matrix 
in vec4 a_pos;       // vertex position in
in vec3 a_norm;      // normal in 
out vec3 v_norm;     // normal out
out mat4 v_mv;       // modelview matrix out
out vec3 v_pos;      // vertex position out
 
void main() {
  gl_Position = u_pm * u_vm * u_mm * a_pos;
  v_mv = u_vm * u_mm;
  v_norm = a_norm;     
  v_pos = vec3(v_mv * a_pos);  // our position in eye coords
}
 
