import std/strformat
import std/options

import discord_rpc
import cppstl

const hex = "imhex/lib/libimhex/include/hex"

type
  EventProviderChanged {.header: hex & "/api/event.hpp", importcpp: "hex::EventProviderChanged"} = object
  EventProviderOpened {.header: hex & "/api/event.hpp", importcpp: "hex::EventProviderOpened"} = object
  Provider {.header: hex & "/providers/provider.hpp", importcpp: "hex::prv::Provider"} = object

proc subscribe[T](function: ptr T): void {.header: hex & "/api/event.hpp", importcpp: "hex::EventManager::subscribe<'*1>(@)", nodecl.}

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
  return cstring"DiscordRPC"

proc getPluginAuthor*(): cstring {.exportc,dynlib.} =
  return cstring"StarrFox"

proc getPluginDescription*(): cstring {.exportc,dynlib.} =
  return cstring"Adds discord rpc to imhex"

proc getCompatibleVersion*(): cstring {.exportc,dynlib.} =
  return cstring"1.24.3"

proc setImGuiContext*(ctx: ptr): void {.exportc,dynlib.} =
  discard

proc initializePlugin*(): void {.exportc,dynlib.} =
  discord = create(DiscordRPC)
  discord[] = newDiscordRPC(1039016357754323015)

  discard discord[].connect

  updateActivity("details", "idling")

  proc onProviderChanged(old: ptr Provider, nonold: ptr Provider): void =
    let name = nonold[].getName()
    updateActivity("onProviderChanged", fmt"editing {name}")

  proc onProviderOpened(opened: ptr Provider): void =
    let name = opened[].getName()
    updateActivity("onProviderOpened", fmt"editing {name}")

  subscribe[EventProviderOpened](cast[ptr EventProviderOpened](onProviderOpened))
  subscribe[EventProviderChanged](cast[ptr EventProviderChanged](onProviderChanged))
