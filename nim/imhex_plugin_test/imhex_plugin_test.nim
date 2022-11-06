{.link: "./libimhex.so.1.24.3"}

proc closeImhex(): void {.importcpp: "hex::ImHexApi::Common::closeImhex()".}

proc getPluginName*(): cstring {.exportc,dynlib.} = 
  return cstring"Test"

proc getPluginAuthor*(): cstring {.exportc,dynlib.} =
  return cstring"StarrFox"

proc getPluginDescription*(): cstring {.exportc,dynlib.} =
  return cstring"Description"

proc getCompatibleVersion*(): cstring {.exportc,dynlib.} =
  return cstring"1.24.3"

proc setImGuiContext*(ctx: ptr): void {.exportc,dynlib.} =
  discard

proc initializePlugin*(): void {.exportc,dynlib.} =
  echo "plugin loaded"
  closeImhex()
