REM This is working fine for me from CMD on python 3.8 
REM Create virtual env 
virtualenv %USERPROFILE%\.virtualenv\carto-fn
REM this puts virtualenv \Scripts at front of path
%USERPROFILE%\.virtualenv\carto-fn\Scripts\activate.bat
REM for this virtualenv add https://github.com/CartoDB/carto-python
pip install carto
