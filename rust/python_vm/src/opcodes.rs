const CACHE: u16 = 0;
const POP_TOP: u16 = 1;
const PUSH_NULL: u16 = 2;
const INTERPRETER_EXIT: u16 = 3;
const END_FOR: u16 = 4;
const END_SEND: u16 = 5;
const NOP: u16 = 9;
const UNARY_NEGATIVE: u16 = 11;
const UNARY_NOT: u16 = 12;
const UNARY_INVERT: u16 = 15;
const RESERVED: u16 = 17;
const BINARY_SUBSCR: u16 = 25;
const BINARY_SLICE: u16 = 26;
const STORE_SLICE: u16 = 27;
const GET_LEN: u16 = 30;
const MATCH_MAPPING: u16 = 31;
const MATCH_SEQUENCE: u16 = 32;
const MATCH_KEYS: u16 = 33;
const PUSH_EXC_INFO: u16 = 35;
const CHECK_EXC_MATCH: u16 = 36;
const CHECK_EG_MATCH: u16 = 37;
const WITH_EXCEPT_START: u16 = 49;
const GET_AITER: u16 = 50;
const GET_ANEXT: u16 = 51;
const BEFORE_ASYNC_WITH: u16 = 52;
const BEFORE_WITH: u16 = 53;
const END_ASYNC_FOR: u16 = 54;
const CLEANUP_THROW: u16 = 55;
const STORE_SUBSCR: u16 = 60;
const DELETE_SUBSCR: u16 = 61;
const GET_ITER: u16 = 68;
const GET_YIELD_FROM_ITER: u16 = 69;
const LOAD_BUILD_CLASS: u16 = 71;
const LOAD_ASSERTION_ERROR: u16 = 74;
const RETURN_GENERATOR: u16 = 75;
const RETURN_VALUE: u16 = 83;
const SETUP_ANNOTATIONS: u16 = 85;
const POP_EXCEPT: u16 = 89;
const HAVE_ARGUMENT: u16 = 90;
const STORE_NAME: u16 = 90;
const DELETE_NAME: u16 = 91;
const UNPACK_SEQUENCE: u16 = 92;
const FOR_ITER: u16 = 93;
const UNPACK_EX: u16 = 94;
const STORE_ATTR: u16 = 95;
const DELETE_ATTR: u16 = 96;
const STORE_GLOBAL: u16 = 97;
const DELETE_GLOBAL: u16 = 98;
const SWAP: u16 = 99;
const LOAD_CONST: u16 = 100;
const LOAD_NAME: u16 = 101;
const BUILD_TUPLE: u16 = 102;
const BUILD_LIST: u16 = 103;
const BUILD_SET: u16 = 104;
const BUILD_MAP: u16 = 105;
const LOAD_ATTR: u16 = 106;
const COMPARE_OP: u16 = 107;
const IMPORT_NAME: u16 = 108;
const IMPORT_FROM: u16 = 109;
const JUMP_FORWARD: u16 = 110;
const POP_JUMP_IF_FALSE: u16 = 114;
const POP_JUMP_IF_TRUE: u16 = 115;
const LOAD_GLOBAL: u16 = 116;
const IS_OP: u16 = 117;
const CONTAINS_OP: u16 = 118;
const RERAISE: u16 = 119;
const COPY: u16 = 120;
const RETURN_CONST: u16 = 121;
const BINARY_OP: u16 = 122;
const SEND: u16 = 123;
const LOAD_FAST: u16 = 124;
const STORE_FAST: u16 = 125;
const DELETE_FAST: u16 = 126;
const LOAD_FAST_CHECK: u16 = 127;
const POP_JUMP_IF_NOT_NONE: u16 = 128;
const POP_JUMP_IF_NONE: u16 = 129;
const RAISE_VARARGS: u16 = 130;
const GET_AWAITABLE: u16 = 131;
const MAKE_FUNCTION: u16 = 132;
const BUILD_SLICE: u16 = 133;
const JUMP_BACKWARD_NO_INTERRUPT: u16 = 134;
const MAKE_CELL: u16 = 135;
const LOAD_CLOSURE: u16 = 136;
const LOAD_DEREF: u16 = 137;
const STORE_DEREF: u16 = 138;
const DELETE_DEREF: u16 = 139;
const JUMP_BACKWARD: u16 = 140;
const CALL_FUNCTION_EX: u16 = 142;
const EXTENDED_ARG: u16 = 144;
const LIST_APPEND: u16 = 145;
const SET_ADD: u16 = 146;
const MAP_ADD: u16 = 147;
const LOAD_CLASSDEREF: u16 = 148;
const COPY_FREE_VARS: u16 = 149;
const YIELD_VALUE: u16 = 150;
const RESUME: u16 = 151;
const MATCH_CLASS: u16 = 152;
const FORMAT_VALUE: u16 = 155;
const BUILD_CONST_KEY_MAP: u16 = 156;
const BUILD_STRING: u16 = 157;
const LIST_EXTEND: u16 = 162;
const SET_UPDATE: u16 = 163;
const DICT_MERGE: u16 = 164;
const DICT_UPDATE: u16 = 165;
const CALL: u16 = 171;
const KW_NAMES: u16 = 172;
const CALL_INTRINSIC_1: u16 = 173;
const CALL_INTRINSIC_2: u16 = 174;
const MIN_INSTRUMENTED_OPCODE: u16 = 238;
const INSTRUMENTED_POP_JUMP_IF_NONE: u16 = 238;
const INSTRUMENTED_POP_JUMP_IF_NOT_NONE: u16 = 239;
const INSTRUMENTED_RESUME: u16 = 240;
const INSTRUMENTED_CALL: u16 = 241;
const INSTRUMENTED_RETURN_VALUE: u16 = 242;
const INSTRUMENTED_YIELD_VALUE: u16 = 243;
const INSTRUMENTED_CALL_FUNCTION_EX: u16 = 244;
const INSTRUMENTED_JUMP_FORWARD: u16 = 245;
const INSTRUMENTED_JUMP_BACKWARD: u16 = 246;
const INSTRUMENTED_RETURN_CONST: u16 = 247;
const INSTRUMENTED_FOR_ITER: u16 = 248;
const INSTRUMENTED_POP_JUMP_IF_FALSE: u16 = 249;
const INSTRUMENTED_POP_JUMP_IF_TRUE: u16 = 250;
const INSTRUMENTED_END_FOR: u16 = 251;
const INSTRUMENTED_END_SEND: u16 = 252;
const INSTRUMENTED_INSTRUCTION: u16 = 253;
const INSTRUMENTED_LINE: u16 = 254;
const MIN_PSEUDO_OPCODE: u16 = 256;
const SETUP_FINALLY: u16 = 256;
const SETUP_CLEANUP: u16 = 257;
const SETUP_WITH: u16 = 258;
const POP_BLOCK: u16 = 259;
const JUMP: u16 = 260;
const JUMP_NO_INTERRUPT: u16 = 261;
const LOAD_METHOD: u16 = 262;
const MAX_PSEUDO_OPCODE: u16 = 262;
const BINARY_OP_ADD_FLOAT: u16 = 6;
const BINARY_OP_ADD_INT: u16 = 7;
const BINARY_OP_ADD_UNICODE: u16 = 8;
const BINARY_OP_INPLACE_ADD_UNICODE: u16 = 10;
const BINARY_OP_MULTIPLY_FLOAT: u16 = 13;
const BINARY_OP_MULTIPLY_INT: u16 = 14;
const BINARY_OP_SUBTRACT_FLOAT: u16 = 16;
const BINARY_OP_SUBTRACT_INT: u16 = 18;
const BINARY_SUBSCR_DICT: u16 = 19;
const BINARY_SUBSCR_GETITEM: u16 = 20;
const BINARY_SUBSCR_LIST_INT: u16 = 21;
const BINARY_SUBSCR_TUPLE_INT: u16 = 22;
const CALL_PY_EXACT_ARGS: u16 = 23;
const CALL_PY_WITH_DEFAULTS: u16 = 24;
const CALL_BOUND_METHOD_EXACT_ARGS: u16 = 28;
const CALL_BUILTIN_CLASS: u16 = 29;
const CALL_BUILTIN_FAST_WITH_KEYWORDS: u16 = 34;
const CALL_METHOD_DESCRIPTOR_FAST_WITH_KEYWORDS: u16 = 38;
const CALL_NO_KW_BUILTIN_FAST: u16 = 39;
const CALL_NO_KW_BUILTIN_O: u16 = 40;
const CALL_NO_KW_ISINSTANCE: u16 = 41;
const CALL_NO_KW_LEN: u16 = 42;
const CALL_NO_KW_LIST_APPEND: u16 = 43;
const CALL_NO_KW_METHOD_DESCRIPTOR_FAST: u16 = 44;
const CALL_NO_KW_METHOD_DESCRIPTOR_NOARGS: u16 = 45;
const CALL_NO_KW_METHOD_DESCRIPTOR_O: u16 = 46;
const CALL_NO_KW_STR_1: u16 = 47;
const CALL_NO_KW_TUPLE_1: u16 = 48;
const CALL_NO_KW_TYPE_1: u16 = 56;
const COMPARE_OP_FLOAT: u16 = 57;
const COMPARE_OP_INT: u16 = 58;
const COMPARE_OP_STR: u16 = 59;
const FOR_ITER_LIST: u16 = 62;
const FOR_ITER_TUPLE: u16 = 63;
const FOR_ITER_RANGE: u16 = 64;
const FOR_ITER_GEN: u16 = 65;
const LOAD_ATTR_CLASS: u16 = 66;
const LOAD_ATTR_GETATTRIBUTE_OVERRIDDEN: u16 = 67;
const LOAD_ATTR_INSTANCE_VALUE: u16 = 70;
const LOAD_ATTR_MODULE: u16 = 72;
const LOAD_ATTR_PROPERTY: u16 = 73;
const LOAD_ATTR_SLOT: u16 = 76;
const LOAD_ATTR_WITH_HINT: u16 = 77;
const LOAD_ATTR_METHOD_LAZY_DICT: u16 = 78;
const LOAD_ATTR_METHOD_NO_DICT: u16 = 79;
const LOAD_ATTR_METHOD_WITH_VALUES: u16 = 80;
const LOAD_CONST__LOAD_FAST: u16 = 81;
const LOAD_FAST__LOAD_CONST: u16 = 82;
const LOAD_FAST__LOAD_FAST: u16 = 84;
const LOAD_GLOBAL_BUILTIN: u16 = 86;
const LOAD_GLOBAL_MODULE: u16 = 87;
const STORE_ATTR_INSTANCE_VALUE: u16 = 88;
const STORE_ATTR_SLOT: u16 = 111;
const STORE_ATTR_WITH_HINT: u16 = 112;
const STORE_FAST__LOAD_FAST: u16 = 113;
const STORE_FAST__STORE_FAST: u16 = 141;
const STORE_SUBSCR_DICT: u16 = 143;
const STORE_SUBSCR_LIST_INT: u16 = 153;
const UNPACK_SEQUENCE_LIST: u16 = 154;
const UNPACK_SEQUENCE_TUPLE: u16 = 158;
const UNPACK_SEQUENCE_TWO_TUPLE: u16 = 159;
const SEND_GEN: u16 = 160;