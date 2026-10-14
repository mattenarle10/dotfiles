import ast
import io
import pathlib
import re
import sys
import tokenize

import spacy
import tqdm
import nltk.data
import nltk.downloader
from nltk.corpus import wordnet

HERE = pathlib.Path(__file__).resolve().parent
MODEL = 'en_core_web_md'
PHRASES = HERE / 'phrases.txt'
CORPORA = HERE / 'nltk_data'

nltk.data.path.append(str(CORPORA))

CLEAN = 0
FOUND = 1
CANNOT = 2

VERBLESS = 'verbless sentence: the main clause has no verb'

VERBAL = ('VERB', 'AUX')

SUBORDINATORS = (
    'though', 'although', 'because', 'if', 'unless', 'while', 'since',
    'after', 'before', 'when', 'until', 'whereas', 'whether', 'once',
    'as', 'even', 'provided',
)

CONNECTIVES = ('so', 'thus', 'therefore', 'hence', 'meaning', 'ergo')

CONTRAST_OPENERS = ('not', 'never', 'rather', 'instead')

COORDINATORS = ('and', 'or', 'nor', 'but')

DESIGNATION = (
    'name', 'give', 'describe', 'list', 'cite', 'identify', 'define',
    'characterize', 'label', 'mark', 'report', 'record', 'state', 'put',
    'set', 'present', 'denote', 'treat', 'peg', 'class', 'count', 'frame',
    'cast', 'render', 'deem', 'regard', 'construe', 'flag', 'tag',
)

DISCOURSE_NOUNS = (
    'thing', 'things', 'point', 'points', 'edit', 'edits', 'step', 'steps',
    'item', 'items', 'reason', 'reasons', 'gap', 'gaps', 'change', 'changes',
    'fix', 'fixes', 'option', 'options', 'angle', 'angles', 'shape', 'shapes',
    'lesson', 'lessons', 'note', 'notes', 'takeaway', 'takeaways', 'part',
    'parts', 'section', 'sections', 'correction', 'corrections', 'caveat',
    'caveats', 'observation', 'observations', 'detail', 'details',
)

FINITE_TAGS = ('VBZ', 'VBP', 'VBD', 'MD', 'VB')

SUBJECTS = ('nsubj', 'nsubjpass', 'expl')

CLAUSE_OPENERS = ('mark', 'preconj')

DEMONSTRATIVES = ('that', 'this', 'these', 'those')

EMPTY_PRONOUNS = (
    'it', 'this', 'that', 'them', 'these', 'those', 'things', 'everything',
    'anything', 'something',
)

HUMAN_ONLY = (
    'name', 'state', 'say', 'indicate', 'reference', 'detail', 'describe',
    'tell', 'decide', 'determine', 'dictate', 'govern', 'judge', 'choose',
    'want', 'know', 'think', 'believe', 'care', 'refuse', 'insist', 'claim',
    'argue', 'suggest', 'explain', 'note', 'mention', 'confirm', 'declare',
    'clarify', 'specify', 'emphasize', 'remind', 'warn', 'promise', 'admit',
    'settle', 'resolve', 'conclude', 'rule', 'agree', 'approve', 'reject',
    'plan', 'intend', 'aim', 'expect', 'assume', 'prefer', 'wish',
)

OWING_WORDS = ('need', 'deserve', 'bear', 'merit', 'warrant', 'worth', 'require')

ACT_FILES = ('noun.act', 'noun.communication', 'noun.cognition')

SPEECH_NOUNS = ('mention', 'remark', 'repetition')

PLACEMENT_VERBS = ('put', 'place', 'slap', 'stick', 'pin', 'stamp')

NAMING_NOUNS = (
    'word', 'name', 'label', 'term', 'tag', 'number', 'figure', 'price',
    'value',
)

PERMISSION_VERBS = ('let', 'allow', 'permit')

GRADING_WORDS = ('better', 'worse', 'best', 'worst')

SENSE_VERBS = ('smell', 'sniff', 'sense', 'taste', 'feel')

CHANT_RUN = 3
CHANT_WORDS = 3

HARM_NOUNS = ('harm', 'damage', 'good', 'benefit', 'value')

REASON_MARKERS = ('because', 'since')

OWNING_VERBS = ('give', 'have', 'lack', 'grow', 'get')

COMMERCE_VERBS = ('buy', 'sell', 'pay', 'purchase', 'earn', 'spend', 'afford')

BODY_PARTS = (
    'eye', 'hand', 'arm', 'leg', 'nose', 'ear', 'mouth', 'tooth', 'foot',
    'finger', 'shoulder',
)

CONTAINER_NOUNS = (
    'part', 'bit', 'piece', 'aspect', 'element', 'portion', 'chunk',
)

CREATION_VERBS = (
    'build', 'create', 'make', 'add', 'remove', 'delete', 'install',
    'configure', 'provision', 'deploy', 'destroy', 'attach', 'detach',
)

DOCUMENT_NOUNS = (
    'runbook', 'document', 'spec', 'specification', 'guide', 'section',
    'chapter', 'page', 'blueprint', 'plan', 'policy', 'standard',
)

PROCESS_NOUNS = (
    'run', 'call', 'attempt', 'invocation', 'execution', 'pass',
    'lookup', 'fetch', 'retry', 'reload', 'restart', 'rollout',
)

DATE_WORDS = (
    'jan', 'january', 'feb', 'february', 'mar', 'march', 'apr', 'april',
    'may', 'jun', 'june', 'jul', 'july', 'aug', 'august', 'sep', 'sept',
    'september', 'oct', 'october', 'nov', 'november', 'dec', 'december',
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday', 'today', 'yesterday', 'tomorrow', 'tonight',
)

EVENT_NOUNS = PROCESS_NOUNS + DATE_WORDS

INSISTING_ADJECTIVES = ('exact', 'same', 'very', 'precise', 'identical')

NAMELESS_PRONOUNS = ('mine', 'yours', 'hers', 'ours', 'theirs')

PLACE_WORDS = ('there', 'here', 'where')

CONTENT_SLOTS = ('nsubj', 'dobj', 'attr')

MIND_VERB_FILES = ('verb.cognition', 'verb.communication', 'verb.emotion')

SETTLED_VERBS = ('mean', 'pass', 'use')

PROGRAM_NOUNS = (
    'command', 'script', 'hook', 'checker', 'parser', 'tagger', 'suite',
    'runner', 'process', 'model', 'program', 'tool', 'compiler', 'daemon',
    'service', 'bot', 'agent', 'job',
)

BODY_VERB_FILES = ('verb.motion', 'verb.contact', 'verb.body', 'verb.consumption')

ANIMATE_FILES = ('noun.person', 'noun.animal')

PHYSICAL_FILES = ANIMATE_FILES + (
    'noun.artifact', 'noun.body', 'noun.food', 'noun.object', 'noun.plant',
    'noun.substance',
)

ORDER_NOUNS = (
    'instruction', 'request', 'order', 'direction', 'requirement',
    'recommendation', 'suggestion', 'demand', 'mandate', 'ask',
)


ANNOUNCE_VERBS = (
    'tell', 'explain', 'mention', 'note', 'flag', 'clarify', 'emphasize',
    'stress', 'highlight', 'preface', 'recap', 'summarize', 'remind', 'say',
    'walk', 'point',
)

MODALS = ('will', 'shall', 'should', 'would', 'can', 'could', 'must', 'may')

MENTAL_ORDERS = (
    'note', 'consider', 'observe', 'notice', 'remember', 'recall', 'imagine',
    'picture', 'realize', 'appreciate', 'understand', 'keep', 'bear',
    'reflect', 'weigh', 'contrast', 'compare',
)

BODY_IDIOMS = (
    ('stand', 'behind'), ('stand', 'by'), ('walk', 'back'),
    ('double', 'down'), ('push', 'back'), ('circle', 'back'),
    ('reach', 'out'), ('loop', 'in'), ('weigh', 'in'), ('dig', 'into'),
    ('drill', 'down'), ('flesh', 'out'), ('tease', 'out'),
    ('shore', 'up'), ('zero', 'in'),
)

BANNED_ARRIVAL = ('lands', 'landed', 'landing', 'landings')

ING_ENDING = 'ing'

LANDING_CRAFT = (
    'plane', 'airplane', 'aeroplane', 'aircraft', 'jet', 'helicopter',
    'boat', 'ship', 'ferry', 'vessel',
)

PLACEHOLDER_NOUNS = ('thing', 'things')

EMPTY_NOUNS = PLACEHOLDER_NOUNS + ('one', 'ones')

NAMING = ('NOUN', 'PROPN', 'NUM')

TAIL_JOINERS = ('and', 'so')

CLAUSE_JOINERS = ('and', 'or', 'nor', 'but', 'so', 'yet')

QUOTE_GLYPHS = ('"', "'", '“', '”', '‘', '’')

HANDOVER_VERBS = (
    'give', 'provide', 'supply', 'hand', 'send', 'share',
    'quote', 'cite', 'comment', 'report', 'offer', 'deliver',
)

SPEAKING_VERBS = ('comment', 'report', 'explain', 'remark')

CONTENT_FILES = (
    'noun.communication', 'noun.cognition', 'noun.attribute',
    'noun.quantity', 'noun.act',
)

NEGATIVE_WORDS = ('no', 'not', 'never', 'nothing', 'nobody', 'none', 'neither')

NEGATIVE_SUBJECTS = ('nothing', 'nobody', 'none', 'neither', 'no')

PLURAL_TAG = 'NNS'

PARTNER_DEPS = ('prep', 'prt', 'advmod')

ABSTRACTIONS = (
    'table', 'rule', 'line', 'file', 'path', 'number', 'value', 'target',
    'stop',
    'signal', 'case', 'test', 'check', 'config', 'field', 'column', 'row',
    'sentence', 'word', 'message', 'error', 'change', 'patch', 'commit',
    'branch', 'function', 'method', 'module', 'package', 'code', 'data',
    'account', 'balance', 'price', 'level', 'rate', 'risk', 'cost', 'gap',
    'logic', 'state', 'result', 'output', 'input', 'record', 'entry',
    'setting', 'flag', 'option', 'report', 'document', 'section', 'answer',
    'question', 'point', 'fact', 'reason', 'idea', 'plan', 'problem',
    'issue', 'bug', 'defect', 'feature', 'release', 'version', 'trade',
    'order', 'position', 'strategy', 'model', 'score', 'metric', 'ratio',
    'guard', 'parser', 'tagger', 'hook', 'script', 'checker', 'suite',
    'pattern',
    'command', 'list', 'table', 'clause', 'pronoun',
    'verb', 'noun', 'subject', 'object', 'miss', 'exemption', 'threshold',
    'increase', 'decrease', 'gain', 'loss', 'raise', 'charge', 'fee',
    'amount', 'total', 'sum', 'count', 'share', 'payment', 'invoice',
)

THING_NOUNS = ABSTRACTIONS + DOCUMENT_NOUNS

BODILY_VERBS = (
    'hold', 'move', 'carry', 'reach', 'eat',
    'land', 'bite', 'sit', 'live', 'hang', 'ride', 'travel', 'walk', 'crawl',
    'jump', 'fly', 'climb', 'creep', 'drift', 'bleed', 'breathe', 'sleep',
    'die', 'march', 'sail', 'swim', 'leap', 'dance', 'sing', 'wander',
    'lurk', 'haunt', 'whisper', 'scream', 'stumble', 'limp',
)

NEGATIVE_OBJECTS = ('nothing', 'nobody', 'none', 'neither')

OPEN_OBJECTS = (
    'anything', 'everything', 'something', 'anybody', 'everybody',
    'somebody', 'all', 'both', 'this',
)

VAGUE_ADJECTIVES = (
    'solid', 'real', 'concrete', 'hard', 'substantial', 'meaningful',
    'serious', 'proper', 'actual', 'genuine',
)

CARRIED_CLAUSES = ('csubj', 'ccomp', 'advcl')

WH_WORDS = ('where', 'what', 'how', 'why', 'which', 'who', 'when')

HUMAN_PRONOUNS = (
    'i', 'we', 'you', 'he', 'she', 'they', 'who', 'whoever',
    'me', 'us', 'him', 'her', 'whom',
)
HUMAN_NOUNS = (
    'person', 'people', 'user', 'reader', 'writer', 'author', 'engineer',
    'architect', 'developer', 'team', 'someone', 'anyone', 'everyone',
    'nobody', 'somebody', 'anybody', 'everybody', 'one', 'man', 'woman',
    'child', 'colleague', 'reviewer', 'caller', 'owner', 'customer',
)

RELATIVES = ('which', 'who', 'whom', 'whose', 'where', 'when', 'whereby', 'wherein', 'whereupon', 'that')

HASH_COMMENT = (
    '.py', '.sh', '.bash', '.zsh', '.rb', '.yaml', '.yml', '.toml', '.conf',
    '.tf', '.pl', '.r', '.ps1', '.gradle', '.cmake', '.mk', '.dockerfile',
)
SLASH_COMMENT = (
    '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.dart', '.java', '.kt',
    '.kts', '.swift', '.c', '.h', '.cc', '.cpp', '.hpp', '.cs', '.go', '.rs',
    '.php', '.scala', '.groovy', '.m', '.mm', '.proto', '.sass', '.scss',
)
DASH_COMMENT = ('.sql', '.lua', '.hs', '.ada')
DOCUMENT = ('.md', '.markdown', '.txt', '.rst', '.adoc', '')

LINE_HASH = re.compile(r'(^|\s)#+\s?(?P<text>.*)$')
LINE_SLASH = re.compile(r'(^|\s)//+\s?(?P<text>.*)$')
LINE_DASH = re.compile(r'(^|\s)--\s?(?P<text>.*)$')
BLOCK_C = re.compile(r'/\*(?P<text>.*?)\*/', re.S)

DOCSTRING_HOLDERS = (
    ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef,
)
STRIP_STARS = re.compile(r'^\s*\*\s?', re.M)

FENCE = re.compile(r'^\s*```')
INLINE_CODE = re.compile(r'`[^`]*`')
HEADING = re.compile(r'^\s*#')
HEADING_TEXT = re.compile(r'^\s*#{1,6}\s+(?P<text>[^#].*?)\s*#*\s*$')
TABLE = re.compile(r'^\s*\|')
SEPARATOR = re.compile(r'^[\s:-]+$')
WRAPPERS = '"\'`()[]{}“”‘’«»'

ADDRESS_END = r'[^\s.,;:!?)\]]'
URL = re.compile(r'https?://\S*' + ADDRESS_END)
PATHLIKE = re.compile(r'(^|\s)[~./]\S*' + ADDRESS_END)


class ModelMissing(Exception):
    pass


class CorpusMissing(Exception):
    pass


def main(argv):
    path, rest = _path_flag(argv)
    try:
        text = _read(rest)
        nlp = _load()
        _corpora()
        phrases = _phrases()
    except (
        ModelMissing, CorpusMissing, OSError, UnicodeDecodeError
    ) as error:
        print(error, file=sys.stderr)
        return CANNOT

    try:
        readable = _readable(text, path or _named(rest))
    except (SyntaxError, tokenize.TokenError) as error:
        print('this file is not valid python: %s' % error, file=sys.stderr)
        return CANNOT

    findings = _findings(nlp, phrases, readable)
    for rule, sentence in findings:
        print('%s\t%s' % (rule, sentence))
    if findings:
        return FOUND
    return CLEAN


def _path_flag(argv):
    if len(argv) >= 2 and argv[0] == '--path':
        return argv[1], argv[2:]
    return None, argv


def _named(argv):
    if len(argv) > 0:
        return argv[0]
    return ''


def _readable(text, name):
    if not name:
        return _finished_sentences(text)
    suffix = pathlib.Path(name).suffix.lower()
    if suffix in DOCUMENT:
        return _prose(text)
    return _comments(text, suffix)


def _finished_sentences(text):
    kept = []
    for line in _prose(text).splitlines():
        stripped = line.strip()
        if stripped == '':
            continue
        probe = stripped.strip(WRAPPERS)
        if probe == '':
            continue
        if probe[-1] not in '.!?:':
            continue
        kept.append(stripped)
    return '\n'.join(kept)


def _comments(text, suffix):
    pieces = []
    if suffix == '.py':
        pieces.extend(_python_prose(text))
    if suffix in HASH_COMMENT and suffix != '.py':
        pieces.extend(_lines_matching(text, LINE_HASH))
    if suffix in SLASH_COMMENT:
        pieces.extend(_lines_matching(text, LINE_SLASH))
        pieces.extend(_blocks(text, BLOCK_C))
    if suffix in DASH_COMMENT:
        pieces.extend(_lines_matching(text, LINE_DASH))
    kept = '\n'.join(pieces)
    return _prose(kept)


def _python_prose(text):
    pieces = []
    reader = io.StringIO(text).readline
    for token in tokenize.generate_tokens(reader):
        if token.type != tokenize.COMMENT:
            continue
        pieces.append(token.string.lstrip('#').strip())
    for node in ast.walk(ast.parse(text)):
        if not isinstance(node, DOCSTRING_HOLDERS):
            continue
        found = ast.get_docstring(node)
        if found:
            pieces.append(_under_the_summary(found))
    return pieces


def _under_the_summary(docstring):
    lines = docstring.splitlines()
    return '\n'.join(lines[1:])


def _lines_matching(text, pattern):
    found = []
    for line in text.splitlines():
        match = pattern.search(line)
        if match is None:
            continue
        found.append(match.group('text').strip())
    return found


def _blocks(text, pattern):
    found = []
    for match in pattern.finditer(text):
        body = STRIP_STARS.sub('', match.group('text'))
        for part in body.split('\n\n'):
            found.append(' '.join(part.split()))
    return found


def _read(argv):
    if len(argv) > 0:
        return pathlib.Path(argv[0]).read_text(encoding='utf-8')
    return sys.stdin.read()


def _load():
    try:
        return spacy.load(MODEL)
    except OSError as error:
        raise ModelMissing(
            'the %s model is not installed: %s' % (MODEL, error)
        ) from error


def _corpora():
    try:
        nltk.data.find('corpora/wordnet.zip', paths=[str(CORPORA)])
    except LookupError:
        _fetch_wordnet()


def _fetch_wordnet():
    loader = nltk.downloader.Downloader()
    done = 0
    with tqdm.tqdm(total=100, desc='downloading wordnet', unit='%') as bar:
        for message in loader.incr_download('wordnet', str(CORPORA)):
            reached = _percent(message, done)
            bar.update(reached - done)
            done = reached


def _percent(message, done):
    if isinstance(message, nltk.downloader.ErrorMessage):
        raise CorpusMissing(
            'the wordnet corpus could not be downloaded: %s' % message.message
        )
    if isinstance(message, nltk.downloader.ProgressMessage):
        return message.progress
    if isinstance(message, nltk.downloader.FinishPackageMessage):
        return 100
    return done


def _phrases():
    if not PHRASES.exists():
        return []
    lines = PHRASES.read_text(encoding='utf-8').splitlines()
    kept = []
    for line in lines:
        stripped = line.strip()
        if stripped == '' or stripped.startswith('#'):
            continue
        kept.append(stripped.lower())
    return kept


def _prose(text):
    kept = []
    fenced = False
    for line in _without_frontmatter(text.splitlines()):
        if FENCE.match(line):
            fenced = not fenced
            kept.append('')
            continue
        if fenced:
            kept.append('')
            continue
        if TABLE.match(line):
            kept.append('')
            for cell in _cells(line):
                kept.append(cell)
                kept.append('')
            continue
        heading = HEADING_TEXT.match(line)
        if heading is not None:
            kept.append('')
            kept.append(heading.group('text').strip())
            kept.append('')
            continue
        line = INLINE_CODE.sub(' it ', line)
        line = URL.sub(' it ', line)
        line = PATHLIKE.sub(' it ', line)
        line = re.sub(r'^\s*[-*]\s+', '', line)
        line = line.replace('**', '')
        kept.append(line)
    return '\n'.join(kept)


def _cells(line):
    found = []
    for piece in line.strip().strip('|').split('|'):
        cell = piece.strip()
        if cell == '' or SEPARATOR.match(cell):
            continue
        found.append(cell)
    return found


def _without_frontmatter(lines):
    if not lines or lines[0].strip() != '---':
        return lines
    for index in range(1, len(lines)):
        if lines[index].strip() == '---':
            return lines[index + 1:]
    return lines


def _findings(nlp, phrases, prose):
    found = []
    kept = []
    for sentence in _sentences(nlp, prose):
        text = ' '.join(sentence.text.split())
        if len(text) < 3:
            continue
        kept.append(sentence)
        for rule in _rules(sentence, text, phrases):
            found.append((rule, text))
    found = _without_the_lone_fragment(found, kept)
    run = _telegraph_run(kept)
    if run is not None:
        found.append(run)
    chant = _chant(kept)
    if chant is not None:
        found.append(chant)
    return found


def _chant(sentences):
    run = 1
    opening = None
    for sentence in sentences:
        words = sentence.text.lower().split()
        if len(words) < CHANT_WORDS:
            opening = None
            run = 1
            continue
        here = tuple(words[:CHANT_WORDS])
        if here == opening:
            run = run + 1
        else:
            opening = here
            run = 1
        if run >= CHANT_RUN:
            return (
                'chant: %d sentences open with the same three words' % run,
                'the whole message',
            )
    return None


def _sentences(nlp, prose):
    found = []
    for block in prose.split('\n\n'):
        text = block.strip()
        if text == '':
            continue
        found.extend(nlp(text).sents)
    return found


def _without_the_lone_fragment(found, sentences):
    if len(sentences) != 1:
        return found
    return [one for one in found if one[0] != VERBLESS]


SHORT_WORDS = 9

TERSE_MEAN = 8.0
TERSE_RUN = 6

JOINERS = COORDINATORS + CONNECTIVES + SUBORDINATORS + RELATIVES


def _telegraph_run(sentences):
    if len(sentences) < TERSE_RUN:
        return None
    lengths = [len(sentence.text.split()) for sentence in sentences]
    mean = sum(lengths) / len(lengths)
    if mean >= TERSE_MEAN:
        return None
    longest = _longest_stub_run(sentences)
    if longest < TERSE_RUN:
        return None
    return (
        'telegraph cadence: %d short sentences in a row, averaging %.1f words'
        % (longest, mean),
        'the whole message',
    )


def _longest_stub_run(sentences):
    longest = 0
    run = 0
    for sentence in sentences:
        if _is_a_stub(sentence):
            run = run + 1
            longest = max(longest, run)
            continue
        run = 0
    return longest


def _is_a_stub(sentence):
    if len(sentence.text.split()) > SHORT_WORDS:
        return False
    for token in sentence:
        if token.lower_ in JOINERS:
            return False
    return True


def _rules(sentence, text, phrases):
    broken = []
    if _is_verbless(sentence) and _closes_a_sentence(text):
        broken.append(VERBLESS)
    if _closes_on_a_pronoun(sentence):
        broken.append('the sentence closes on "it": name the thing, so write "I named the column"')
    if _closes_on_an_ing_word(sentence) and _closes_a_sentence(text):
        broken.append('the last word ends in -ing: finish the sentence on another word, so write "I fix the door tomorrow"')
    if _lands_without_a_craft(sentence):
        broken.append('the banned verb: only a plane or a boat lands, so write "The plane landed on time"')
    if _is_label(sentence, text):
        broken.append('label line: a heading standing in for a sentence')
    if _is_triad(sentence):
        broken.append('three clauses in one sentence: give each one its own')
    if _is_summary_slogan(sentence):
        broken.append('slogan: "That is the X" says nothing, so say the thing')
    if _has_possessed_gerund(sentence):
        broken.append('possessed gerund: say "whether I remember", not "my remembering"')
    if _announces_structure(sentence):
        broken.append('announcement: a count of my own points, not of the work')
    if _designates_with_as(sentence):
        broken.append('designation: write "Y is Z", never "X names Y as Z"')
    if _makes_a_pronoun_something(sentence):
        broken.append('light verb: name the thing and the action, not "make it X"')
    if _puts_a_non_actor_in_the_do_er_slot(sentence):
        broken.append('non-actor as the do-er: name the one that really acts, so write "The app shows the symbol"')
    if _explains_after_a_finished_clause(sentence):
        broken.append('overexplained tail: the sentence is finished, so write "The suite passed"')
    if _misses_the_oxford_comma(sentence):
        broken.append('no Oxford comma: write "I read the page, and the default is 14 bars"')
    if _claims_a_handover_with_no_content(sentence):
        broken.append('handover with no content: give the thing, so write "The measurement is 80,095.90"')
    if _adds_a_tail_with_nothing_new(sentence):
        broken.append('tail with nothing new: stop at the first clause, so write "Three older rows print a second message now"')
    if _points_at_everything(sentence):
        broken.append('pointer in every slot: name a thing the reader can check, so write "I put the fragment in the middle of your paragraph"')
    if _points_at_a_value(sentence):
        broken.append('pointer at a value: give the value, so write "you read 80,095.90 off the chart"')
    if _makes_a_thing_owe_an_act(sentence):
        broken.append('owed act: ask the question itself, so write "Which of these two rows do you want?"')
    if _repeats_its_own_head_noun(sentence):
        broken.append('repeated pair: name the two things once, so write "each mode has two tables"')
    if _asserts_and_denies(sentence):
        broken.append('corrective: say where the fix starts and stop')
    if _grades_the_harm(sentence):
        broken.append('verdict: name the sentence it breaks, not the amount of harm')
    if _argues_for_its_own_clause(sentence):
        broken.append('tail that argues for my own sentence: cut the tail and leave the instruction')
    if _hands_the_reader_a_sense_verb(sentence):
        broken.append('sense verb on the reader: he read the words, so quote the words')
    if _leans_on_a_container_noun(sentence):
        broken.append('container noun: quote the words, so write "the sentence about the cutoff"')
    if _grades_a_thing(sentence):
        broken.append('grade in place of a fact: give the number or the name, so write "I invented the 20"')
    if _puts_a_word_on_a_pronoun(sentence):
        broken.append('coined idiom: nobody puts a word on a thing, so ask what the thing is called')
    if _grants_the_reader_permission(sentence):
        broken.append('granted permission: he judges his own work without my permission, so state the fact and stop')
    if _announces_my_own_telling(sentence):
        broken.append('announcement: write "Here is why:" and then the reason')
    if _hides_the_statement_in_a_wh_clause(sentence, text):
        broken.append('empty frame: state the thing, or end the line with a colon')
    if _orders_the_reader(sentence):
        broken.append('order to the reader: state the fact and let him read it his own way')
    if _takes_a_bare_indefinite_object(sentence):
        broken.append('bare object: name the thing, so the reader can check it')
    if _uses_a_body_idiom(sentence):
        broken.append('idiom: say what you did or did not do, not what you stand behind')
    if _describes_a_non_action(sentence):
        broken.append('non-action: name the verb, so write "it avoids the problem"')
    if _takes_a_placeholder_subject(sentence):
        broken.append('placeholder subject: say which one, never "a thing"')
    if _equates_two_categories(sentence):
        broken.append('category equation: say what it does, never "X is Y" with a bare plural')
    if _denies_twice(sentence):
        broken.append('double negative: say it once')
    if _turns_an_order_into_a_noun(sentence):
        broken.append('nominalised order: write the order as an order')
    if _puts_two_noun_phrases_around_be(sentence):
        broken.append('nominalised pair: name the actor and the action, so write who does what')
    if _denies_on_the_object(sentence):
        broken.append('denial on the object: say what you did, so write "Every term of the old file is in the new file"')
    tail = _bad_tail(sentence)
    if tail is not None:
        broken.append(tail)
    hit = _phrase_in(text, phrases)
    if hit is not None:
        broken.append('canned phrase: %s' % hit)
    return broken


def _denies_on_the_object(sentence):
    for token in sentence:
        if token.dep_ != 'dobj':
            continue
        for child in token.children:
            if child.dep_ == 'det' and child.lower_ == 'no':
                return True
    return False


def _closes_a_sentence(text):
    return text.endswith(('.', '!', '?'))


def _announces_structure(sentence):
    for token in sentence:
        if token.lower_ not in DISCOURSE_NOUNS:
            continue
        if token.dep_ not in SUBJECTS:
            continue
        for child in token.children:
            if child.dep_ != 'nummod':
                continue
            if child.like_num and not child.is_alpha:
                continue
            return True
        if _counts_its_own_parts(sentence):
            return True
    return False


def _designates_with_as(sentence):
    for token in sentence:
        if token.pos_ not in ('VERB', 'NOUN'):
            continue
        if token.lemma_ not in DESIGNATION:
            continue
        if not _has_as_phrase(token):
            continue
        if _has_child(token, 'dobj') or _has_child(token, 'appos'):
            return True
    return False


def _takes_a_bare_indefinite_object(sentence):
    for token in sentence:
        if token.dep_ != 'dobj':
            continue
        if _is_denied(token.head):
            continue
        word = token.lemma_.lower()
        if word in NEGATIVE_OBJECTS:
            return True
        if word in OPEN_OBJECTS and _is_bare(token):
            return True
    return False


def _is_bare(token):
    for child in token.children:
        if child.lower_ == 'else':
            continue
        if child.lemma_.lower() in VAGUE_ADJECTIVES:
            continue
        return False
    return True


def _orders_the_reader(sentence):
    root = sentence.root
    if root.pos_ != 'VERB' or root.tag_ != 'VB':
        return False
    if root.lemma_.lower() not in MENTAL_ORDERS:
        return False
    return not _has_child(root, 'nsubj')


def _hides_the_statement_in_a_wh_clause(sentence, text):
    if text.endswith(':'):
        return False
    root = sentence.root
    if root.lemma_ != 'be':
        return False
    for child in root.children:
        if child.dep_ in CARRIED_CLAUSES and _opens_with_a_question_word(child):
            return True
        if child.dep_ != 'attr':
            continue
        for grandchild in child.children:
            if grandchild.dep_ != 'relcl':
                continue
            if _opens_with_a_question_word(grandchild):
                return True
    return False


def _opens_with_a_question_word(clause):
    tokens = list(clause.subtree)
    if not tokens:
        return False
    return tokens[0].lower_ in WH_WORDS


def _announces_my_own_telling(sentence):
    for token in sentence:
        if token.pos_ != 'VERB':
            continue
        if token.lemma_ not in ANNOUNCE_VERBS:
            continue
        if _is_denied(token):
            continue
        if not _speaker_is_me(token):
            continue
        if token.tag_ == 'VB' or _has_modal(token):
            return True
    return False


def _speaker_is_me(token):
    for child in token.children:
        if child.dep_ in SUBJECTS:
            return child.lemma_.lower() in ('i', 'we')
    if token.dep_ in ('xcomp', 'ccomp'):
        return _speaker_is_me(token.head)
    return False


def _has_modal(token):
    for child in token.children:
        if child.dep_ == 'aux' and child.lower_ in MODALS:
            return True
    return False


def _counts_its_own_parts(sentence):
    for token in sentence:
        if token.dep_ != 'nummod':
            continue
        if token.like_num and not token.is_alpha:
            continue
        return True
    return False


def _takes_a_placeholder_subject(sentence):
    for token in sentence:
        if token.dep_ not in SUBJECTS:
            continue
        if token.lemma_.lower() not in PLACEHOLDER_NOUNS:
            continue
        if _carries_only_a_determiner(token):
            return True
    return False


def _carries_only_a_determiner(token):
    for child in token.children:
        if child.dep_ != 'det':
            return False
    return True


def _equates_two_categories(sentence):
    root = sentence.root
    if root.lemma_ != 'be':
        return False
    for child in root.children:
        if child.dep_ != 'attr':
            continue
        if child.tag_ != PLURAL_TAG:
            continue
        if _carries_only_a_determiner(child) and not _has_child(child, 'det'):
            return True
    return False


def _makes_a_document_build_something(sentence):
    for token in sentence:
        if token.pos_ not in ('VERB', 'NOUN'):
            continue
        if token.lemma_.lower() not in CREATION_VERBS:
            continue
        if _is_denied(token):
            continue
        if _has_document_subject(token):
            return True
    return False


def _has_document_subject(token):
    for child in token.children:
        if child.dep_ not in SUBJECTS:
            continue
        if child.lemma_.lower() in DOCUMENT_NOUNS:
            return True
    return False


def _puts_a_non_actor_in_the_do_er_slot(sentence):
    for test in NON_ACTOR_TESTS:
        if test(sentence):
            return True
    return False


def _hands_a_thing_a_verb_it_cannot_do(sentence):
    for token in sentence:
        if token.pos_ != 'VERB':
            continue
        lemma = token.lemma_.lower()
        if lemma in SETTLED_VERBS:
            continue
        subject = _child_in(token, ('nsubj',))
        if subject is None:
            continue
        family = _first_sense_file(lemma, 'v')
        if family in MIND_VERB_FILES and not _sits_in(subject, ANIMATE_FILES):
            return True
        if family not in BODY_VERB_FILES:
            continue
        if not _sits_in(subject, PHYSICAL_FILES):
            return True
        if _sits_in(subject, ANIMATE_FILES):
            continue
        target = _child_in(token, ('dobj',))
        if target is not None and not _sits_in(target, PHYSICAL_FILES):
            return True
    return False


def _first_sense_file(word, kind):
    found = wordnet.synsets(word, pos=kind)
    if not found:
        return None
    return found[0].lexname()


def _sits_in(token, families):
    if _is_human(token):
        return True
    if token.lemma_.lower() in PROGRAM_NOUNS:
        return True
    if token.lemma_.lower() in THING_NOUNS:
        return False
    for sense in wordnet.synsets(token.lemma_.lower(), pos='n'):
        if sense.lexname() in families:
            return True
    return False


def _explains_after_a_finished_clause(sentence):
    root = sentence.root
    if not _has_child(root, 'nsubj'):
        return False
    for token in sentence:
        if token.lower_ != 'so':
            continue
        if token.dep_ == 'advmod' and token.head == root:
            return True
    return False


def _misses_the_oxford_comma(sentence):
    if _opens_with_a_coordinator(sentence):
        return True
    for token in sentence:
        if token.dep_ != 'cc' or token.lower_ not in CLAUSE_JOINERS:
            continue
        if token.i == 0 or _sits_between_quotes(token):
            continue
        if _sits_inside_a_quotation(token, sentence):
            continue
        if _breaks_a_series(token):
            return True
        if token.doc[token.i - 1].text == ',':
            continue
        if _joins_two_clauses(token):
            return True
    return False


def _opens_with_a_coordinator(sentence):
    first = sentence[0]
    return first.dep_ == 'cc' and first.lower_ in CLAUSE_JOINERS


def _breaks_a_series(joiner):
    opening = _first_item(joiner)
    members = [
        member for member in _series_members(opening)
        if member.pos_ == opening.pos_
    ]
    if len(members) < 3:
        return False
    gaps = [(members[i], members[i + 1]) for i in range(len(members) - 1)]
    if all(_holds_a_coordinator(first, second) for first, second in gaps):
        return False
    for first, second in gaps:
        if not _holds_a_comma(first, second):
            return True
    return False


def _series_members(head):
    members = [head]
    for child in head.children:
        if child.dep_ == 'conj' or _follows_a_comma(child):
            members.extend(_series_members(child))
    return sorted(members, key=lambda token: token.i)


def _follows_a_comma(child):
    if child.dep_ != 'appos':
        return False
    opening = child.left_edge.i
    return opening > 0 and child.doc[opening - 1].text == ','


def _holds_a_comma(first, second):
    return ',' in _between(first, second)


def _holds_a_coordinator(first, second):
    for token in _gap(first, second):
        if token.dep_ == 'cc' and token.lower_ in CLAUSE_JOINERS:
            return True
    return False


def _gap(first, second):
    opening = second.left_edge.i
    if opening <= first.i:
        opening = second.i
    return first.doc[first.i + 1:opening]


def _between(first, second):
    return [token.text for token in _gap(first, second)]


def _first_item(joiner):
    head = joiner.head
    while head.dep_ in ('conj', 'appos'):
        head = head.head
    return head


def _joins_two_clauses(joiner):
    first = _first_item(joiner)
    second = _child_in(first, ('conj',))
    if second is None:
        return False
    if first.pos_ not in VERBAL or second.pos_ not in VERBAL:
        return False
    if _child_in(second, ('nsubj', 'nsubjpass')) is None:
        return False
    return _child_in(first, ('nsubj', 'nsubjpass')) is not None


def _sits_inside_a_quotation(joiner, sentence):
    marks = 0
    for token in sentence:
        if token.i >= joiner.i:
            break
        if token.text in QUOTE_GLYPHS:
            marks += 1
    return marks % 2 == 1


def _sits_between_quotes(joiner):
    doc = joiner.doc
    if doc[joiner.i - 1].text in QUOTE_GLYPHS:
        return True
    if joiner.i + 1 >= len(doc):
        return False
    return doc[joiner.i + 1].text in QUOTE_GLYPHS


def _claims_a_handover_with_no_content(sentence):
    for token in sentence:
        if token.pos_ not in VERBAL:
            continue
        lemma = token.lemma_.lower()
        if lemma not in HANDOVER_VERBS:
            continue
        giver = _child_in(token, SUBJECTS)
        if giver is None or not _is_human(giver):
            continue
        if _child_in(token, ('neg',)) is not None:
            continue
        if _carries_content(sentence):
            return False
        target = _child_in(token, ('dobj',))
        if target is None:
            if lemma in SPEAKING_VERBS:
                return True
            continue
        if _carries_a_no(target):
            continue
        if _first_sense_file(target.lemma_.lower(), 'n') in CONTENT_FILES:
            return True
    return False


def _carries_content(sentence):
    for token in sentence:
        if token.pos_ == 'NUM':
            return True
        if token.text in QUOTE_GLYPHS or token.text == ':':
            return True
        if token.dep_ == 'ccomp':
            return True
    return False


def _adds_a_tail_with_nothing_new(sentence):
    root = sentence.root
    if not _has_child(root, 'nsubj'):
        return False
    if not _joins_a_tail(root):
        return False
    for tail in root.children:
        if tail.dep_ != 'conj':
            continue
        if not _has_child(tail, 'nsubj'):
            continue
        if _names_a_new_thing(root, tail):
            continue
        return True
    return False


def _joins_a_tail(root):
    for child in root.children:
        if child.dep_ == 'cc' and child.lower_ in TAIL_JOINERS:
            return True
    return False


def _names_a_new_thing(root, tail):
    inside = set(token.i for token in tail.subtree)
    earlier = set()
    for token in root.subtree:
        if token.i in inside:
            continue
        earlier.add(token.lemma_.lower())
    for token in tail.subtree:
        if token.pos_ not in NAMING:
            continue
        lemma = token.lemma_.lower()
        if lemma in EMPTY_NOUNS or lemma in earlier:
            continue
        return True
    return False


def _makes_an_event_the_actor(sentence):
    for token in sentence:
        if token.dep_ not in SUBJECTS:
            continue
        if token.lower_ not in EVENT_NOUNS and token.lemma_.lower() not in EVENT_NOUNS:
            continue
        if token.head.pos_ not in VERBAL:
            continue
        if token.head.lemma_ == 'be':
            continue
        return True
    return False


def _points_at_everything(sentence):
    for token in sentence:
        if token.lower_ in NAMELESS_PRONOUNS and token.dep_ in CONTENT_SLOTS:
            return True
    if not _subject_points_back(sentence):
        return False
    for token in sentence:
        if token.lower_ in PLACE_WORDS and token.dep_ in ('advmod', 'mark'):
            return True
        if token.dep_ != 'dobj':
            continue
        if token.lemma_.lower() in NEGATIVE_OBJECTS:
            return True
        if _carries_a_no(token):
            return True
    return False


def _subject_points_back(sentence):
    subject = _child_in(sentence.root, SUBJECTS)
    if subject is None:
        return False
    return subject.lower_ in EMPTY_PRONOUNS or subject.lower_ in NAMELESS_PRONOUNS


def _carries_a_no(token):
    for child in token.children:
        if child.dep_ == 'det' and child.lower_ == 'no':
            return True
    return False


def _points_at_a_value(sentence):
    for token in sentence:
        if token.lemma_.lower() not in NAMING_NOUNS:
            continue
        if not _has_demonstrative_determiner(token):
            continue
        if _carries_an_insisting_adjective(token):
            return True
    return False


def _has_demonstrative_determiner(token):
    for child in token.children:
        if child.dep_ == 'det' and child.lower_ in DEMONSTRATIVES:
            return True
    return False


def _carries_an_insisting_adjective(token):
    for child in token.children:
        if child.dep_ != 'amod':
            continue
        if child.lemma_.lower() in INSISTING_ADJECTIVES:
            return True
    return False


def _turns_an_order_into_a_noun(sentence):
    for token in sentence:
        if token.lemma_.lower() not in ORDER_NOUNS:
            continue
        if _carries_an_infinitive(token):
            return True
    return False


def _carries_an_infinitive(token):
    for child in token.children:
        if child.dep_ == 'acl' and child.tag_ == 'VB':
            return True
    return False


def _puts_two_noun_phrases_around_be(sentence):
    root = sentence.root
    if root.lemma_ != 'be':
        return False
    subject = _child_in(root, SUBJECTS)
    complement = _child_in(root, ('attr',))
    if subject is None or complement is None:
        return False
    if not _has_child(subject, 'prep'):
        return False
    return _has_child(complement, 'compound')


def _child_in(root, deps):
    for child in root.children:
        if child.dep_ in deps:
            return child
    return None


def _denies_twice(sentence):
    for token in sentence:
        if token.dep_ not in SUBJECTS:
            continue
        if token.lower_ not in NEGATIVE_SUBJECTS:
            continue
        if _holds_another_negative(sentence, token):
            return True
    return False


def _holds_another_negative(sentence, subject):
    for token in sentence:
        if token.i == subject.i:
            continue
        if token.lower_ in NEGATIVE_WORDS:
            return True
    return False


def _describes_a_non_action(sentence):
    for token in sentence:
        if token.pos_ != 'VERB' or token.lemma_.lower() != 'leave':
            continue
        if _has_child(token, 'dobj') and _has_child(token, 'oprd'):
            return True
    return False


def _uses_a_body_idiom(sentence):
    for token in sentence:
        if token.pos_ != 'VERB':
            continue
        for verb, partner in BODY_IDIOMS:
            if token.lemma_.lower() != verb:
                continue
            if _has_partner(token, partner):
                return True
    return False


def _has_partner(token, partner):
    for child in token.children:
        if child.dep_ not in PARTNER_DEPS:
            continue
        if child.lower_ == partner:
            return True
    return False


def _gives_a_thing_a_body(sentence):
    for token in sentence:
        if token.pos_ not in ('VERB', 'NOUN'):
            continue
        if token.lemma_.lower() not in BODILY_VERBS:
            continue
        if _has_abstract_subject(token):
            return True
        if _leans_on_an_abstraction(token):
            return True
    return False


def _leans_on_an_abstraction(token):
    for child in token.children:
        if child.i > token.i:
            continue
        if child.dep_ not in ('amod', 'compound', 'nmod', 'poss'):
            continue
        if child.lemma_.lower() in ABSTRACTIONS:
            return True
    return False


def _has_abstract_subject(token):
    for child in token.children:
        if child.dep_ not in SUBJECTS:
            continue
        if child.lower_ in EMPTY_PRONOUNS:
            return True
        if child.lemma_.lower() in ABSTRACTIONS:
            return True
    return False


def _gives_a_thing_a_human_verb(sentence):
    for token in sentence:
        if token.lemma_.lower() not in HUMAN_ONLY:
            continue
        if token.pos_ not in ('VERB', 'NOUN'):
            continue
        if _takes_an_empty_pronoun(token):
            return True
        if _sits_before_an_empty_pronoun(token):
            return True
        if _has_human_subject(token):
            continue
        if _has_thing_subject(token):
            return True
    return False


def _has_human_subject(token):
    for child in token.children:
        if child.dep_ in SUBJECTS and _is_human(child):
            return True
    return False


def _has_thing_subject(token):
    for child in token.children:
        if child.dep_ in SUBJECTS and not _is_human(child):
            return True
    return False


def _sits_before_an_empty_pronoun(token):
    doc = token.doc
    index = token.i + 1
    if index >= len(doc):
        return False
    after = doc[index]
    if after.lower_ not in EMPTY_PRONOUNS:
        return False
    return after.dep_ not in SUBJECTS + CLAUSE_OPENERS


def _takes_an_empty_pronoun(token):
    for child in token.children:
        if child.dep_ not in ('dobj', 'appos'):
            continue
        if child.lower_ in EMPTY_PRONOUNS:
            return True
    return False


def _is_denied(token):
    for child in token.children:
        if child.dep_ == 'neg':
            return True
    return False


def _is_human(token):
    if token.ent_type_ == 'PERSON':
        return True
    if token.lower_ in HUMAN_PRONOUNS:
        return True
    if token.lemma_.lower() in HUMAN_NOUNS:
        return True
    return token.pos_ == 'PROPN' and token.ent_type_ == ''


def _makes_a_thing_owe_an_act(sentence):
    for token in sentence:
        if token.lemma_.lower() not in OWING_WORDS:
            continue
        if _is_denied(token):
            continue
        if _has_human_subject(_owner(token)):
            continue
        if _owes_an_act(token):
            return True
    return False


def _owner(token):
    if token.dep_ == 'acomp':
        return token.head
    return token


def _owes_an_act(token):
    for child in token.children:
        if child.dep_ == 'xcomp' and child.pos_ in VERBAL:
            return True
        if child.dep_ not in ('dobj', 'attr'):
            continue
        if child.lemma_.lower() in SPEECH_NOUNS:
            return True
        if _has_child(child, 'poss'):
            return True
        if _first_sense_file(child.lemma_.lower(), 'n') in ACT_FILES:
            return True
    return False


def _repeats_its_own_head_noun(sentence):
    seen = []
    for token in sentence:
        if token.pos_ != 'NOUN':
            continue
        lemma = token.lemma_.lower()
        if token.dep_ == 'conj' and lemma in seen and not _is_told_apart(token):
            return True
        seen.append(lemma)
    return False


def _is_told_apart(token):
    return _has_child(token, 'compound') or _has_child(token, 'amod')


def _asserts_and_denies(sentence):
    for token in sentence:
        if token.dep_ != 'conj':
            continue
        if not _is_denied(token):
            continue
        if token.pos_ not in ('VERB', 'AUX'):
            return True
        if token.lemma_.lower() in ('do', 'be') and not _has_child(token, 'dobj'):
            return True
    return False


def _grades_the_harm(sentence):
    for token in sentence:
        if token.lemma_.lower() not in HARM_NOUNS:
            continue
        if not _carries_a_comparative(token):
            continue
        if _has_abstract_subject(token.head):
            return True
    return False


def _carries_a_comparative(token):
    for child in token.children:
        if child.dep_ != 'amod':
            continue
        if child.lower_ in ('more', 'less'):
            return True
    return False


def _argues_for_its_own_clause(sentence):
    for token in sentence:
        if token.dep_ != 'mark':
            continue
        if token.lower_ not in REASON_MARKERS:
            continue
        if _has_demonstrative_subject(token.head):
            return True
    return False


def _has_demonstrative_subject(clause):
    for child in clause.children:
        if child.dep_ not in SUBJECTS:
            continue
        if child.lower_ in DEMONSTRATIVES:
            return True
    return False


def _makes_a_thing_trade(sentence):
    for token in sentence:
        if token.lemma_.lower() not in COMMERCE_VERBS:
            continue
        if _is_denied(token):
            continue
        if _has_abstract_subject(token):
            return True
    return False


def _gives_a_thing_a_body_part(sentence):
    for token in sentence:
        if token.lemma_.lower() not in OWNING_VERBS:
            continue
        if not _takes_a_body_part(token):
            continue
        if _owner_is_a_thing(token):
            return True
    return False


def _takes_a_body_part(token):
    for child in token.children:
        if child.dep_ != 'dobj':
            continue
        if child.lemma_.lower() in BODY_PARTS:
            return True
    return False


def _owner_is_a_thing(token):
    for child in token.children:
        if child.dep_ not in SUBJECTS + ('dative',):
            continue
        if child.lower_ in EMPTY_PRONOUNS:
            return True
        if child.lemma_.lower() in ABSTRACTIONS:
            return True
    return False


def _hands_the_reader_a_sense_verb(sentence):
    for token in sentence:
        if token.lemma_.lower() not in SENSE_VERBS:
            continue
        if _is_denied(token):
            continue
        if not _has_reader_subject(token):
            continue
        if _names_its_object(token):
            continue
        return True
    return False


def _names_its_object(token):
    for child in token.children:
        if child.dep_ != 'dobj':
            continue
        if child.lower_ not in EMPTY_PRONOUNS:
            return True
    return False


def _leans_on_a_container_noun(sentence):
    for token in sentence:
        if token.dep_ not in SUBJECTS:
            continue
        if token.lemma_.lower() not in CONTAINER_NOUNS:
            continue
        if _carries_only_a_determiner_and_a_clause(token):
            return True
    return False


def _carries_only_a_determiner_and_a_clause(token):
    for child in token.children:
        if child.dep_ not in ('det', 'relcl'):
            return False
    return True


def _grades_a_thing(sentence):
    for token in sentence:
        if token.lower_ not in GRADING_WORDS:
            continue
        if token.dep_ not in ('acomp', 'attr'):
            continue
        if _has_human_subject(token.head):
            continue
        if _has_thing_subject(token.head):
            return True
    return False


def _puts_a_word_on_a_pronoun(sentence):
    for token in sentence:
        if token.lemma_.lower() not in PLACEMENT_VERBS:
            continue
        if not _takes_a_naming_object(token):
            continue
        if _has_empty_prepositional_object(token):
            return True
    return False


def _takes_a_naming_object(token):
    for child in token.children:
        if child.dep_ != 'dobj':
            continue
        if child.lemma_.lower() in NAMING_NOUNS:
            return True
    return False


def _has_empty_prepositional_object(token):
    for child in token.children:
        if child.dep_ != 'prep':
            continue
        if _has_empty_object(child):
            return True
    return False


def _has_empty_object(preposition):
    for child in preposition.children:
        if child.dep_ != 'pobj':
            continue
        if child.lower_ in EMPTY_PRONOUNS:
            return True
    return False


def _grants_the_reader_permission(sentence):
    for token in sentence:
        if token.lemma_.lower() not in PERMISSION_VERBS:
            continue
        if _is_denied(token):
            continue
        if _permits_the_reader(token):
            return True
    return False


def _permits_the_reader(token):
    for child in token.children:
        if child.dep_ == 'ccomp' and _has_reader_subject(child):
            return True
        if child.dep_ == 'dobj' and child.lower_ == 'you':
            return True
    return False


def _has_reader_subject(clause):
    for child in clause.children:
        if child.dep_ in SUBJECTS and child.lower_ == 'you':
            return True
    return False


def _makes_a_pronoun_something(sentence):
    for token in sentence:
        if token.lemma_ != 'make' or token.pos_ != 'VERB':
            continue
        for child in token.children:
            if child.dep_ != 'ccomp':
                continue
            if _has_empty_subject(child):
                return True
    return False


def _has_empty_subject(token):
    for child in token.children:
        if child.dep_ in SUBJECTS and child.lower_ in EMPTY_PRONOUNS:
            return True
    return False


def _has_child(token, dep):
    for child in token.children:
        if child.dep_ == dep:
            return True
    return False


def _has_as_phrase(token):
    for child in token.children:
        if child.dep_ == 'prep' and child.lower_ == 'as':
            return True
    return False


def _is_label(sentence, text):
    if not text.endswith(':'):
        return False
    for token in sentence:
        if token.text == ',':
            break
        if token.pos_ in VERBAL:
            return False
    return True


def _has_possessed_gerund(sentence):
    for token in sentence:
        if not token.lower_.endswith('ing'):
            continue
        if token.pos_ not in ('NOUN', 'VERB'):
            continue
        for child in token.children:
            if child.dep_ == 'poss':
                return True
    return False


def _is_summary_slogan(sentence):
    root = sentence.root
    if root.lemma_ != 'be':
        return False
    subject = None
    for child in root.children:
        if child.dep_ in SUBJECTS:
            subject = child
    if subject is None:
        return False
    if subject.lower_ not in DEMONSTRATIVES:
        return False
    if list(subject.children):
        return False
    for child in root.children:
        if child.dep_ in ('attr', 'acomp') and child.pos_ in ('NOUN', 'PROPN'):
            return True
    return False


def _is_triad(sentence):
    commas = [token for token in sentence if token.text == ',']
    if len(commas) < 2:
        return False
    parallel = [child for child in sentence.root.children if child.dep_ == 'conj']
    return len(parallel) > 1


def _bad_tail(sentence):
    for comma in _commas(sentence):
        if not _opens_a_tail(sentence, comma):
            continue
        chunk = _chunk_after(sentence, comma)
        if not chunk:
            continue
        if chunk[0].lower_ in COORDINATORS:
            continue
        if chunk[0].lower_ in CONNECTIVES:
            continue
        if chunk[0].lower_ in CONTRAST_OPENERS:
            continue
        if _is_marked(chunk):
            continue
        finite = _finite_verbs(chunk)
        if not finite:
            if _holds_coordinator(chunk):
                continue
            return 'trailing fragment: a tail after a comma with no verb'
        if _has_relative_subject(finite):
            return 'trailing adjunct: a relative clause after a comma'
        if _has_own_subject(finite):
            return 'welded clauses: two sentences joined by a comma'
        if _is_imperative(finite):
            continue
        return 'trailing adjunct: a participle or gerund clause after a comma'
    return None


def _commas(sentence):
    return [token for token in sentence if token.text == ',']


def _opens_a_tail(sentence, comma):
    head = [
        token for token in sentence
        if token.i < comma.i and token.pos_ != 'PUNCT'
    ]
    if not head:
        return False
    if head[0].lower_ in SUBORDINATORS:
        return False
    return bool(_finite_verbs(head))


def _holds_coordinator(chunk):
    for token in chunk:
        if token.lower_ in COORDINATORS:
            return True
    return False


def _chunk_after(sentence, comma):
    return [
        token for token in sentence
        if token.i > comma.i and token.pos_ != 'PUNCT'
    ]


def _is_marked(chunk):
    first = chunk[0]
    return first.dep_ == 'mark' and first.lower_ in SUBORDINATORS


def _finite_verbs(chunk):
    return [token for token in chunk if token.tag_ in FINITE_TAGS]


def _has_relative_subject(verbs):
    for verb in verbs:
        for child in verb.children:
            if child.dep_ in SUBJECTS and child.lower_ in RELATIVES:
                return True
    return False


def _has_own_subject(verbs):
    for verb in verbs:
        for child in verb.children:
            if child.dep_ in SUBJECTS:
                return True
    return False


def _is_imperative(verbs):
    for verb in verbs:
        if verb.tag_ == 'VB':
            return True
    return False


MAIN_DEPS = ('ROOT', 'ccomp', 'conj', 'xcomp')


def _closes_on_a_pronoun(sentence):
    for token in reversed(list(sentence)):
        if token.pos_ in ('PUNCT', 'SPACE'):
            continue
        if token.lower_ != 'it' or token.whitespace_ != '':
            return False
        return token.i == 0 or token.doc[token.i - 1].pos_ != 'SPACE'
    return False


def _closes_on_an_ing_word(sentence):
    for token in reversed(list(sentence)):
        if token.pos_ in ('PUNCT', 'SPACE'):
            continue
        return token.lower_.endswith(ING_ENDING)
    return False


def _lands_without_a_craft(sentence):
    for token in sentence:
        spelt = token.lower_ in BANNED_ARRIVAL
        acting = token.lemma_.lower() == 'land' and token.pos_ in VERBAL
        if not spelt and not acting:
            continue
        craft = _child_in(token, SUBJECTS)
        if craft is None:
            return True
        if craft.lemma_.lower() not in LANDING_CRAFT:
            return True
    return False


def _is_verbless(sentence):
    if sentence.root.pos_ in VERBAL:
        return False
    if _holds_a_particle(sentence):
        return False
    if _is_a_mistagged_verb(sentence.root):
        return False
    for token in sentence:
        if token.pos_ in VERBAL and token.dep_ in MAIN_DEPS:
            return False
    return True


LEFT_OF_A_VERB = ('compound', 'nsubj', 'nsubjpass')

RIGHT_OF_A_VERB = ('dobj', 'prep', 'prt', 'dative', 'attr', 'advcl')


def _holds_a_particle(sentence):
    for token in sentence:
        if token.dep_ == 'prt':
            return True
    return False


def _is_a_mistagged_verb(root):
    if root.pos_ != 'NOUN':
        return False
    left = False
    right = False
    for child in root.children:
        if child.i < root.i and child.dep_ in LEFT_OF_A_VERB:
            left = True
        if child.i > root.i and child.dep_ in RIGHT_OF_A_VERB:
            right = True
    return left and right


def _phrase_in(text, phrases):
    lowered = text.lower()
    for phrase in phrases:
        if phrase in lowered:
            return phrase
    return None


def _makes_we_do_the_app_work(sentence):
    for token in sentence:
        if token.pos_ != 'VERB':
            continue
        subject = _child_in(token, ('nsubj',))
        if subject is None or subject.lower_ != 'we':
            continue
        if token.tag_ == 'VBD' and token.lower_ != token.lemma_.lower():
            continue
        target = _child_in(token, ('dobj',))
        if target is None or target.pos_ != 'NOUN':
            continue
        if _has_child(token, 'prep') or _has_child(target, 'prep'):
            return True
    return False


NON_ACTOR_TESTS = (
    _makes_we_do_the_app_work,
    _hands_a_thing_a_verb_it_cannot_do,
    _gives_a_thing_a_human_verb,
    _gives_a_thing_a_body,
    _makes_a_thing_trade,
    _gives_a_thing_a_body_part,
    _makes_a_document_build_something,
    _makes_an_event_the_actor,
)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
