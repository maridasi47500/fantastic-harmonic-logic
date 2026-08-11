
mkdir templates 
python3 scaffold.py musicalinstrument name
python3 scaffold.py country name
python3 scaffold.py user username password phone email country_id:references pic:file
python3 scaffold.py score title composer bpm caractere key_signature time_signature content  musicalinstrument_id:references
python3 scaffold.py scorehaslogic_post jugdment emotion logic listen_to_the_music play_the_music memoire bpm score_content user_id:references pic:file pic_of_the_score:radio
