with import <nixpkgs> {}; stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    sqlite
    mitmproxy
    python3
    python3Packages.beautifulsoup4
  ];
  shellHook = ''
    export PYTHONPATH=".:$PYTHONPATH"
  '';
}
