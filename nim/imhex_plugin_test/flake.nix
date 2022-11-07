{
    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
        utils.url = "github:numtide/flake-utils";
    };

    outputs = {self, nixpkgs, utils}:
        utils.lib.eachDefaultSystem (system:
            let
                pkgs = import nixpkgs { inherit system; };
            in {
                packages.default = pkgs.nimPackages.buildNimPackage {
                    name = "imhex_plugin";
                    src = ./.;
                };
                devShells.default = with pkgs; mkShell {
                    buildInputs = [ nim ];
                };
            }
        );

}