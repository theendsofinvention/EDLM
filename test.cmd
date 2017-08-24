@echo off
conda remove -n edlm_test --all -y
conda create -n edlm_test -y
call activate edlm-test
pip install git+file://f:/dev/edlm
pause