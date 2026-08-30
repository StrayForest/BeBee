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
  "orthographic_zoom: 1.0\n"
  "orthographic_mode: ORTHO_MODE_AUTO_COVER\n"
  ""
}
embedded_components {
  id: "pollination_complete"
  type: "sound"
  data: "sound: \"/assets/audio/pollination_complete.wav\"\n"
  "looping: 0\n"
  "group: \"master\"\n"
  "gain: 0.75\n"
  ""
}
embedded_components {
  id: "region_complete"
  type: "sound"
  data: "sound: \"/assets/audio/region_complete.wav\"\n"
  "looping: 0\n"
  "group: \"master\"\n"
  "gain: 0.85\n"
  ""
}
embedded_components {
  id: "pollen_chime"
  type: "sound"
  data: "sound: \"/assets/audio/pollen_chime.wav\"\n"
  "looping: 0\n"
  "group: \"master\"\n"
  "gain: 0.62\n"
  ""
}
embedded_components {
  id: "portal_whoosh"
  type: "sound"
  data: "sound: \"/assets/audio/portal_whoosh.wav\"\n"
  "looping: 0\n"
  "group: \"master\"\n"
  "gain: 0.58\n"
  ""
}
embedded_components {
  id: "pest_alert"
  type: "sound"
  data: "sound: \"/assets/audio/pest_alert.wav\"\n"
  "looping: 0\n"
  "group: \"master\"\n"
  "gain: 0.45\n"
  ""
}
