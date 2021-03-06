require() {
  command -v "$1" >/dev/null 2>&1 || {
    echo >&2 "I require $1 but it's not installed. "; return 1;
  }
}

if [[ ! -d "venv" ]]; then
  require "virtualenv" && {
    virtualenv venv
  }
fi

if [[ -d "venv" ]]; then
  source ./venv/bin/activate
  pip install -r requirements.txt
fi