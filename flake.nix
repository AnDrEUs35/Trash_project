{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    pythonVerison = "python312";
  in {
    devShells.${system}.default = pkgs.mkShell rec {
      packages = [
        pkgs.${pythonVerison}
        pkgs.${pythonVerison}.pkgs.pip
      ];
      buildInputs = [
        pkgs.zlib
      ];
      shellHook = ''
        export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath buildInputs}:$LD_LIBRARY_PATH"
        export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib.outPath}/lib:$LD_LIBRARY_PATH"
        tmp=$(mktemp -d)
        
        python -m venv $tmp/venv
        $tmp/venv/bin/pip install -r ${self}/requirements.txt

        mkdir $tmp/src
        cp -r ${self}/* $tmp/src
        chmod -R 777 $tmp/src
        
        mkdir ./results
        mv -f ./parameters/*.json ./parameters/output.json
        $tmp/venv/bin/python $tmp/src/__main__.py ./parameters/output.json ./results
        EXIT_CODE=$?
        
        rm -rf $tmp
        exit $EXIT_CODE
      '';
    };
  };
}