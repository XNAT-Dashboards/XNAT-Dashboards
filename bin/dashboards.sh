export PYTHONPATH=/home/marina/Dev/forks/pyxnat:$PYTHONPATH
export PYTHONPATH=/home/marina/Dev/forks/XNAT-Dashboards:$PYTHONPATH
cd /home/marina/Dev/forks/XNAT-Dashboards
git checkout staging
#git pull
cd bin
#CI_TEST=0
python3 download_data.py -i /home/marina/.xnat.cfg -o ~/data_prod/prod.pickle
python3 stop_run_dashboards.py
python3 run_dashboards.py -c /home/marina/Dev/forks/XNAT-Dashboards/config.json -p ~/data_prod/prod.pickle

