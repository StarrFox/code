import cppstl

const hex = "imhex/lib/libimhex/include/hex"
const pl = "imhex/lib/external/pattern_language/lib/include/pl"

type
    FunctionParameterCount {.header: pl & "/api.hpp", importcpp: "pl::api::FunctionParameterCount"} = object
    FunctionCallback {.header: pl & "/api.hpp", importcpp: "pl::api::FunctionCallback"} = object
    CppVariant[T] {.importcpp: "std::variant<'*0>"} = object 

# std::function<return type>(?)
#proc initFunctionCallback(): FunctionCallback {.constructor, importcpp: "pl::api::FunctionCallback<'*0>()".}
proc initFunctionParameterCountExactly(howmany: cint): FunctionParameterCount {.importcpp: "pl::api::FunctionParameterCount::exactly(@)".}

# https://github.com/WerWolv/ImHex/blob/603ff9256c1f98b7fa08c3d2ce9007f7a102917a/lib/libimhex/include/hex/api/content_registry.hpp#L138
# void addFunction(const pl::api::FunctionCallback &func);
proc addFunction(namespace: CppVector[CppString], name: CppString, parameterCount: FunctionParameterCount, callback: proc (x: var Evaluator, y: CppVector[Literal])): void {.header: hex & "/api/content_registry.hpp", importcpp: "hex::ContentRegistry::PatternLanguage::addFunction(@)".}

proc getPluginName*(): cstring {.exportc,dynlib.} = 
  return cstring"ImhexZlib"

proc getPluginAuthor*(): cstring {.exportc,dynlib.} =
  return cstring"StarrFox"

proc getPluginDescription*(): cstring {.exportc,dynlib.} =
  return cstring"Adds zlib decompress to imhex"

proc getCompatibleVersion*(): cstring {.exportc,dynlib.} =
  return cstring"1.25.0"

proc setImGuiContext*(ctx: ptr): void {.exportc,dynlib.} =
  discard

proc decompress(ctx: ptr, params: CppVector): cint =
    return 1

proc initializePlugin*(): void {.exportc,dynlib.} =
    # zlib::decompress
    var namespaceVec = initCppVector[CppString]()
    var namespace = initCppString("zlib")

    namespaceVec.push_back(namespace)

    var functionName = initCppString("decompress")
    # min, max
    var parameterCount = initFunctionParameterCountExactly(2)

    addFunction(namespaceVec, functionName, parameterCount, decompress)
