
from django.conf import settings
import uuid
import os

def __save_uploaded_file(dest, filename, uploaded_file):
    file_path = os.path.join(dest, filename)
    with open(file_path, 'wb+') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    return file_path

def __parse_line(source_phrase_model, target_phrase_model, line, sep='\t'):
    pos = line.find(sep)
    source_text, target_text = line[:pos].strip(), line[pos:].strip()

    source_phrase = source_phrase_model(text=source_text) \
                        if len(source_text) > 0 \
                        else None

    target_phrase = target_phrase_model(text=target_text) \
                        if len(target_text) > 0 \
                        else None

    return source_phrase, target_phrase

def handle_phrase_import(source_language, target_language, uploaded_file):

    dest = settings.CORPUS_IMPORTS_DIR 
    filename = f'{uuid.uuid4()}.txt'
    os.makedirs(dest, exist_ok=True)

    file_path = __save_uploaded_file(dest, filename, uploaded_file)

    # saving phrases
    source_phrase_model = source_language.dictionnary.phrases.model
    target_phrase_model = target_language.dictionnary.phrases.model

    # read lines
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[:1000]:
        source_phrase, target_phrase = __parse_line(source_phrase_model, target_phrase_model,line)

        if source_phrase:
            source_phrase.save()
        
        if target_phrase:
            target_phrase.shared_id = source_phrase.shared_id \
                                        if source_phrase \
                                        else target_phrase.shared_id
            target_phrase.save()
    
    # delete after
    os.remove(file_path)






def _line_generator(source_language, target_language):
    source_phrases = source_language \
                        .dictionnary \
                        .phrases \
                        .filter(shared_id__in=[p.shared_id for p in target_language.dictionnary.phrases.all()])
    target_phrases = target_language \
                        .dictionnary \
                        .phrases.all()
    
    for source_phrase in source_phrases:
        match_found = False
        for target_phrase in target_phrases:
            if target_phrase.shared_id == source_phrase.shared_id:
                yield source_phrase, target_phrase
                match_found = True
                break

        if match_found:
            continue
            
        yield source_phrase, source_phrase
            
def _print_as_txt(source_language, target_language, f):
    for s_phrase, t_phrase in _line_generator(source_language, target_language):
        f.write(f"{s_phrase.text}\t{t_phrase.text}\n")

def _print_as_json(source_language, target_language, f):
    import json
    f.write('[')
    
    for s_phrase, t_phrase in _line_generator(source_language, target_language):
        f.write("{json},".format(json=json.dumps({
            source_language.code: s_phrase.text,
            target_language.code: t_phrase.text
        })))

    f.write(']')
    
    
def handle_phrase_export(source_language, target_language, export_as='txt'):
    
    dest = settings.CORPUS_EXPORTS_DIR 
    filename = f'{uuid.uuid4()}.{export_as}'
    os.makedirs(dest, exist_ok=True)
    
    file_path = os.path.join(dest, filename)

    with open(file_path, 'w+', encoding="utf-8") as f:
        {
            'txt' : _print_as_txt,
            'json': _print_as_json
        }[export_as](source_language, target_language, f)


    return file_path




