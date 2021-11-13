#!/bin/bash
start=`date +%s`
python3 Dfs_update.py
python3 covid_estado_sp.py
python3 covid_municipios_sp.py
python3 evolucao_aplicacao_doses.py
python3 isolamento_social.py
python3 leitos_uti_enfermaria.py
python3 srag_covid.py
python3 vacinacao_estatisticas.py
python3 vacinometro_sp.py
end=`date +%s`
runtime=$((end-start))
hours=$((runtime / 3600)); minutes=$(( (runtime % 3600) / 60 ))
seconds=$(( (runtime % 3600) % 60 ))
echo "Runtime: $hours:$minutes:$seconds (hh:mm:ss)"
