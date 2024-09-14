{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
  in {
    devShells."x86_64-linux".default = pkgs.mkShell {
      packages = with pkgs; [
        chromedriver

        python311
        python311Packages.selenium
        python311Packages.openai
        python311Packages.python-dotenv
        python311Packages.python-socketio
        python311Packages.flask
        python311Packages.speechrecognition
        python311Packages.websockets
        python311Packages.pydub
        python311Packages.scipy
        python311Packages.webdriver-manager
        python311Packages.beautifulsoup4
        python311Packages.pynput
        python311Packages.pyaudio
      ];
    };
  };
}
