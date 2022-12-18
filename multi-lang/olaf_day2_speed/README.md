compile nim code with:
nim c --mm:arc -d:danger --threads:off --passC:-flto --passL:-flto --experimental:views --cc:clang -d:useMalloc --maxLoopIterationsVM:100000000 olaf6.nim
