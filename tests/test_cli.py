import src.modules.cli as cli
import os
import nltk
nltk.download("all",quiet=True)
dirname = os.path.dirname(__file__)


def test_cli_pdf_similarity():
    pdf1 = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    pdf2 = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    cli.pdf_similarity(pdf1, pdf2, False)


def test_snowballing():
    cli.snowballing(os.path.join(dirname, 'snowballing_test_seed_set/'))


def test_extract_pdf_references():
    pdf1 = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    cli.extract_pdf_references(pdf=pdf1, save_to_file="test_result.json")


def test_extract_keyphrases():
    pdf1 = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    cli.extract_keyphrases_pdf(pdf=pdf1)


def test_extract_keywords():
    pdf1 = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    cli.extract_keywords_pdf(pdf=pdf1)


def test_paper_selection():
    cli.paper_selection([" Conspiracy theories explain complex world events with reference to secret plots hatched by powerful groups. Belief in such theories is largely determined by a general propensity towards conspirational thinking. Such a conspiracy mentality can be understood as a generalised political attitude, distinct from established generalised political attitudes such as right\u2013wing authoritarianism (RWA) and social dominance orientation (SDO) (Study 1a, N = 497) that is temporally relatively stable (Study 1b and 1c, total N = 196). Three further studies (combined N = 854) show that in contrast to RWA and SDO, conspiracy mentality is related to prejudice against high\u2013power groups that are perceived as less likeable and more threatening than low\u2013power groups, whereas SDO and RWA are associated with an opposite reaction to perceptions of power. Study 5 (N = 1852) investigates the relationship of conspiracy mentality with political behavioural intentions in a specific catastrophic scenario (i.e. the damage to the Fukushima nuclear reactor after the 2011 tsunami in Japan) revealing a hitherto neglected role of conspiracy mentality in motivating social action aimed at changing the status quo. Copyright \u00a9 2013 European Association of Personality Psychology. "],["conspiracy", "conspiracy mentality", "social media", "sausage"])


def test_snowballing_paper_selection():
    cli.snowballing_paper_selection(snowballing_result_path=os.path.join(dirname,
                                                                         '../src/modules/snowballing_result.json'), keywords=["conspiracy", "conspiracy mentality", "social media", "sausage"])


def test_summary():
    cli.summarization(" Conspiracy theories explain complex world events with reference to secret plots hatched by powerful groups. Belief in such theories is largely determined by a general propensity towards conspirational thinking. Such a conspiracy mentality can be understood as a generalised political attitude, distinct from established generalised political attitudes such as right\u2013wing authoritarianism (RWA) and social dominance orientation (SDO) (Study 1a, N = 497) that is temporally relatively stable (Study 1b and 1c, total N = 196). Three further studies (combined N = 854) show that in contrast to RWA and SDO, conspiracy mentality is related to prejudice against high\u2013power groups that are perceived as less likeable and more threatening than low\u2013power groups, whereas SDO and RWA are associated with an opposite reaction to perceptions of power. Study 5 (N = 1852) investigates the relationship of conspiracy mentality with political behavioural intentions in a specific catastrophic scenario (i.e. the damage to the Fukushima nuclear reactor after the 2011 tsunami in Japan) revealing a hitherto neglected role of conspiracy mentality in motivating social action aimed at changing the status quo. Copyright \u00a9 2013 European Association of Personality Psychology.")
