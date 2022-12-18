{
  description = "A very basic flake";

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.basic = 
      let pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
      in
      pkgs.stdenv.mkDerivation {
        pname = "basic";
        version = "0.1.0";
        src = ./.;
        buildInputs = with pkgs; [
          zig
        ];
        buildPhase = ''
        export XDG_CACHE_HOME=".cache"
        zig build-exe src/main.zig --name basic
        '';
        installPhase = ''
        mkdir -p $out/bin
        cp basic $out/bin
        '';
      };

    packages.x86_64-linux.default = self.packages.x86_64-linux.basic;
  };
}
