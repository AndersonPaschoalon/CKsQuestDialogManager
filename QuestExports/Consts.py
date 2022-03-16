
class Consts:
    # file constants
    EXPORT_SCENE_PREFIX = 'SceneDialogue_'
    EXPORT_DIALOG_PREFIX = "dialogueExport"
    EXPORT_SCENE_EXT = ".txt"
    EXPORT_DIALOG_EXT = ".txt"
    EXPORT_SCENE_DELIMITER = "\t"

    # CSV default values
    CSV_COMMENTS_DELIMITER = ","
    CSV_ACTOR_DELIMITER = ","
    CSV_SCENES_ORDER_DELIMITER = ","
    CSV_EMPTY_COLUMN = "--"

    # string labels
    STR_SCENE_VAL = "Scene"
    STR_PLAYER_VAL = "Player"
    STR_EMPTY_ACTOR_ID = "--"

    # CreationKit CSV labels
    # dialog export
    LABEL_DIALOG_FULL_PATH = 'FULL PATH'
    LABEL_DIALOG_FILENAME = 'FILENAME'  # <<<< todo
    LABEL_DIALOG_QUEST_QUEST = 'QUEST'
    LABEL_DIALOG_QUEST_BRANCH = 'BRANCH'
    LABEL_DIALOG_QUEST_TOPIC = 'TOPIC'
    LABEL_DIALOG_QUEST_TYPE = 'TYPE'  # <<<<<< todo
    LABEL_DIALOG_QUEST_FORM_ID = 'TOPICINFO'
    LABEL_DIALOG_PLAYER_PROMPT = 'PROMPT'  # player dialog text
    LABEL_DIALOG_NPC_SPEAKER = 'SPEAKER'   # <<<< todo
    LABEL_DIALOG_NPC_RACE = 'RACE'  # <<<< todo
    LABEL_DIALOG_NPC_VOICE_TYPE = 'VOICE TYPE'
    LABEL_DIALOG_NPC_RESPONSE_INDEX = 'RESPONSE INDEX'    # <<<<<<< todo
    LABEL_DIALOG_NPC_RESPONSE_TEXT = 'RESPONSE TEXT'  # npc dialog text
    LABEL_DIALOG_NPC_EMOTION = 'EMOTION'
    LABEL_DIALOG_CATEGORY = 'CATEGORY'
    # scene export
    LABEL_SCENE_FULL_PATH = 'FULL PATH'
    LABEL_SCENE_FILENAME = 'FILENAME'
    LABEL_SCENE_QUEST = 'QUEST'
    LABEL_SCENE_SCENE = 'SCENE'
    LABEL_SCENE_RESPONSE_INDEX = 'RESPONSE INDEX'
    LABEL_SCENE_CATEGORY = 'CATEGORY'
    LABEL_SCENE_ALIAS = 'ALIAS'
    LABEL_SCENE_VOICE_TYPE = 'VOICE TYPE'
    LABEL_SCENE_RESPONSE_TEXT = 'RESPONSE TEXT'
    LABEL_SCENE_SUPPORTING_DIALOGUE = 'SUPPORTING DIALOGUE'
    LABEL_SCENE_EMOTION = 'EMOTION'
    LABEL_SCENE_SCRIPT_NOTES = 'SCRIPT NOTES'
    LABEL_SCENE_SCENE_PHASE = 'SCENE PHASE'

    # default values
    DEFAULT_BRANCH_DESCRIPTION = "?banch-comment?"
    DEFAULT_QUEST_DESCRIPTION = "?quest-comment?"
    DEFAULT_SCENE_DESCRIPTION = "?scene-comment?"

    # documentation directories
    DOC_HTML_DIR = "/Html/"
    DOC_MD_DIR = "/Md/"
    DOC_JSON_DIR = "/Json/"
    DOC_DOCX_DIR = "/Docx/"
