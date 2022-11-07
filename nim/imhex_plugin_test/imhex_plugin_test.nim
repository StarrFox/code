import std/strformat
import std/options

import discord_rpc
import cppstl

{.link: "libimhex.so.1.24.3"}

const hex = "lib/libimhex/include/hex"

type
  #EventManager {.header: hex & "/api/event.hpp", importcpp: "hex::EventManager"} = object
  EventProviderChanged {.header: hex & "/api/event.hpp", importcpp: "hex::EventProviderChanged"} = object
  EventProviderOpened {.header: hex & "/api/event.hpp", importcpp: "hex::EventProviderOpened"} = object
  Provider {.header: hex & "/providers/provider.hpp", importcpp: "hex::prv::Provider"} = object

proc subscribe[T](function: ptr T): void {.header: hex & "/api/event.hpp", importcpp: "hex::EventManager::subscribe<'*1>(@)", nodecl.}

#proc closeImhex(arg: bool): void {.header: hex & "/api/imhex_api.hpp",  importcpp: "hex::ImHexApi::Common::closeImHex(@)".}

proc getName(this: Provider): CppString {.header: hex & "/providers/provider.hpp", importcpp: "#.getName(@)".}

var discord: ptr DiscordRPC

proc updateActivity(details, state: string) =
  discord[].setActivity Activity(
    details: details,
    state: state,
    assets: some ActivityAssets(
      largeImage: "icon-name",
      largeText: "yep, thats it"
    )
  )

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

  discord = create(DiscordRPC)
  discord[] = newDiscordRPC(1039016357754323015)

  discard discord[].connect

  updateActivity("details", "idling")

  proc onProviderChanged(old: ptr Provider, nonold: ptr Provider): void =
    let oldAddress = cast[ByteAddress](old)

    let oldProviderName =
      if oldAddress != 0:
        $old[].getName()
      else:
        "[null]"

    let newProviderName = nonold[].getName()

    echo fmt"onProviderChanged: old: {oldProviderName} new: {newProviderName}"

    updateActivity("onProviderChanged", fmt"editing {newProviderName}")

  proc onProviderOpened(opened: ptr Provider): void =
    let name = opened[].getName()
    echo fmt"onProviderOpened: {name}"

    updateActivity("onProviderOpened", fmt"editing {name}")

  subscribe[EventProviderOpened](cast[ptr EventProviderOpened](onProviderOpened))
  subscribe[EventProviderChanged](cast[ptr EventProviderChanged](onProviderChanged))
