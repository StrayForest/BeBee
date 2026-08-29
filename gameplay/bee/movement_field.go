components {
  id: "controller"
  component: "/gameplay/bee/movement_field.script"
}
components {
  id: "view"
  component: "/gameplay/bee/movement_field.gui"
}
embedded_components {
  id: "camera"
  type: "camera"
  data: "aspect_ratio: 0.0\n"
  "fov: 0.0\n"
  "near_z: -1.0\n"
  "far_z: 1.0\n"
  "orthographic_projection: 1\n"
  ""
}
