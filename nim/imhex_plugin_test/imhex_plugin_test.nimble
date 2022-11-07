# Package

version       = "0.1.0"
author        = "StarrFox"
description   = "A new awesome nimble package"
license       = "GPL-2.0-only"
srcDir        = "src"
backend       = "cpp"
bin           = @["imhex_plugin_test"]

import os
before build:
    echo getCurrentDir()

--app:lib
--threads:on
--define:release
--mm:arc
--passC:"-Isrc/imhex/lib/libimhex/include/"
--passC:"-std=c++20"
--passC:"-Isrc/imhex/lib/external/nativefiledialog/src/include"

# Dependencies

requires "nim >= 1.6.8"
requires "discord_rpc"
requires "cppstl"
