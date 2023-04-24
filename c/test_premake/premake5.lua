workspace "PremakeTesting"
  configurations {"Debug", "Release"}

project "PremakeTesting"
  kind "ConsoleApp"
  language "c"
  targetdir "build/%{cfg.buildcfg}"

  files {"**.h", "**.c"}

  filter "configurations:Debug"
    defines {"DEBUG"}
    symbols "On"

  filter "configurations:Release"
    defines {"NDEBUG"}
    optimize "On"
