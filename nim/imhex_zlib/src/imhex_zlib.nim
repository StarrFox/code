import cppstl

const hex = "imhex/lib/libimhex/include/hex"
# const pl = "imhex/lib/external/plattern_language/lib/include/pl"

{.push header: "<functional>"}

type
    ParamCount* = object
        min*, max*: int
    
    CppFunction*[T] {.importcpp: "std::function"} = object

# std::function<return type>(?)
proc initCppFunction*[T](): CppFunction {.constructor, importcpp: "std::function<'*0>()".} 

# type
#     FunctionParameterCount {.header: pl & "/api.hpp", importcpp: "pl::api::FunctionParameterCount"} = object

# https://github.com/WerWolv/ImHex/blob/603ff9256c1f98b7fa08c3d2ce9007f7a102917a/lib/libimhex/include/hex/api/content_registry.hpp#L138
# void addFunction(const pl::api::FunctionCallback &func);
proc addFunction(
    namespace: CppVector[CppString],
    name: CppString,
    parameterCount: ParamCount,
    callback: ptr
    ):  void {.header: hex & "/api/content_registry.hpp", importcpp: "hex::ContentRegistery::PatternLanguage::addFunction(@)".}

proc getPluginName*(): cstring {.exportc,dynlib.} = 
  return cstring"DiscordRPC"

proc getPluginAuthor*(): cstring {.exportc,dynlib.} =
  return cstring"StarrFox"

proc getPluginDescription*(): cstring {.exportc,dynlib.} =
  return cstring"Adds discord rpc to imhex"

proc getCompatibleVersion*(): cstring {.exportc,dynlib.} =
  return cstring"1.25.0"

proc setImGuiContext*(ctx: ptr): void {.exportc,dynlib.} =
  discard

proc initializePlugin*(): void {.exportc,dynlib.} =
    proc decompress() =
        discard

    # zlib::decompress
    var namespaceVec = initCppVector[CppString]()
    var namespace = initCppString("zlib")

    namespaceVec.push_back(namespace)

    var functionName = initCppString("decompress")
    # min, max
    var parameterCount = ParamCount(min: 1, max: 1)

    addFunction(namespaceVec, functionName, parameterCount, cast[ptr CppFunction[void]](decompress))
