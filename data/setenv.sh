# THIS DOEST NOT WORK AS IS
# Seems like it is possible but the sky is high and the emperor far away
# Create virtual env 
virtualenv $USERPROFILE/.virtualenv/carto-fn
python.exe -m venv Scripts
# this puts virtualenv \Scripts at front of path
source $USERPROFILE/.virtualenv/carto-fn/Scripts/activate
#source $USERPROFILE/.virtualenv/carto-fn/Scripts/activate
# for this virtualenv add https://github.com/CartoDB/carto-python
pip install carto