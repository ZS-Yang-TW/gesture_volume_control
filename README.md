# 【事前準備】使用 pyenv 建立 Python 3.9 虛擬環境
Python 建議版本 : **3.9**

因為現在 Python 3.9 已經不是主要版本了，不過你可以使用 pyenv 來指定虛擬環境，安裝步驟如下：

（以下都是 bash 指令）

1. 使用 pip 安裝 pyenv。
    ```bash
    pip install pyenv-win --target $HOME/.pyenv
    ```

2. 設定環境變數。
    ```bash
    export PYENV="$HOME/.pyenv/pyenv-win/"
    export PYENV_HOME="$HOME/.pyenv/pyenv-win/"
    export PATH="$HOME/.pyenv/pyenv-win/bin:$HOME/.pyenv/pyenv-win/shims:$PATH"
    ```

3. 驗證 pyenv 有沒有安裝成功。
    ```bash
    pyenv --version
    ```

4. pyenv 安裝成功後，就可以指定環境的版本。
    ```bash
    pyenv local 3.9.8
    ```

# 【事前準備】安裝套件!
請在終端機輸入以下指令

```bash
pip install -r requirements.txt
```
