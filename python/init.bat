@ECHO OFF

SET ACTIVATE=.\venv\Scripts\activate.bat
SET FLAGS=--trusted-host pypi.org --trusted-host files.pythonhosted.org

IF NOT EXIST %ACTIVATE% (
    ECHO * Creating virtual environment
    python -m venv venv
)

%ACTIVATE% & (

    ECHO * Installing python dependencies
    python -m pip install %FLAGS% --upgrade pip
    pip install %FLAGS% -r requirements.txt

    deactivate
)
