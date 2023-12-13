let
  pkgs = import <nixpkgs> {};
in
derivation {
  name = "basic";
  system = "x86_64-linux";
  builder = "${pkgs.bash}/bin/bash";
  args = ["${./builder.sh}"];
  PATH = "${pkgs.gcc}/bin/:${pkgs.busybox}/bin/";
}
