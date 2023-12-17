{
  description = "a python project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts/";
    nix-systems.url = "github:nix-systems/default";
  };

  outputs = inputs @ {
    self,
    flake-parts,
    nix-systems,
    poetry2nix,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      debug = true;
      systems = import nix-systems;
      perSystem = {
        pkgs,
        system,
        self',
        ...
      }: let
        python = pkgs.python312.withPackages (python-pkgs: with python-pkgs; [
          pyparsing
        ]);
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            python
          ];

          shellHook = ''
            venv="$(cd $(dirname $(which python)); cd ..; pwd)"
            ln -Tsf "$venv" .venv
          '';
        };
      };
    };
}