{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts/";
    nix-systems.url = "github:nix-systems/default";
  };

  outputs = inputs @ {
    flake-parts,
    nix-systems,
    nixpkgs,
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
        projectCargo = builtins.fromTOML (builtins.readFile ./Cargo.toml);
        packageName = projectCargo.package.name;
      in {
        packages.${packageName} = pkgs.rustPlatform.buildRustPackage {
          name = packageName;
          src = ./.;
          version = projectCargo.package.version;
          nativeBuildInputs = with pkgs; [
            cmake
            raylib
            xorg.libX11.dev
            xorg.libXrandr.dev
            xorg.libXinerama.dev
            xorg.libXcursor.dev
            xorg.libXi.dev
            pkg-config
          ];
          cargoLock = {
            lockFile = ./Cargo.lock;
          };
        };

        packages.default = self'.packages.${packageName};

        devShells.default = pkgs.mkShell {
          name = packageName;
          packages = with pkgs; [
            rustc
            cargo
            cmake

            xorg.libX11.dev
            xorg.libXrandr.dev
            xorg.libXinerama.dev
            xorg.libXcursor.dev
            xorg.libXi.dev
            pkg-config

            raylib

            just
            alejandra
          ];
        };
      };
    };
}