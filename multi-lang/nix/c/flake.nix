{
  description = "Example c flake";

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.cexample =
      let pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
      in
      pkgs.stdenv.mkDerivation {
        pname = "cexample";
        version = "0.1.0";
        src = ./.;
      };

    packages.x86_64-linux.default = self.packages.x86_64-linux.cexample;
  };
}