./ci/pyenv-installer

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install -vs 3.4.2
pyenv install -vs 3.3.6
pyenv install -vs 2.7.9
