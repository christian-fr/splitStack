from typing import List, Union, Tuple, Dict, Optional
import datetime
import pprint

from context.json_data import JSON_ARRAY_01
from context.json_data import SPLIT_TYPE_VAR


def get_episode(json_array: List[dict], index: Union[int, str]) -> dict:
    if int(index) < 0 or int(index) > len(json_array) - 1:
        return {}
    try:
        return json_array[int(index)]
    except:
        breakpoint()


def get_json_property(episode: dict, prprty: str) -> Union[dict, list, str, None]:
    if prprty in episode.keys():
        return episode[prprty]
    else:
        return None


def remove_property(episode: dict, prprty: str) -> dict:
    if prprty in episode.keys():
        episode.pop(prprty)
    return episode


def add_or_replace_prprty(episode: dict, prprty: str, value: str) -> dict:
    episode[prprty] = value
    return episode


def valid_timestamp(ts_str: str) -> bool:
    assert as_datetime_timestamp(ts_str)
    return True


def timestamp_within_episode(ts_str: str, episode: dict) -> bool:
    if ts_str is None:
        return False
    ts_1 = as_datetime_timestamp(ts_str)

    ts_0 = as_datetime_timestamp(episode['startDate'])
    ts_n = as_datetime_timestamp(episode['endDate'])
    if ts_0 < ts_1 <= ts_n:
        return True
    else:
        return False


def create_split_stack(json_array: List[dict],
                       episode_index: Union[int, str],
                       split_type_var_dict: dict,
                       previous_split_stack: dict) -> Tuple[List[dict], Dict[str, list]]:
    # create stack
    episode = get_episode(json_array, episode_index)

    split_dict = {}
    for split_type, value in split_type_var_dict.items():

        split_type_var = split_type_var_dict[split_type]["var"]
        split_type_reference_val = split_type_var_dict[split_type]["val"]
        split_type_var_value = get_json_property(episode, split_type_var)

        if split_type_var_value is None:
            continue

        if split_type_var_value == split_type_reference_val:
            split_type_timestamp_var = split_type_var_dict[split_type]['timestampvar']
            split_type_timestamp = get_json_property(episode, split_type_timestamp_var)
            if split_type_timestamp is None:
                continue

            if valid_timestamp(split_type_timestamp):
                if split_type_timestamp in split_dict.keys():
                    split_dict[split_type_timestamp].append(split_type)
                else:
                    split_dict[split_type_timestamp] = [split_type]

            # DEV
            # breakpoint()

            # clean up parent episode
            #  clean up split timestamp
            remove_property(episode, split_type_timestamp_var)
            #  clean up split var
            remove_property(episode, split_type_var)

            # DEV
            # breakpoint()

    for key, val in previous_split_stack.items():
        if key in split_dict.keys():
            split_dict[key]
        else:
            split_dict[key] = val

    return json_array, split_dict


def end_of_current_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=1, days=-1)


def end_of_previous_month(ts: datetime) -> datetime:
    return add_timedelta(ts, months=0, days=-1)


def split_episode(json_array: List[dict],
                  index: Union[int, str],
                  timestamp: str,
                  split_stack: dict) -> Tuple[List[dict], str, dict]:
    index = int(index)
    tmp_json_array = json_array.copy()
    assert valid_timestamp(timestamp)
    ts = as_datetime_timestamp(timestamp)

    parent_episode = tmp_json_array[index]
    max_episode_id = max([int(episode_json['id']) for episode_json in tmp_json_array if 'id' in episode_json.keys()])

    # child episode
    child_id = str(max_episode_id + 1)
    child_episode = parent_episode.copy()
    child_episode = add_or_replace_prprty(child_episode, 'startDate', as_zofar_datetime_str(ts))
    child_episode = add_or_replace_prprty(child_episode, 'id', child_id)
    child_episode = add_or_replace_prprty(child_episode, 'parent', str(parent_episode['id']))
    child_episode = add_or_replace_prprty(child_episode, 'state', 'new')

    if get_json_property(child_episode, 'startDate') in [ts for ts in split_stack.keys()]:
        add_or_replace_prprty(child_episode, 'splitType', split_stack[child_episode['startDate']])
        split_stack.pop(child_episode['startDate'])
    child_episode['splitStack'] = split_stack
    if child_episode['splitStack'] == {}:
        child_episode.pop('splitStack')

    # parent episode
    parent_episode['endDate'] = as_zofar_datetime_str(end_of_previous_month(ts))
    parent_episode['child'] = child_id
    if 'splitStack' in parent_episode:
        parent_episode.pop('splitStack')

    tmp_json_array[index] = parent_episode
    tmp_json_array.append(child_episode)
    new_index = len(tmp_json_array) - 1

    return tmp_json_array, str(new_index), split_stack


def as_zofar_datetime_str(timestamp_str: datetime) -> str:
    return timestamp_str.strftime(format='%Y-%m-%dT01-00-00.000Z')


def as_datetime_timestamp(date_str: str) -> datetime:
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT01-00-00.000Z')


def add_timedelta(ts: datetime, months: int = 0, days: int = 0) -> datetime:
    new_year = ts.year
    months_incr = months
    # additional increment by 1 because we want to decrease it by 1 day (to get the end of the month) later
    new_month = ts.month + months_incr

    if new_month > 12:
        new_year += 1
        new_month = new_month - 12

    return ts.replace(year=new_year, month=new_month) + datetime.timedelta(days=days)


def next_split(json_array: List[dict],
               episode_index: Union[int, str],
               split_stack_dict: dict) -> Tuple[List[dict], str, dict]:
    episode_index = int(episode_index)
    if episode_index == -1:
        breakpoint()

    if split_stack_dict == {}:
        return json_array, str(-1), {}

    def _prepare_timestamp(_split_stack_dict: dict) -> Tuple[Optional[str], Optional[List[str]]]:
        timestamp_list = list(split_stack_dict.keys())
        # noinspection PySimplifyBooleanCheck
        if timestamp_list != []:
            timestamp_list.sort()
            # get the first entry of the split_stack
            _timestamp = timestamp_list[0]
            return _timestamp, timestamp_list
        else:
            return None, None

    timestamp, sorted_timestamp_list = _prepare_timestamp(split_stack_dict)

    if get_episode(json_array, episode_index) != {}:
        while not timestamp_within_episode(timestamp, get_episode(json_array, episode_index)):
            split_stack_dict.pop(timestamp)
            timestamp, sorted_timestamp_list = _prepare_timestamp(split_stack_dict)
            if timestamp is None:
                if 'splitStack' in get_episode(json_array, episode_index):
                    if get_episode(json_array, episode_index)['splitStack'] == {}:
                        # json_array[episode_index] = json_array[episode_index].pop('splitStack')
                        json_array[episode_index].pop('splitStack')

                return json_array, str(-1), {}

    else:
        return json_array, str(-1), {}

    # split the episode at the current timestamp
    json_array, next_episode_index, split_stack_dict = split_episode(json_array, episode_index, timestamp,
                                                                     split_stack_dict)
    # pop the item after the split
    json_array[episode_index]['state'] = 'done'

    return json_array, next_episode_index, split_stack_dict


def main():
    main_json_array = JSON_ARRAY_01
    episode_index = 0

    # Definition:
    # - Modul:
    #   - eine Sammlung von Pages, die aufeinander verweisen und innerhalb der Gesamtbefragung einen Subgraphen
    #     bilden;
    #   - ein Modul beinhaltet detaillierte Nachfragen zu einem bestimmten Episoden-Typ;
    #   - in einem Modul gibt es:
    #     - mind. eine Page, über die das Modul betreten wird;
    #     - mind. eine Page, über die das Modul verlassen wird;
    #     - ggf. Verzweigungen innerhalb des Moduls;
    #     - ggf. Pages, auf denen ->Splitkriterien abgefragt werden;
    #     - ggf. Pages, auf denen ->Splitvariablen abgefragt werden;
    #     - ggf. Pages, auf denen ->Zeitstempel für diese ->Splitvariablen (per Monthpicker) abgefragt werden;
    #     - auf den End-Pages eines Moduls werden ggf. ->Split-Stacks erstellt und
    #       Splits durchgeführt (siehe hierzu: ->Elter-Episode);
    #   - die Modul-Zugehörigkeit einer Page lässt sich durch die ersten n Buchstaben ihres Namens eindeutig erkennen;
    # - Teilmodul:
    #   - innerhalb eines Modul kann es Teilmodule geben;
    #   - diese Teilmodule werden unter bestimmten Bedingungen betreten und wieder verlassen;
    #   - die Teilmodul-Zugehörigkeit einer Page lässt sich durch die ersten n+1 Buchstaben ihres Namens
    #     eindeutig erkennen;
    # - Splitkriterium: ein oder mehrere Merkmale, die inhaltlich zusammenhängen und bei denen eine
    #    eventuelle Änderung mithilfer einer ->Splitvariablen abgefragt wird;
    # - Zeitstempel-Variable: Variable, die über einen Monthpicker erfasst wurde und einen Zeitstempel der Form
    #    "YYYY-MM-DDT01:00:00.000Z" aufweist, wobei
    #     "DD" -> {"01","28","29","30","31"}
    #     sein kann (erster bzw. letzter Tag des Monats);
    # - Splitvariable: eine oder mehre Variablen, deren Beantwortung mit einem bestimmten Wert
    #    die Änderung eines ->Split-Kriteriums markiert und die einen Split auslöst; je nach Kombination aus
    #    Variablenname und Variablenwert wird dem zugehörigen Zeitstempel ein bestimmter ->Split-Typ zugeordnet;
    # - Split-Typ: ein String, der eindeutig eine von ggf. mehreren möglichen Kombinationen von Variablennamen und
    #    Variablenwerten markiert, ihm wird beim Split eine ->Zeitstempel-Variable zugeordnet;
    #    die Split-Typen werden als Map/Dictionary im QML festgelegt zugeführt:
    #      {
    #      	"SplitTypA": [{
    #  	    	           "split_var": {
    #  	    		                    "splitvar01": "val0",
    #  	    		                    "splitvar02": "val1"
    #  	    	                        },
    #  	    	          "timestamp_var": "date_var01"
    #  	                 }],
    #      	"SplitTypB": [{
    #  	    	           "split_var": {
    #  	    		                    "splitvar03": "val0"
    #  	    	                        },
    #  	    	          "timestamp_var": "date_var04"
    #  	                 }],
    #       [...]
    #      }
    #
    # - Split-Stack: eine Map/Dictionary, die aus key-value-Paaren besteht und einem ->Zeitstempel eine Liste von
    #    Split-Typen zuordnet; wenn eine Episode ->Split-Variablen mit Variablenwerten enthält, die sich einem
    #    ->Split-Typ zuordnen lassen; der Split-Stack wird auf Grundlage der ->Split-Variablen und der Variablenwerte
    #    für die aktuelle Episode erstellt; falls bereits ein JSON-Property/Key "splitStack" in der aktuellen Episode
    #    vorhanden ist, werden die Split-Stacks vereinigt;
    #        {
    # 	      "2019-03-01T01:00:00.00Z": ["SplitTypA", "SplitTypD"],
    # 	      "2018-04-01T01:00:00.00Z": ["SplitTypB"],
    # 	      "2019-02-01T01:00:00.00Z": ["SplitTypC"]
    #        }
    #    wenn der Split-Stack leer ist ("{}"), wird die Property aus der Episode entfernt;
    #    wenn der Split-Stack für die aktuelle Episode erstellt wurde (ggf. auch schon während der Erstellung),
    #    werden die ->Split-Variablen, die sich einem ->Split-Typ zuordnen ließen, aus der Episode entfernt;
    #    der Split-Stack liegt unmittelbar nach Erstellung als Property "splitStack" der aktuellen Episode vor;
    #
    #     => hier sollten wir eine "Sicherung" einbauen: falls bereits eine andere Episode existiert (gleich welchen
    #        Typs), die einen Split-Stack (also das Property "splitStack" oder "currentSplit") beinhaltet, werden
    #        diese Properties entfernt, sobald ein neuer Split-Stack erstellt und in der Elter-Episode abgespeichert
    #        wird;
    #
    # - Elter-Episode: wenn für die aktuelle Episode ein Split-Stack erstellt werden konnte oder noch als JSON-Property
    #    vorliegt, wird die aktuelle Episode zu einer Elter-Episode;
    #    - der Status "state" der Elter-Episode wird auf "done" gesetzt;
    #    - der "splitStack" der Elter-Episode wird nach Keys sortiert, der niedrigste Key (->Zeitstempel) wird
    #      ausgewählt;
    #    - dieser niedrigste Key (frühester ->Zeitstempel) wird für die Datumsanpassung genutzt:
    #        parent_episode["endDate"] = earliest_timestamp - 1day
    #        child_episode["startDate"] = earliest_timestamp
    #       falls hierbei auffällt, dass der Zeitstempel nicht innerhalb der Episode liegt, wird der Eintrag des
    #       Split-Stacks entfernt und der nächste niedrigste Zeitstempel wird gesucht;
    #         ** Prüfung, ob ein Split-Zeitstempel innerhalb der Episode liegt **
    #         parent_episode["startDate"] < timestamp_split <=  parent_episode["endDate"
    #    - falls kein Zeitstempel gefunden werden konnte, wird die Episode normal beendet, es wird kein
    #      ->Split-Stack erstellt; es findet kein Split statt;
    #
    #    - falls ein niedrigster Zeitstempel gefunden werden konnte, der innerhalb der Episode liegt:
    #      - die gesamte Elter-Episode wird kopiert, die Kopie bekommt eine neue ID:
    #          child_episode["id"] = max([Liste aller Episoden-IDs aus dem JSON-Array]) +1;
    #      - die Elter-Episode bekommt ein property:
    #          parent_episode["child"] = [child_episode["id"]]
    #        falls das property schon existiert, wird die Liste ergänzt:
    #          parent_episode["child"].append(child_episode["id"])
    #      - die generierte ->Kind-Episode erhält ein property "parent":
    #         child_episode["parent"] = parent_episode["id"]
    #
    #      - der Value des gefundenen, niedrigsten Eintrags im "splitStack" (Liste von ->Split-Typen, z.B.:
    #            ["SplitTypA", "SplitTypB"]
    #          wird ins Property "currentSplit" der ->Kind-Episode kopiert;
    #      - der Eintrag mit dem zuvor gefunden niedrigstens Zeitstempel wird daraufhin aus dem Split-Stack der Kind-
    #        Episode entfernt:
    #         child_episode["splitStack"].pop(**timestamp_used_for_split**)
    #      - der "stackSplit" der Elter-Episode wird entfernt:
    #          parent_episode.pop("splitStack")
    #      - die Property "currentSplit" der Elter-Episode wird entfernt:
    #          parent_episode.pop("currentSplit")
    #      - (die genutzten Split-Variablen und Zeitstempel wurden bereits beim Erstellen des Split-Stacks entfernt;)
    #      - die generierte Episode wird ans JSON-Array angehängt:
    #          JSON_ARRAY.append(child_episode)
    #
    # - Kind-Episode:
    #    - nach erfolgtem Split und kompletter Bearbeitung der Elter-Episode (siehe oben) ist die Kind-Episode
    #      die einzige im JSON-Array, die die Properties "splitStack" und "currentSplit" enthält;
    #    - sie besitzt zudem noch keine -> Split-Variablen oder Zeitstempel-Variablen;
    #
    #  Navigation
    #    - in die Kind-Episode wird navigiert, indem über das Property "child" der noch aktiven Elter-Episode
    #      der Index der Kind-Episode bestimmt wird:
    #        child_episode_index = find_index_of_id(json_array=JSON_ARRAY, id=parent_episode["child"])
    #      (alternativ kann unmittelbar nach Hinzufügen der child_episode zum JSON-Array auch die Länge des Arrays
    #      bestimmt werden und der Wert um 1 verringert werden:
    #        child_episode_index = len(JSON_ARRAY) -1
    #    - falls kein Property "child" gefunden werden kann, wird die Episode normal beendet;
    #    - innerhalb des Moduls, für das ->Split-Typen definiert wurden,


    # Episode filled completely, end-page of module reached
    print('### Episode filled completely, end-page of module reached.')
    pprint.pprint(JSON_ARRAY_01)


    json_array, split_stack = create_split_stack(json_array=main_json_array,
                                                 episode_index=episode_index,
                                                 split_type_var_dict=SPLIT_TYPE_VAR,
                                                 previous_split_stack={})

    # first split
    resulting_json_array, episode_index, split_stack = next_split(json_array=json_array, episode_index=episode_index,
                                                                  split_stack_dict=split_stack)

    print('### we clicked on "Next", first split is done.')
    pprint.pprint(resulting_json_array)

    # second split
    if split_stack != {}:
        resulting_json_array, episode_index, split_stack = next_split(json_array=resulting_json_array,
                                                                      episode_index=episode_index,
                                                                      split_stack_dict=split_stack)

        print('### second split is done.')
        pprint.pprint(resulting_json_array)


if __name__ == '__main__':
    main()
