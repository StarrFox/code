{
  description = "misc code";

  inputs = {
    nixpkgs.url = "github:NixOs/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    nix-systems.url = "github:nix-systems/default";
  };

  outputs = inputs @ {self, flake-parts, nix-systems, ...}:
    flake-parts.lib.mkFlake {inherit inputs;} {
      debug = true;
      systems = import nix-systems;
      perSystem = {pkgs, ...}: {
        devShells.default = pkgs.mkShell {
          name = "code";
          packages = with pkgs; [
            python3
            zig
            rustup
            cargo
            gcc
            nim
            elixir
          ];
        };
      };
    };
}