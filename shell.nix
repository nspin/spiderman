with import <nixpkgs> {}; stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    sqlite
    mitmproxy
    python3
    python3Packages.beautifulsoup4
    python3Packages.selenium
    python3Packages.requests
    python3Packages.flask
    python3Packages.werkzeug
  ];
  shellHook = ''
    export PYTHONPATH="$PWD:$PYTHONPATH"
  '';
}
