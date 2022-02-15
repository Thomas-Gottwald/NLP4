import math
import numpy

from src.modules.Similarities import specter_1to1_cosine
from src.modules.Similarities import specter_query_reference_similarity
from src.modules.Similarities import pdf_similarity
from src.modules.PDFMiner import get_pdf_text
import os
dirname = os.path.dirname(__file__)


def test_1to1_similarity():
    pdf = os.path.join(dirname, 'test_paper/15.pdf')
    paper1 = pdf
    sim = specter_1to1_cosine(get_pdf_text(paper1).rsplit('References', 1)[0], get_pdf_text(paper1).rsplit('References', 1)[0])
    assert math.isclose(sim, 1, abs_tol=1e-2)


def test_query_similarity():
    corpus = {
        "title": "test Title 1 ",
        "abstract": " Conspiracy theories explain complex world events with reference to secret plots hatched by powerful groups. Belief in such theories is largely determined by a general propensity towards conspirational thinking. Such a conspiracy mentality can be understood as a generalised political attitude, distinct from established generalised political attitudes such as right\u2013wing authoritarianism (RWA) and social dominance orientation (SDO) (Study 1a, N = 497) that is temporally relatively stable (Study 1b and 1c, total N = 196). Three further studies (combined N = 854) show that in contrast to RWA and SDO, conspiracy mentality is related to prejudice against high\u2013power groups that are perceived as less likeable and more threatening than low\u2013power groups, whereas SDO and RWA are associated with an opposite reaction to perceptions of power. Study 5 (N = 1852) investigates the relationship of conspiracy mentality with political behavioural intentions in a specific catastrophic scenario (i.e. the damage to the Fukushima nuclear reactor after the 2011 tsunami in Japan) revealing a hitherto neglected role of conspiracy mentality in motivating social action aimed at changing the status quo. Copyright \u00a9 2013 European Association of Personality Psychology. "
    }, {
        "title": "test Title 1 ",
        "abstract": "AbstractVaccination saves millions of lives, and the World Health Organization (WHO) European Region celebrated record high coverage in 2018. Still, national or sub-national coverage is insufficient to stop the spread of vaccine-preventable diseases. Health authorities are increasingly aware of the need to prioritize the \u201cdemand\u201d side of vaccination. Achieving high and equitable vaccination uptake in all population groups is not a quick-fix; it requires long-term investment in multifaceted interventions, informed by research with the target groups. The WHO focuses on both individual and context determinants of vaccination behaviours. Individual determinants include risk perceptions, (dis)trust and perceived constraints; insights from psychology help us understand these. Context determinants include social norms, socioeconomic status and education level, and the way health systems are designed, operate and are financed. The WHO recommends using a proven theoretical model to understand vaccination behaviours and has adapted the \u201cCOM\u2011B model\u201d for their Tailoring Immunization Programmes (TIP) approach. This adapted model is described in the article. Informed by insights into the factors affecting vaccination behaviours, interventions and policies can be planned to increase vaccination uptake. Some evidence exists on proven methods to do this. At the individual level, some interventions have been seen to increase vaccination uptake, and experimental studies have assessed how certain messages or actions affect vaccination perceptions. At the context level, there is more documentation for effective strategies, including those that focus on making vaccination the easy, convenient and default behaviour and that focus on the interaction between caregivers and health workers."
    }
    query = {
        "10.1177/0093650214565914": {
            "title": "Test Title",
            "abstract": " This study joins a growing body of research that demonstrates the behavioral consequences of hostile media perceptions. Using survey data from a nationally representative U.S. sample, this study tests a moderated-mediation model examining the direct and indirect effects of hostile media perceptions on climate change activism. The model includes external political efficacy as a mediator and political ideology and internal political efficacy as moderators. The results show that hostile media perceptions have a direct association with climate activism that is conditioned by political ideology: Among liberals, hostile media perceptions promote activism, whereas among conservatives, they decrease activism. Hostile media perceptions also have a negative, indirect relationship with activism that is mediated through external political efficacy; however, this relationship is conditioned by both ideology and internal political efficacy. Specifically, the indirect effect manifests exclusively among conservatives and moderates who have low internal efficacy. Theoretical, normative, and practical implications are discussed. ",
            "similarity": "0.8984190225601196, similar to corpus_set Papers"
        },
        "0093650214565914": {
            "title": "None",
            "abstract": "None"}
    }
    sim = specter_query_reference_similarity(query_set=query, corpus_set=corpus)
    print(sim)
    assert isinstance(sim, dict)


def test_pdf_similarity():
    pdf = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    sim = pdf_similarity(pdf, pdf, only_abstract=True)
    assert isinstance(sim, numpy.float32)

    pdf = os.path.join(dirname, 'test_paper/rsos.201199.pdf')
    sim = pdf_similarity(pdf, pdf, only_abstract=False)
    assert isinstance(sim, numpy.float32)

    pdf = os.path.join(dirname, 'test_paper/15.pdf')
    sim = pdf_similarity(pdf, pdf, only_abstract=True)
    assert isinstance(sim, numpy.float32)
