def quality_score(doc):
    score = 100
    issues = []

    font_sizes = []
    for para in doc.paragraphs:
        for run in para.runs:
            if run.font.size:
                font_sizes.append(run.font.size.pt)

    if len(set(font_sizes)) > 3:
        score -= 10
        issues.append("Font inconsistency detected")

    if len(doc.paragraphs) < 5:
        score -= 10
        issues.append("Too little content")

    if score < 0:
        score = 0

    return score, issues
