{
  description = "a project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts/";
    nix-systems.url = "github:nix-systems/default";
  };

  outputs = inputs @ {flake-parts, nix-systems, ...}:
    flake-parts.lib.mkFlake {inherit inputs;} {
      debug = true;
      systems = import nix-systems;
      perSystem = {pkgs, ...}: {
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "test";
          version = "0.1.0";
          src = ./.;
        };

        devShells.default = pkgs.mkShell {
          name = "manual_make";
          packages = with pkgs; [
            gnumake
          ];
        };
      };
    };
}
